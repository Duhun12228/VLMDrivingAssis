# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run the app (Gradio UI at http://127.0.0.1:7865)
python app.py

# End-to-end pipeline smoke test (generates a synthetic video, runs all 5 stages)
python scripts/smoke_pipeline.py

# Install dependencies
pip install -r requirements.txt
```

## Architecture

### App state machine
`app.py` is a 4-state Gradio app: **IDLE → UPLOADED → ANALYZING → RESULTS**. Each state is a `gr.Group` toggled by visibility. State transitions are driven by:
- `file_in.upload` → `on_file_uploaded()` (IDLE → UPLOADED)
- `analyze_btn.click` → `go_analyzing()` then `run_analysis()` then `go_results()` (UPLOADED → ANALYZING → RESULTS)
- `home_btn` / `back_btn` / `new_analysis_btn` → `go_idle()` (any → IDLE)

Each non-IDLE screen is rendered as **one self-contained HTML blob** (e.g. `ready_screen_html()`, `analyzing_screen_html()`, `results_screen_html()`) returned into a single `gr.HTML` component. This is intentional — using `gr.Row`/`gr.Column` for layout caused Gradio's flex containers to break the custom CSS grids.

### Core pipeline (`run_analysis`)
```
detect_video() → extract_events() → generate_coaching() → calculate_score() → render_annotated_video()
```
All pipeline modules exchange data through the dataclasses defined in `core/schema.py` — this is the team's shared interface contract. Do not rename fields without team coordination.

### Mock vs real models
Two env vars gate real inference:
- `USE_REAL_YOLO=1` → enables `core/detector._detect_real_frame()` (currently `NotImplementedError`)
- `USE_REAL_VLM=1` → enables `core/vlm._generate_real_coaching()` (currently `NotImplementedError`)

Default (`=0`) uses deterministic mock data from `mock_data.py`. The mock trajectories and coaching texts are designed to trigger all four event types.

### Replacement points (team ownership)
- `core/detector._detect_real_frame()` — owner: 이지원. Replace with YOLO26n / RT-DETR. Must return `FrameDetections` with `cls` values from `core.schema.CLASS_NAMES`.
- `core/vlm._generate_real_coaching()` — owner: 김두훈. Replace with Qwen2.5-VL. Must return `Coaching` with `scene_description`, `scene_analysis`, `action_plan`.

### JS ↔ Gradio bridge (`DC_BOOT_JS`)
The visible custom `<button>` elements inside the HTML blobs cannot trigger Gradio events directly. `DC_BOOT_JS` (defined at the top of `app.py`) bridges them to hidden `gr.Button` instances via class selectors:
- `#ready-back-btn` → `.dc-ready-back-hit`
- `#ready-go-btn` → `.dc-ready-go-hit`
- `#results-again-btn` → `.dc-results-again-hit`
- `.dc-v3-root .brand` → `.dc-home-hit`

`bootDC()` is called on mount and re-called via `MutationObserver` after every Gradio DOM re-render, because Gradio replaces DOM nodes on state changes.

### CSS scoping
All styles from `ui/theme.py` (`CUSTOM_CSS`) are scoped under `.dc-v3-root`. The IDLE landing page, Ready, Analyzing, and Results screens each root their HTML in `<div class="dc-v3-root ...">`. Styles outside this class are Gradio's own.

### Video handling
Dashcam files are often HEVC or fragmented MP4 that browsers refuse to play. `core/video_utils.normalize_for_browser()` re-encodes any upload to H.264 / yuv420p / `+faststart` via `imageio-ffmpeg` (bundled) or system `ffmpeg`. The `render_annotated_video()` function does the same two-stage process: write raw frames with OpenCV (mp4v), then transcode to H.264.

Korean text on video frames is rendered via PIL (`_put_text_ko` in `core/overlay.py`) because `cv2.putText` only supports ASCII.

### Event extraction tuning
`core/event_extractor.py` contains named constants at the top (`_CLOSE_VEHICLE_AREA_RATIO`, `_EVENT_COOLDOWN_FRAMES`, etc.) — these are the primary knobs for adjusting event sensitivity without touching logic.

### Scoring
Each of the 5 categories (`signal`, `lane`, `pedestrian`, `speed`, `distance`) starts at 100 and loses `event.penalty` per violation, capped at `_MAX_CATEGORY_DROP = 40`. Grade thresholds: A ≥ 90, B ≥ 80, C ≥ 70, D < 70.

## Coding Guidelines

### Think before coding
State assumptions explicitly before implementing. If multiple interpretations exist, surface them — don't pick silently. If something is unclear, name what's confusing and ask rather than guessing.

### Simplicity first
Minimum code that solves the problem. No speculative features, abstractions for single-use code, or "flexibility" that wasn't requested. If 200 lines could be 50, rewrite it.

### Surgical changes
Touch only what is directly required. Don't "improve" adjacent code, comments, or formatting. Match existing style even if you'd do it differently. If unrelated dead code is noticed, mention it — don't delete it. Remove only imports/variables/functions that *your* changes made unused.

### Verify before declaring done
Transform tasks into verifiable goals before starting. For the pipeline, run `python scripts/smoke_pipeline.py` after any change to `core/`. For UI changes that affect the Gradio app, verify by running `python app.py` and exercising the affected state transition.
