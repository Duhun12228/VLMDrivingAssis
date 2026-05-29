"""Local persistence for past analysis runs.

Stores one JSON file per analysis under `~/.drivingassis/history/`. This is
what turns BackMirror from a one-shot scorecard into a coach that
remembers — the Results screen reads `load_prior()` to compare this run
against the previous one.

Why local files (not SQLite): single-user, no concurrent writers, human-
inspectable. We rebuild full records on read so callers can treat them
like the live dataclasses from `core.schema`.
"""
from __future__ import annotations

import dataclasses
import json
import os
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from core.schema import (
    CategoryScore,
    Coaching,
    Event,
    ScoreReport,
)


HISTORY_DIR = Path.home() / ".drivingassis" / "history"

# Filenames are "{ISO timestamp}_{session_id}.json" — sortable by time.
# Colons in ISO timestamps break Windows filenames, so we substitute "-".
_FNAME_RE = re.compile(r"^[0-9T\-]+_[A-Z0-9]+\.json$")


@dataclass
class AnalysisRecord:
    """One past analysis, rehydrated from disk.

    Mirrors what the live pipeline produces: a ScoreReport, the events list,
    the coachings list, plus minimal video provenance. Everything needed to
    say "지난번보다 +3점, 같은 차간거리 문제 반복" without re-running anything.
    """
    analyzed_at: str           # ISO timestamp (local time)
    session_id: str
    video_name: str
    duration: float
    score: ScoreReport
    events: list[Event] = field(default_factory=list)
    coachings: list[Coaching] = field(default_factory=list)


# ─── Save ─────────────────────────────────────────────────────

def save_analysis(
    session_id: str,
    video_name: str,
    duration: float,
    score: ScoreReport,
    events: list[Event],
    coachings: list[Coaching],
) -> Path:
    """Write the current analysis to disk and return its path."""
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    now = datetime.now()
    ts = now.isoformat(timespec="seconds").replace(":", "-")
    path = HISTORY_DIR / f"{ts}_{session_id}.json"

    payload = {
        "analyzed_at": now.isoformat(timespec="seconds"),
        "session_id": session_id,
        "video_name": video_name,
        "duration": float(duration),
        "score": dataclasses.asdict(score),
        "events": [dataclasses.asdict(e) for e in events],
        "coachings": [dataclasses.asdict(c) for c in coachings],
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


# ─── Load ─────────────────────────────────────────────────────

def _rehydrate(payload: dict) -> AnalysisRecord:
    """JSON dict → AnalysisRecord with live dataclass instances inside."""
    score_d = payload["score"]
    score = ScoreReport(
        total=score_d["total"],
        grade=score_d["grade"],
        categories=[CategoryScore(**c) for c in score_d.get("categories", [])],
        focus_area=(CategoryScore(**score_d["focus_area"])
                    if score_d.get("focus_area") else None),
    )
    events = [Event(**e) for e in payload.get("events", [])]
    # Coaching has a nested Event — but for history comparison we don't need
    # the linkage to be the same object identity. Build a fresh Event for each.
    coachings = []
    for c in payload.get("coachings", []):
        ev_d = c.get("event") or {}
        coachings.append(Coaching(
            event=Event(**ev_d) if ev_d else None,  # type: ignore[arg-type]
            scene_description=c.get("scene_description", ""),
            scene_analysis=c.get("scene_analysis", ""),
            action_plan=c.get("action_plan", ""),
        ))
    return AnalysisRecord(
        analyzed_at=payload["analyzed_at"],
        session_id=payload["session_id"],
        video_name=payload.get("video_name", ""),
        duration=float(payload.get("duration", 0.0)),
        score=score,
        events=events,
        coachings=coachings,
    )


def _list_files() -> list[Path]:
    """All history JSON files sorted newest first.

    Corrupt or off-pattern files are skipped silently — history is for a
    nice-to-have feature, not the critical path.
    """
    if not HISTORY_DIR.exists():
        return []
    files = [p for p in HISTORY_DIR.iterdir()
             if p.is_file() and _FNAME_RE.match(p.name)]
    # Filename starts with an ISO timestamp, so lexicographic sort = chrono sort
    files.sort(key=lambda p: p.name, reverse=True)
    return files


def load_recent(limit: int = 10) -> list[AnalysisRecord]:
    """Return up to `limit` most-recent analyses, newest first."""
    out: list[AnalysisRecord] = []
    for p in _list_files()[:limit]:
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            out.append(_rehydrate(data))
        except (OSError, json.JSONDecodeError, KeyError, TypeError):
            continue
    return out


def delete_analysis(session_id: str) -> bool:
    """Remove every history file whose session_id matches. Returns True if at
    least one file was deleted. Used by the visible × on each history card —
    silently no-ops if the session is already gone."""
    if not session_id:
        return False
    removed = False
    for p in _list_files():
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if data.get("session_id") == session_id:
            try:
                p.unlink()
                removed = True
            except OSError:
                pass
    return removed


def load_prior(exclude_session_id: str | None = None) -> AnalysisRecord | None:
    """The most recent analysis, optionally skipping a given session id.

    Pass `exclude_session_id` from the live pipeline if you call this AFTER
    saving the current run — that way you get the actual previous one, not
    the just-saved current one. Returns None if no prior exists.
    """
    for p in _list_files():
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            if exclude_session_id and data.get("session_id") == exclude_session_id:
                continue
            return _rehydrate(data)
        except (OSError, json.JSONDecodeError, KeyError, TypeError):
            continue
    return None
