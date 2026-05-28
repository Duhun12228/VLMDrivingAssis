"""DrivingAssis AI landing page — v3 editorial / cinematic.

The IDLE screen is a 7-section marketing page based on the v3 HTML mock
(DrivingAssis v3.html — real photos + SVG annotations):

    1. Fixed top nav (brand + primary CTA)
    2. Hero — split dual-frame (raw / AI-analyzed) + bottom stat strip
    3. Upload band — copy + bullets + custom dropzone (.dz)
    4. What we see — 3 capability tiles with photo + SVG overlay
    5. Sample report — timeline + 3 key moments + score footer
    6. Numbers — 4-tile proof strip
    7. CTA — fullbleed bg photo + glow headline
    8. Footer — 4-col links + bar

All v3 styles live under `.dc-v3-root` (see theme.py). The visible
`.dz` is just HTML; an `init` JS in app.py bridges its click/drop to
the hidden `gr.File` so Gradio still handles the actual upload.
"""
from __future__ import annotations


# ─── Shared bits ──────────────────────────────────────────────

def _arrow_svg() -> str:
    return ('<svg class="arrow" viewBox="0 0 12 12" fill="none" '
            'stroke="currentColor" stroke-width="1.6">'
            '<path d="M2 6h8M7 2l4 4-4 4"/></svg>')


_BRAND_SVG = (
    '<svg viewBox="0 0 32 32" fill="none">'
    '<path d="M2 8 L2 2 L8 2" stroke="#00E59A" stroke-width="1.6" stroke-linecap="square"/>'
    '<path d="M24 2 L30 2 L30 8" stroke="#00E59A" stroke-width="1.6" stroke-linecap="square"/>'
    '<path d="M30 24 L30 30 L24 30" stroke="#00E59A" stroke-width="1.6" stroke-linecap="square"/>'
    '<path d="M8 30 L2 30 L2 24" stroke="#00E59A" stroke-width="1.6" stroke-linecap="square"/>'
    '<path d="M6 28 L14.5 14" stroke="#00E59A" stroke-width="2" stroke-linecap="round"/>'
    '<path d="M26 28 L17.5 14" stroke="#00E59A" stroke-width="2" stroke-linecap="round"/>'
    '<path d="M16 28 L16 22" stroke="#00E59A" stroke-width="1.6" stroke-linecap="round"/>'
    '<path d="M16 19 L16 15.5" stroke="#00E59A" stroke-width="1.4" stroke-linecap="round" opacity="0.7"/>'
    '<circle cx="16" cy="13" r="1.6" fill="#00E59A"/>'
    '</svg>'
)


def _brand_html() -> str:
    """Shared brand mark — used in nav + footer."""
    return (
        '<a class="brand" href="#dc-top" aria-label="DrivingAssis">'
        f'<span class="brand-mark" aria-hidden="true">{_BRAND_SVG}</span>'
        '<span>DRIVING<span style="color:var(--signal)">ASSIS</span></span>'
        '</a>'
    )


# ─── 1. NAV ───────────────────────────────────────────────────

def _nav_html() -> str:
    arrow = _arrow_svg()
    return f"""
    <header class="nav" id="dc-nav">
      {_brand_html()}
      <div class="nav-actions">
        <a class="nav-link" id="dc-history-link" href="#">기록</a>
        <a class="btn btn-primary" href="#dc-upload">영상 업로드 {arrow}</a>
      </div>
    </header>
    """


# ─── 2. HERO — dual-frame ─────────────────────────────────────

def _hero_section() -> str:
    # Local hero.mp4 (in assets/) — served by Gradio via allowed_paths.
    # We use the gradio_api/file route which Gradio exposes for static files.
    hero_video = "/gradio_api/file=assets/hero.mp4"
    return f"""
    <section class="hero" id="dc-top">
      <div class="hero-top">
        <div>
          <div class="hero-eyebrow">
            <span class="label label-signal">A driving intelligence platform</span>
          </div>
          <h1 class="hero-title" id="dc-heroTitle">
            <span class="line"><span class="inner">주행을 다시 보다,</span></span>
            <span class="line"><span class="inner"><em class="accent">프레임 단위로.</em></span></span>
          </h1>
        </div>
        <p class="hero-sub" data-reveal style="--rd:500ms">
          블랙박스 영상을 올리면 DrivingAssis가 급제동·차선 이탈·차간거리 부족 같은
          위험 이벤트를 자동으로 찾아내고, 그 순간의 운전 습관을 한 페이지 리포트로 정리합니다.
        </p>
      </div>

      <div class="hero-stage" data-reveal style="--rd:200ms">
        <div class="frame frame-raw"><i></i>
          <span class="frame-tag mono">Raw footage</span>
          <span class="frame-tc">00:00:13:21</span>
          <video autoplay muted loop playsinline preload="auto"
                 aria-label="야간 주행 POV — 원본"
                 src="{hero_video}"></video>
        </div>

        <div class="frame frame-ai"><i></i>
          <span class="frame-tag mono">AI · DrivingAssis</span>
          <span class="frame-tc">00:00:13:21 · 24 fps</span>
          <video autoplay muted loop playsinline preload="auto"
                 aria-label="야간 주행 POV — AI 분석"
                 src="{hero_video}"></video>

          <svg class="ai-overlay" viewBox="0 0 1600 900" preserveAspectRatio="none">
            <defs>
              <radialGradient id="dcv3-attnGrad" cx="50%" cy="55%" r="35%">
                <stop offset="0%"   stop-color="rgba(0,229,154,0.30)"/>
                <stop offset="60%"  stop-color="rgba(0,229,154,0.08)"/>
                <stop offset="100%" stop-color="rgba(0,229,154,0)"/>
              </radialGradient>
            </defs>
            <ellipse class="attn" cx="800" cy="460" rx="480" ry="220"/>
          </svg>

          <div class="frame-ai-hud">
            <div class="hud-pill"><span class="dot"></span>LANE <b>STABLE</b></div>
            <div class="hud-pill">LEAD <b>14.2m</b></div>
            <div class="hud-pill risk"><span class="dot"></span>RISK <b>LOW</b></div>
          </div>
        </div>

        <div class="frame-divider" aria-hidden="true"></div>
      </div>

      <div class="hero-bottom">
        <div class="hero-stat" data-reveal style="--rd:600ms">
          <div class="label" style="margin-bottom:14px">01 · Detect</div>
          <div class="d" style="font-size:15px;color:rgba(255,255,255,0.86);max-width:32ch">
            급제동·차선 이탈·차간거리 부족 같은 위험 이벤트를 영상에서 자동으로 찾아냅니다.
          </div>
        </div>
        <div class="hero-stat" data-reveal style="--rd:720ms">
          <div class="label" style="margin-bottom:14px">02 · Contextualize</div>
          <div class="d" style="font-size:15px;color:rgba(255,255,255,0.86);max-width:32ch">
            사건 직전·직후의 운전 결정을 같이 봅니다. 결과만이 아니라 그 결정이 만들어진 순간을 함께.
          </div>
        </div>
        <div class="hero-stat" data-reveal style="--rd:840ms">
          <div class="label" style="margin-bottom:14px">03 · Coach</div>
          <div class="d" style="font-size:15px;color:rgba(255,255,255,0.86);max-width:32ch">
            반복되는 습관에 한 줄 피드백을 붙여, 다음 주행에서 무엇을 바꿔볼지 알려드립니다.
          </div>
        </div>
      </div>
    </section>
    """


# ─── 3. UPLOAD BAND — custom dropzone bridges to gr.File ─────

def _upload_section() -> str:
    arrow = _arrow_svg()
    return f"""
    <section class="upload" id="dc-upload">
      <div class="upload-grid">
        <div class="upload-copy">
          <span class="label label-signal">Step 01 — Upload</span>
          <h2>영상 한 편,<br/>리포트 한 장.</h2>
          <p>대시캠·블랙박스·휴대폰 어떤 영상이든 받습니다. 업로드된 영상은 안전하게
            처리되고, 분석이 끝나면 주요 이벤트·근거 클립·코칭이 한 페이지로 정리됩니다.</p>
          <ul class="upload-bullets">
            <li><span><b>MP4 · MOV · HEVC</b> 주요 블랙박스 포맷 그대로 올리면 됩니다.</span></li>
            <li><span><b>이벤트 자동 검출</b> 급제동·차선 이탈·차간거리 부족·신호 미준수 등.</span></li>
          </ul>
        </div>

        <div class="dz" id="dc-dropzone" tabindex="0" role="button"
             aria-label="주행 영상 업로드">
          <div class="dz-head">
            <span>upload · drag &amp; drop</span>
            <span class="dz-status"><i class="dot"></i>READY</span>
          </div>
          <div class="dz-body dz-idle">
            <div class="dz-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"
                   stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 16V4"/><path d="M6 10l6-6 6 6"/><path d="M4 20h16"/>
              </svg>
            </div>
            <h3 id="dc-dz-title">여기에 블랙박스 영상을 끌어다 놓으세요</h3>
            <div class="dz-meta en" id="dc-dz-meta">또는 파일 선택 · MP4 · MOV · HEVC</div>
            <div class="dz-cta">
              <span class="btn btn-primary">파일 선택하기 {arrow}</span>
              <span class="btn btn-ghost">샘플 영상으로 체험</span>
            </div>
          </div>
        </div>
      </div>
    </section>
    """


# ─── 4. WHAT WE SEE — 3 capability tiles ──────────────────────

def _see_section() -> str:
    return """
    <section class="see" id="dc-see">
      <div class="see-head">
        <div>
          <span class="label label-signal">What we see</span>
          <h2 data-reveal>모델은 단순한 객체 검출이 아닙니다.<br/><em>맥락을 봅니다.</em></h2>
        </div>
        <p data-reveal style="--rd:200ms">
          한 장의 프레임에서 차선·차량·보행자·표지판을 분리해내고, 30초 윈도우 안에서
          그것들이 만들어내는 의사결정의 결을 추적합니다.
        </p>
      </div>

      <div class="see-grid">
        <article class="tile" data-reveal>
          <img alt="스티어링 POV — 운전자 조작 추적"
            src="https://images.unsplash.com/photo-1449965408869-eaa3f722e40d?auto=format&fit=crop&w=1600&q=80"/>
          <div class="tile-overlay">
            <svg viewBox="0 0 400 500" preserveAspectRatio="none">
              <rect class="bbox" x="120" y="260" width="170" height="110"/>
              <text x="120" y="254">HANDS · 0.96</text>
              <rect class="bbox amber" x="240" y="180" width="60" height="40"/>
              <text x="240" y="174" style="fill:var(--amber)">GAZE · FORWARD</text>
            </svg>
          </div>
          <div class="tile-shade"></div>
          <div class="tile-body">
            <div class="tile-num">CAPABILITY · 01</div>
            <h3>운전자의 시선과 조작을 함께 본다</h3>
            <p>스티어링 입력의 미세한 진동·시선 방향·페달 압력을 시간축에 정렬합니다.</p>
          </div>
        </article>

        <article class="tile" data-reveal style="--rd:120ms">
          <img alt="앞차 추적 — 전방 차량 검출"
            src="https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=1600&q=80"/>
          <div class="tile-overlay">
            <svg viewBox="0 0 400 500" preserveAspectRatio="none">
              <rect class="bbox" x="110" y="230" width="190" height="130"/>
              <text x="110" y="224">VEHICLE · 0.98 · 14.2m</text>
              <path class="lane" d="M40,500 C120,380 180,300 200,240" style="stroke-dasharray:8 6"/>
              <path class="lane" d="M380,500 C320,380 240,300 220,240" style="stroke-dasharray:8 6"/>
            </svg>
          </div>
          <div class="tile-shade"></div>
          <div class="tile-body">
            <div class="tile-num">CAPABILITY · 02</div>
            <h3>앞차와의 거리·상대 속도를 본다</h3>
            <p>전방 차량을 프레임마다 추적해 차간거리·상대 가감속을 0.1초 단위로 계산합니다.</p>
          </div>
        </article>

        <article class="tile" data-reveal style="--rd:240ms">
          <img alt="차선·도로 인지 — 다양한 환경"
            src="https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?auto=format&fit=crop&w=1600&q=80"/>
          <div class="tile-overlay">
            <svg viewBox="0 0 400 500" preserveAspectRatio="none">
              <path class="lane" d="M50,500 C140,360 200,270 215,200"/>
              <path class="lane" d="M350,500 C280,360 230,270 225,200"/>
              <ellipse cx="220" cy="260" rx="140" ry="60"
                style="fill:rgba(0,229,154,0.08); stroke:none"/>
              <text x="160" y="195">LANE · STABLE</text>
            </svg>
          </div>
          <div class="tile-shade"></div>
          <div class="tile-body">
            <div class="tile-num">CAPABILITY · 03</div>
            <h3>차선과 도로 형상을 끊김 없이 인지한다</h3>
            <p>차선 마킹이 흐릿하거나 비대칭인 환경에서도 도로 형상을 안정적으로 추정합니다.</p>
          </div>
        </article>
      </div>
    </section>
    """


# ─── 5. SAMPLE REPORT ─────────────────────────────────────────

def _report_section() -> str:
    arrow = _arrow_svg()
    return f"""
    <section class="report" id="dc-report">
      <div class="report-head">
        <div>
          <span class="label label-signal">What you get</span>
          <h2 data-reveal>당신이 받는 한 페이지<br/>분석 리포트.</h2>
        </div>
        <p data-reveal style="--rd:200ms">
          검출된 위험 이벤트, 그 순간의 근거 클립, 그리고 다음 주행에서 바꿔볼 수 있는
          짧은 코칭이 한 페이지로 정리됩니다.
        </p>
      </div>

      <div class="report-card" data-reveal>
        <div class="rc-head">
          <div class="rc-head-left">
            <span class="rc-id">REPORT · #DA-20260524-2419</span>
          </div>
          <div class="rc-head-right">
            <span>DURATION <b>12:34</b></span>
            <span>EVENTS <b>3</b></span>
            <span>SCORE <b style="color:var(--signal)">82</b></span>
          </div>
        </div>

        <div class="rc-timeline">
          <div class="rc-timeline-label">
            <h4>Timeline · 검출된 의사결정</h4>
            <div class="rc-tl-ticks" style="width:280px">
              <span>00:00</span><span>06:17</span><span>12:34</span>
            </div>
          </div>
          <div class="rc-tl">
            <div class="rc-tl-bar" style="left:0; width:18%"></div>
            <div class="rc-tl-bar" style="left:32%; width:14%"></div>
            <div class="rc-tl-bar" style="left:64%; width:22%"></div>
            <div class="rc-tl-marker" data-l="02:14 · LANE CHANGE" style="left:18%"></div>
            <div class="rc-tl-marker amber" data-l="06:47 · CLOSE GAP" style="left:46%"></div>
            <div class="rc-tl-marker risk" data-l="10:32 · LATE BRAKE" style="left:78%"></div>
          </div>
        </div>

        <div class="rc-moments">
          <article class="km">
            <div class="km-img">
              <img alt="02:14 차선 변경"
                src="https://images.unsplash.com/photo-1449965408869-eaa3f722e40d?auto=format&fit=crop&w=900&q=80"/>
              <svg class="km-overlay" viewBox="0 0 400 225" preserveAspectRatio="none">
                <rect x="168" y="96" width="108" height="70"/>
                <text x="168" y="90">HANDS · 0.96</text>
                <rect x="220" y="50" width="56" height="30"/>
                <text x="220" y="44">GAZE · FWD</text>
              </svg>
              <span class="km-tc mono">02:14</span>
              <span class="km-badge mono">GOOD</span>
            </div>
            <div class="km-cat">LANE CHANGE · LEFT</div>
            <h4>충분한 거리에서 한 번에 들어갔습니다.</h4>
            <p>차선 변경 1.6초 전부터 사이드미러를 확인했고, 깜빡이를 1.2초 유지한 뒤 진입했습니다.</p>
            <div class="km-coach"><b>코칭</b><span>같은 패턴을 야간에도 유지해 보세요. 평균 1.4초 → 1.6초로 안정적.</span></div>
          </article>

          <article class="km">
            <div class="km-img">
              <img alt="06:47 차간거리"
                src="https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=900&q=80"/>
              <svg class="km-overlay" viewBox="0 0 400 225" preserveAspectRatio="none">
                <rect class="amber" x="130" y="94" width="140" height="82"/>
                <text class="amber" x="130" y="88">VEHICLE · 1.4s</text>
                <rect class="amber" x="300" y="180" width="70" height="22"/>
                <text class="amber" x="308" y="194">GAP · LOW</text>
              </svg>
              <span class="km-tc mono">06:47</span>
              <span class="km-badge amber mono">REVIEW</span>
            </div>
            <div class="km-cat">FOLLOWING DISTANCE</div>
            <h4>앞차와의 간격이 1.4초로 좁아졌습니다.</h4>
            <p>고속도로 권장 간격은 2.0초입니다. 차간거리 부족 상태가 9초간 지속됐습니다.</p>
            <div class="km-coach"><b>코칭</b><span>오른발을 액셀에서 떼는 것만으로 0.6초가 다시 확보됩니다.</span></div>
          </article>

          <article class="km">
            <div class="km-img">
              <img alt="10:32 급제동"
                src="https://images.unsplash.com/photo-1485463611174-f302f6a5c1c9?auto=format&fit=crop&w=900&q=80"/>
              <svg class="km-overlay" viewBox="0 0 400 225" preserveAspectRatio="none">
                <rect class="risk" x="150" y="86" width="120" height="92"/>
                <text class="risk" x="150" y="80">VEHICLE · BRAKE</text>
                <rect class="risk" x="280" y="180" width="80" height="22"/>
                <text class="risk" x="288" y="194">DECEL · -0.42g</text>
              </svg>
              <span class="km-tc mono">10:32</span>
              <span class="km-badge risk mono">RISK</span>
            </div>
            <div class="km-cat">LATE BRAKING</div>
            <h4>0.7초 늦은 제동, –0.42g.</h4>
            <p>30초 전 앞 차량의 브레이크등이 두 번 점멸했지만 페달 입력은 7초 뒤에 시작됐습니다.</p>
            <div class="km-coach"><b>코칭</b><span>앞차의 두 번째 브레이크등이 곧 제동의 신호입니다. 미리 시선을 두세요.</span></div>
          </article>
        </div>

        <div class="rc-foot">
          <div class="rc-score">
            <div class="rc-score-item"><div class="l">OVERALL</div><div class="v signal">82<small>/100</small></div></div>
            <div class="rc-score-item"><div class="l">ATTENTION</div><div class="v">88<small>/100</small></div></div>
            <div class="rc-score-item"><div class="l">SPACING</div><div class="v">72<small>/100</small></div></div>
            <div class="rc-score-item"><div class="l">SMOOTHNESS</div><div class="v">79<small>/100</small></div></div>
          </div>
          <a class="btn btn-ghost" href="#dc-upload">내 영상으로 받아보기 {arrow}</a>
        </div>
      </div>
    </section>
    """


# ─── 6. NUMBERS ───────────────────────────────────────────────

def _numbers_section() -> str:
    big = ("font-size:clamp(30px,3.2vw,44px);"
           "line-height:1.05;letter-spacing:-0.025em")
    return f"""
    <section class="numbers" id="dc-numbers">
      <div class="numbers-head">
        <span class="label label-signal">What we detect</span>
        <h2 data-reveal>리포트가 짚어주는<br/><em>세 가지 순간.</em></h2>
      </div>
      <div class="numbers-grid">
        <div class="num" data-reveal>
          <div class="l">Event · 01</div>
          <div class="v" style="{big}">차선 이탈</div>
          <div class="d">방향지시등 없이 차선을 넘어가거나, 차선 안에서 좌우 흔들림이 큰 구간을 표시합니다.</div>
        </div>
        <div class="num" data-reveal style="--rd:120ms">
          <div class="l">Event · 02</div>
          <div class="v" style="{big}">차간거리 부족</div>
          <div class="d">앞 차량과의 시간 간격이 권장 수준 아래로 떨어져 지속된 구간을 따로 모아 보여드립니다.</div>
        </div>
        <div class="num" data-reveal style="--rd:240ms">
          <div class="l">Event · 03</div>
          <div class="v" style="{big}">신호·정지선</div>
          <div class="d">신호 전환 시점의 정지·통과 결정과 정지선 위치를 함께 기록합니다.</div>
        </div>
      </div>
    </section>
    """


# ─── 7. CTA ───────────────────────────────────────────────────

def _cta_section() -> str:
    arrow = _arrow_svg()
    return f"""
    <section class="cta" id="dc-cta">
      <div class="cta-overlay"></div>
      <div class="cta-inner">
        <div>
          <span class="label label-signal">Try it now</span>
          <h2>지난 주행이,<br/>다음 주행의<br/><span class="glow">코칭이 됩니다.</span></h2>
        </div>
        <div class="cta-side">
          <p>블랙박스 영상 한 편이면 충분합니다. 위험 이벤트와 근거 클립, 그리고
             다음 주행에서 바꿔볼 한 줄을 정리해 돌려드립니다.</p>
          <div class="cta-actions">
            <a class="btn btn-primary btn-lg" href="#dc-upload">영상 업로드 시작 {arrow}</a>
            <a class="btn btn-ghost btn-lg" href="#dc-report">샘플 리포트 보기</a>
          </div>
          <div class="cta-fine">No setup · No hardware · Early access</div>
        </div>
      </div>
    </section>
    """


# ─── 8. FOOTER ────────────────────────────────────────────────

def _footer_section() -> str:
    return f"""
    <footer class="footer-min" id="dc-footer">
      {_brand_html()}
      <p class="foot-tag">블랙박스 영상 한 편을 한 페이지 리포트로 바꾸는 운전 코칭 프로젝트.</p>
      <div class="foot-mini mono">© 2026 DRIVINGASSIS</div>
    </footer>
    """


# ─── Top-level IDLE HTML (assembled) ──────────────────────────

def _font_links() -> str:
    """Emit <link> tags for the v3 fonts.

    We cannot use `@import` inside CUSTOM_CSS because Gradio injects styles
    via `CSSStyleSheet.replaceSync()` which forbids @import directives. So
    we inline the <link> tags at the top of the idle HTML — gr.HTML appends
    them to the document and the browser fetches the fonts normally.
    """
    return (
        '<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link rel="stylesheet" '
        'href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/'
        'dist/web/variable/pretendardvariable-dynamic-subset.min.css">'
        '<link rel="stylesheet" '
        'href="https://fonts.googleapis.com/css2'
        '?family=Inter:wght@400;500;600;700'
        '&family=JetBrains+Mono:wght@400;500;600'
        '&family=Noto+Sans+KR:wght@400;500;600;700;800;900'
        '&display=swap">'
    )


def idle_hero_html() -> str:
    """The whole v3 landing page, wrapped in `.dc-v3-root` for CSS scoping."""
    return (
        _font_links()
        + '<div class="dc-v3-root">'
        + _nav_html()
        + _hero_section()
        + _upload_section()
        + _see_section()
        + _report_section()
        + _numbers_section()
        + _cta_section()
        + _footer_section()
        + '</div>'
    )


# ─── UPLOADED — v4 "Ready" screen ──────────────────────────────
# Built as a SINGLE HTML blob (not split across multiple gr.HTML + gr.Row).
# Reason: when we used gr.Row/gr.Column to lay out nav / stepper / stage /
# action bar, Gradio's own flex containers fought our CSS grid and the
# stepper collapsed to a vertical stack, the rail vanished, etc. The IDLE
# landing works because it's a single self-contained `.dc-v3-root` div —
# we use the same pattern here.
#
# Custom <button> elements inside the HTML are bridged by JS in app.py
# to the hidden gr.Button instances (see `.dc-hidden-actions`).

import urllib.parse


def _fmt_size(bytes_: int | float) -> str:
    n = float(bytes_)
    if n <= 0:
        return "—"
    units = ["B", "KB", "MB", "GB"]
    i = 0
    while n >= 1024 and i < len(units) - 1:
        n /= 1024
        i += 1
    return f"{n:.1f} {units[i]}"


def _fmt_duration(sec: float) -> str:
    if sec <= 0:
        return "00:00"
    m, s = divmod(int(sec), 60)
    return f"{m:02d}:{s:02d}"


def _video_url(abs_path: str) -> str:
    """Build the /gradio_api/file= URL for a path inside `allowed_paths`."""
    if not abs_path:
        return ""
    return "/gradio_api/file=" + urllib.parse.quote(
        abs_path.replace("\\", "/"), safe="/:."
    )


def _file_icon_svg() -> str:
    return (
        '<svg class="file-icon" width="14" height="14" viewBox="0 0 24 24"'
        ' fill="none" stroke="currentColor" stroke-width="1.6">'
        '<rect x="3" y="6" width="14" height="12" rx="1"/>'
        '<path d="M17 10 L21 8 L21 16 L17 14 Z" fill="currentColor"/>'
        '</svg>'
    )


def _arrow_go_svg() -> str:
    return (
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"'
        ' stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M5 12 L19 12 M13 6 L19 12 L13 18"/></svg>'
    )


def ready_screen_html(
    video_path: str = "",
    name: str = "",
    duration: float = 0.0,
    width: int = 0,
    height: int = 0,
    fps: float = 0.0,
    codec: str = "—",
    size_bytes: int = 0,
    session_id: str = "—",
) -> str:
    """Full v4 Ready screen — nav · stepper · stage · action bar · footer.

    All wrapped in one `.dc-v3-root.ready-root` so Gradio's component
    containers can't break the internal grid layout.
    """
    dur_str = _fmt_duration(duration)
    size_str = _fmt_size(size_bytes)
    res_str = f"{width}×{height}" if width and height else "—"
    fps_str = f"{fps:.0f} FPS" if fps > 0 else "—"
    if duration > 0 and size_bytes > 0:
        bitrate_str = f"{(size_bytes * 8 / duration) / 1e6:.1f} Mb/s"
    else:
        bitrate_str = "—"
    safe_name = name or "—"
    meta_line = f"방금 · {size_str}" if size_bytes > 0 else "준비 중"
    vurl = _video_url(video_path)
    video_el = (
        f'<video src="{vurl}" controls preload="metadata" playsinline></video>'
        if vurl else
        '<div class="ready-video-empty">영상 미리보기를 준비 중입니다…</div>'
    )

    return f"""
<div class="dc-v3-root ready-root">

  <nav class="ready-nav">
    <a class="brand" href="#dc-top" aria-label="DrivingAssis">
      <span class="brand-mark" aria-hidden="true">{_BRAND_SVG}</span>
      <span>DRIVING<span style="color:var(--signal)">ASSIS</span></span>
    </a>
    <div class="ready-nav-right">
      <span class="ready-session">SESSION · {session_id}</span>
    </div>
  </nav>

  <div class="ready-stepper-wrap">
    <div class="ready-stepper" role="list">
      <div class="ready-step done" role="listitem">
        <span class="num">01</span><span class="check">✓</span><span>업로드</span>
      </div>
      <div class="ready-step current" role="listitem">
        <span class="num">02</span><span class="pulse" aria-hidden="true"></span><span>검토</span>
      </div>
      <div class="ready-step" role="listitem">
        <span class="num">03</span><span>분석</span>
      </div>
      <div class="ready-step" role="listitem">
        <span class="num">04</span><span>리포트</span>
      </div>
    </div>
  </div>

  <section class="ready-stage">
    <div class="ready-rail">
      <div class="ready-rail-status">
        <span class="dot"></span>
        <span class="label label-signal">Ready · 검토 중</span>
      </div>
      <h1>
        <span>{dur_str}.</span><br/>
        <span class="accent">이 영상.</span>
        <span class="em">받았습니다. 한 프레임도 빠짐없이 분석해 드릴 준비가 되었습니다.</span>
      </h1>
      <div class="ready-filename">
        {_file_icon_svg()}
        <div>
          {safe_name}
          <span class="file-meta">{meta_line}</span>
        </div>
      </div>
    </div>

    <div class="ready-video-stage">
      <div class="ready-video-frame">
        {video_el}
        <span class="ready-br ready-br-tl"></span>
        <span class="ready-br ready-br-tr"></span>
        <span class="ready-br ready-br-bl"></span>
        <span class="ready-br ready-br-br"></span>
        <div class="ready-hud ready-hud-tl">
          <span class="ready-hud-tag"><span class="ready-rec-dot"></span>REC · CH1</span>
        </div>
        <div class="ready-hud ready-hud-tr">
          <span class="ready-hud-tag">{res_str} · {fps_str}</span>
        </div>
      </div>
      <div class="ready-meta-strip">
        <div class="ready-meta-cell"><span class="k">Duration</span><span class="v">{dur_str}</span></div>
        <div class="ready-meta-cell"><span class="k">Resolution</span><span class="v">{res_str}</span></div>
        <div class="ready-meta-cell"><span class="k">Frame rate</span><span class="v">{fps_str}</span></div>
        <div class="ready-meta-cell"><span class="k">Codec</span><span class="v">{codec} <span class="ok">✓</span></span></div>
        <div class="ready-meta-cell"><span class="k">Bitrate</span><span class="v">{bitrate_str}</span></div>
        <div class="ready-meta-cell"><span class="k">Size</span><span class="v">{size_str}</span></div>
      </div>
    </div>
  </section>

  <section class="ready-action-wrap">
    <div class="ready-action-bar">
      <div class="ready-action-summary">
        <div class="lbl">Ready to analyze</div>
        <div class="ttl">위 영상으로 분석을 시작합니다.</div>
      </div>
      <button class="ready-btn-secondary" type="button" id="ready-back-btn">다른 영상으로</button>
      <button class="ready-btn-go" type="button" id="ready-go-btn">
        분석 시작 {_arrow_go_svg()}
        <span class="go-eta">약 30초</span>
      </button>
    </div>
    <div class="ready-kbd-hint">
      <span class="kbd">⏎</span> Enter 키로 즉시 시작
    </div>
  </section>

  <footer class="ready-foot">© 2026 DRIVINGASSIS · 분석 세션 {session_id}</footer>

</div>
"""


# ─── ANALYZING — v5 redesign ──────────────────────────────────
# Soul of the screen: the LIVE FRAME with real bboxes burned in (or SVG-
# overlaid from FrameDetections). Everything else (% / ETA / counters /
# stepper) is small mono chrome. The phase-driven H1 changes verb with
# each stage of the pipeline:
#   detect → 보고 / events → 추리고 / vlm → 쓰고 / score → 계산 / render → 만들고
# All values come from real run_analysis generator yields; no faked client
# animation. The screen is one self-contained .dc-v3-root blob (no gr.Row).

# Ordered phase definitions — drives stepper / phase list / H1 narrative.
_ANALYZ_PHASE_DEFS = [
    # (key, stepper_short, list_full,  h1_pre,        h1_verb,                  nav_label)
    ("detect", "검출",       "객체 검출",    "프레임을",     "보고 있습니다.",            "DETECT"),
    ("events", "이벤트",     "이벤트 추출",  "위험 구간을",   "추리고 있습니다.",          "EVENTS"),
    ("vlm",    "코칭",       "코칭 작성",    "코칭 문장을",   "쓰고 있습니다.",            "VLM"),
    ("score",  "점수",       "점수 산정",    "점수를",       "계산하고 있습니다.",        "SCORE"),
    ("render", "출력",       "영상 출력",    "주석 영상을",   "만들고 있습니다.",          "RENDER"),
]


def _phase_index(phase: str) -> int:
    for i, (key, *_rest) in enumerate(_ANALYZ_PHASE_DEFS):
        if key == phase:
            return i
    return 0


def _stepper_html(phase: str) -> str:
    idx = _phase_index(phase)
    out = []
    for i, (key, short, *_rest) in enumerate(_ANALYZ_PHASE_DEFS):
        cls = "current" if i == idx else ("done" if i < idx else "")
        pulse = '<span class="pulse"></span>' if i == idx else ""
        out.append(
            f'<div class="analyz-step {cls}" data-phase="{key}">'
            f'<span class="num">{i + 1:02d}</span>{pulse}'
            f'<span>{short}</span>'
            f'</div>'
        )
    return "".join(out)


def _phase_list_html(phase: str) -> str:
    idx = _phase_index(phase)
    out = []
    for i, (key, _short, full, *_rest) in enumerate(_ANALYZ_PHASE_DEFS):
        if i < idx:
            cls, status = "done", "완료"
        elif i == idx:
            cls, status = "current", "진행 중"
        else:
            cls, status = "pending", "대기"
        out.append(
            f'<li class="{cls}" data-phase="{key}">'
            f'<span class="num">{i + 1:02d}</span>'
            f'<span class="name">{full}</span>'
            f'<span class="stt">{status}</span>'
            f'</li>'
        )
    return "".join(out)


# Class → severity mapping for the live bbox overlay. Matches the counter
# strip color language: vehicles/pedestrians = signal, two-wheeled = amber,
# traffic markers stay muted (default signal). Risk tone is reserved for
# bboxes inside a flagged event region (not detected here per-frame).
_BBOX_CLS_TIER = {
    "car": "signal", "truck": "signal", "bus": "signal",
    "person": "signal",
    "bike": "amber", "motor": "amber", "rider": "amber",
    "traffic light": "signal", "traffic sign": "signal",
}


def _bbox_overlay_svg(det, frame_w: int, frame_h: int) -> str:
    """Live bbox layer over the static poster. Uses the latest FrameDetections
    object so the boxes sync exactly with what the model just emitted.
    Returns empty string when there are no detections to draw."""
    if not det or not det.detections or frame_w <= 0 or frame_h <= 0:
        return ""
    # Label box geometry — sized to fit "VEHICLE 0.94" at 9px mono
    LABEL_H = max(14, int(frame_h * 0.020))
    parts = []
    for d in det.detections[:12]:  # cap so the frame never looks like graffiti
        x1, y1, x2, y2 = d.bbox
        w = max(0, x2 - x1)
        h = max(0, y2 - y1)
        if w < 4 or h < 4:
            continue
        tier = _BBOX_CLS_TIER.get(d.cls, "signal")
        cls_extra = "" if tier == "signal" else f" {tier}"
        label = f"{d.cls.upper()} {d.confidence:.2f}"
        # Label background bar sits just above the bbox top edge
        label_w = min(int(w), max(60, len(label) * 7))
        label_y = max(0, y1 - LABEL_H - 2)
        text_cls = "dark" if tier == "signal" else "amber-dark"
        parts.append(
            f'<rect class="{tier}" x="{x1}" y="{y1}" width="{w}" height="{h}"/>'
            f'<rect class="label-bg{cls_extra}" x="{x1}" y="{label_y}" '
            f'width="{label_w}" height="{LABEL_H}"/>'
            f'<text class="{text_cls}" x="{x1 + 5}" y="{label_y + LABEL_H - 4}">{label}</text>'
        )
    if not parts:
        return ""
    return (f'<svg class="svg-overlay" viewBox="0 0 {frame_w} {frame_h}" '
            f'preserveAspectRatio="none">{"".join(parts)}</svg>')


def analyzing_screen_html(
    poster_path: str = "",
    name: str = "",
    session_id: str = "—",
    pct: int = 0,
    frame_idx: int = 0,
    total_frames: int = 0,
    proc_fps: float = 0.0,
    eta_sec: int = 0,
    veh: int = 0,
    ped: int = 0,
    two: int = 0,
    risk: int = 0,
    phase: str = "detect",
    det=None,
    frame_w: int = 0,
    frame_h: int = 0,
) -> str:
    """Live-analysis screen — v5 redesign.

    Every number here (pct, frame counter, processing fps, ETA, cumulative
    per-class detection counts, phase) reflects the actual run_analysis
    generator's state at the moment of yield. The right-side frame shows a
    poster jpg that the server periodically overwrites with the most-recent
    processed frame; on top of it, an SVG overlay draws bboxes from the
    latest FrameDetections (passed via `det`). No fake client animation.

    Counter labels read 차량·보행자·이륜차·위험 ··· but the numbers are
    cumulative across processed frames (vs the previous per-frame snapshot).
    With no tracker present this overstates unique objects, so labels are
    framed as "검출된 N건" rather than "고유 차량 N대".
    """
    safe_name = name or "—"
    idx = _phase_index(phase)
    _, _short, _full, h1_pre, h1_verb, nav_label = _ANALYZ_PHASE_DEFS[idx]
    pct = max(0, min(100, int(pct)))
    eta_str = f"약 {eta_sec}초" if eta_sec > 0 else "마무리"
    frame_str = f"{frame_idx:,} / {total_frames:,}" if total_frames else f"{frame_idx:,}"
    det_now = veh + ped + two

    poster_url = _video_url(poster_path)
    poster_el = (
        f'<img class="poster" src="{poster_url}" alt="현재 처리 중인 프레임"/>'
        if poster_url else
        '<div class="poster poster-empty"></div>'
    )
    bbox_svg = _bbox_overlay_svg(det, frame_w, frame_h)

    return f"""
<div class="dc-v3-root analyz-root">

  <nav class="analyz-nav">
    <a class="analyz-brand" href="#dc-top" aria-label="DrivingAssis">
      <span class="mark" aria-hidden="true">{_BRAND_SVG}</span>
      <span>DRIVING<span class="accent">ASSIS</span></span>
    </a>
    <div class="analyz-nav-right">
      <span class="live-pill"><span class="dot"></span>LIVE · {nav_label}</span>
      <span>SESSION · {session_id}</span>
      <button class="analyz-cancel" type="button" id="analyz-cancel-btn">분석 중단</button>
    </div>
  </nav>

  <div class="analyz-stepper">
    {_stepper_html(phase)}
  </div>

  <section class="analyz-stage">

    <aside class="analyz-rail">
      <div>
        <span class="phase-kicker">PHASE {idx + 1:02d} <span class="of">/ 05</span></span>
        <h1 class="analyz-h1">
          <span>{h1_pre}</span>
          <em>{h1_verb}</em>
        </h1>
        <div class="analyz-filename">
          {_file_icon_svg()}
          <span>{safe_name}</span>
        </div>
      </div>

      <div class="analyz-progress">
        <div class="row">
          <span class="pct">{pct}<span class="unit">%</span></span>
          <span class="eta">남은 시간 · <b>{eta_str}</b></span>
        </div>
        <div class="bar"><div class="fill" style="width:{pct}%"></div></div>
        <div class="meta">
          <span>프레임 · <b>{frame_str}</b></span>
          <span><b>{proc_fps:.0f}</b> f/s</span>
        </div>
      </div>

      <ul class="analyz-phases">
        {_phase_list_html(phase)}
      </ul>
    </aside>

    <div class="analyz-frame">
      {poster_el}
      {bbox_svg}

      <span class="br br-tl"></span>
      <span class="br br-tr"></span>
      <span class="br br-bl"></span>
      <span class="br br-br"></span>

      <div class="hud hud-tl">
        <span class="hud-chip"><span class="dot"></span>ANALYZING · CH1</span>
      </div>
      <div class="hud hud-tr">
        <span class="hud-chip">FRAME {frame_str}</span>
      </div>
      <div class="hud hud-bl">
        <span class="hud-chip">PHASE · <span class="accent">{nav_label}</span></span>
      </div>
      <div class="hud hud-br">
        <span class="hud-chip">DET <span class="accent">{det_now}</span></span>
      </div>
    </div>
  </section>

  <div class="analyz-counters">
    <div class="analyz-counter signal"><span class="k">차량 · Vehicle</span><span class="v">{veh}</span></div>
    <div class="analyz-counter"      ><span class="k">보행자 · Pedestrian</span><span class="v">{ped}</span></div>
    <div class="analyz-counter amber"><span class="k">이륜차 · Two-wheeled</span><span class="v">{two}</span></div>
    <div class="analyz-counter risk" ><span class="k">위험 이벤트 · Risk</span><span class="v">{risk}</span></div>
  </div>

</div>
"""


# ─── RESULTS — v4 cinematic finale ────────────────────────────
# Score becomes a sentence, key moments become evidence cards, annotated
# video sits below as proof. All in one self-contained .dc-v3-root blob —
# same pattern as Ready / Analyzing. The "또 다른 주행" custom button is
# bridged by JS to a hidden gr.Button.

def _score_comment(score) -> str:
    """One-line emotional comment shown next to the big score number.
    Bracket thresholds chosen so the user feels rewarded above 80 and
    challenged below 70 — the rough A/B/C/D bands of the existing scorer."""
    if not score:
        return ""
    s = score.total
    if s >= 90:
        return "정말 안정적이었어요"
    if s >= 80:
        return "대체로 안정적이었지만 아쉬운 순간이 있었어요"
    if s >= 70:
        return "몇 가지 주의할 점이 발견되었어요"
    return "개선이 필요한 구간이 많았어요"


def _category_tier(s: int) -> str:
    """Return the tier class for a category score — drives the bar color.
    Brackets match the visual / verbal language of _score_comment."""
    if s >= 85:
        return "tier-good"
    if s >= 70:
        return "tier-warn"
    return "tier-bad"


def _count_by_category(events) -> dict[str, int]:
    """Tally event counts keyed by score-category short key (e.g. 'distance').
    Used to detect repeated patterns across runs."""
    out: dict[str, int] = {}
    for e in events or []:
        out[e.category] = out.get(e.category, 0) + 1
    return out


# Korean label (CategoryScore.name_ko) → short key (Event.category).
# Built lazily once so we can look events up by the focus area's Korean name.
def _name_ko_to_key() -> dict[str, str]:
    from core.schema import SCORE_CATEGORY_DEFS
    return {ko: key for key, _en, ko, _icon in SCORE_CATEGORY_DEFS}


def _hero_sentence(score, events, prior=None) -> tuple[str, str]:
    """Returns (hero_html, secondary_text) — 2-line natural language summary
    of the drive. The hero may contain a single <em> tag for emphasis.

    When `prior` (a previous AnalysisRecord) is provided, the voice shifts
    from one-shot scorecard ("오늘 주행, 정말 안정적이었어요") to a coach who
    remembers ("지난번에 얘기한 차간거리, 이번엔 좋아졌어요"). The repeated-
    focus-area case is the killer moment — that's the line TMAP can't say.
    """
    if not score:
        return ("분석이 완료되었어요.", "결과를 정리하고 있어요.")

    overall = score.total
    focus = score.focus_area  # CategoryScore | None — the weakest category
    n_total = len(events) if events else 0
    n_risk    = sum(1 for e in (events or []) if e.severity == "danger")
    n_caution = sum(1 for e in (events or []) if e.severity == "caution")

    if prior is not None:
        return _hero_with_history(score, events, prior,
                                  overall, focus, n_total, n_risk, n_caution)

    # ─── First analysis ever — no prior to compare against ───
    if overall >= 88 and n_risk == 0:
        hero = "오늘 주행, <em>정말 안정적</em>이었어요."
    elif overall >= 75:
        if focus:
            hero = f"평균 이상이지만,<br/><em>{focus.name_ko}</em>에서 살짝 아쉬웠어요."
        else:
            hero = "평균 이상으로 <em>안정적인 주행</em>이었어요."
    elif overall >= 60:
        if focus:
            hero = (f"몇 군데 주의가 필요했어요.<br/>"
                    f"특히 <em>{focus.name_ko}</em>를 다음에 신경 써 보세요.")
        else:
            hero = "조금 더 안정적으로 갈 수 있을 것 같아요."
    else:
        if focus:
            hero = (f"다음 주행에서 바꿀 것이 있어요.<br/>"
                    f"<em>{focus.name_ko}</em>가 오늘의 가장 큰 이슈예요.")
        else:
            hero = "오늘은 평소보다 <em>거친 주행</em>이었어요."

    # First analysis — set the expectation that comparison starts next time
    if n_total == 0:
        secondary = "큰 위험 없이 부드럽게 흘러갔어요. 다음 주행부터 비교가 시작됩니다."
    elif n_risk > 0:
        secondary = (f"총 {n_total}건의 핵심 순간, 그 중 {n_risk}건이 위험 구간이었어요. "
                     f"다음 주행과 비교해 볼게요.")
    elif n_caution > 0:
        secondary = (f"총 {n_total}건의 핵심 순간, {n_caution}건이 주의가 필요했어요. "
                     f"다음 주행과 비교해 볼게요.")
    else:
        secondary = f"총 {n_total}건의 핵심 순간이 있었어요. 다음 주행과 비교해 볼게요."

    return (hero, secondary)


def _hero_with_history(score, events, prior,
                       overall: int, focus, n_total: int,
                       n_risk: int, n_caution: int) -> tuple[str, str]:
    """Coach-mode hero — picks the story that best describes how *this* drive
    differs from the previous one. Priority order:
      1. Same focus area as last time → "지난번에 얘기한 X, 이번에도…"  ← the moment
      2. Score jumped or fell meaningfully → "지난번보다 +/-N점, …"
      3. Otherwise → neutral status line referencing prior
    """
    prior_score = prior.score.total
    delta = overall - prior_score
    prior_focus = prior.score.focus_area
    now_cats = _count_by_category(events)
    prior_cats = _count_by_category(prior.events)

    same_focus = (focus is not None and prior_focus is not None
                  and focus.name_ko == prior_focus.name_ko)
    ko2key = _name_ko_to_key()

    # ── 1. Same weakness twice in a row — strongest "I remember" beat ──
    if same_focus and focus is not None:
        key = ko2key.get(focus.name_ko, "")
        now_n = now_cats.get(key, 0)
        prior_n = prior_cats.get(key, 0)
        if now_n and prior_n and now_n < prior_n:
            hero = (f"지난번에 얘기한 <em>{focus.name_ko}</em>,<br/>"
                    f"이번엔 {prior_n}건 → {now_n}건으로 좋아졌어요.")
        elif now_n and prior_n and now_n > prior_n:
            hero = (f"지난번에도 <em>{focus.name_ko}</em>가 이슈였는데,<br/>"
                    f"이번엔 더 자주 나왔어요 ({prior_n} → {now_n}건).")
        else:
            hero = (f"지난번에도 같은 패턴이 보였어요.<br/>"
                    f"<em>{focus.name_ko}</em>를 한 번 더 신경 써 볼 시간이에요.")
        secondary = _secondary_with_delta(delta, n_total, n_risk, n_caution)
        return (hero, secondary)

    # ── 2. Prior focus area cleared this run — meaningful win.
    #    Only celebrate when overall score didn't tank; otherwise the user
    #    sees "한 번도 안 나왔어요" next to a falling number and gets confused.
    if (prior_focus is not None
            and (focus is None or focus.name_ko != prior_focus.name_ko)
            and delta >= -2):
        prior_key = ko2key.get(prior_focus.name_ko, "")
        prior_n = prior_cats.get(prior_key, 0)
        now_n = now_cats.get(prior_key, 0)
        if now_n == 0 and prior_n > 0:
            hero = (f"지난번 가장 큰 이슈였던 <em>{prior_focus.name_ko}</em>,<br/>"
                    f"오늘은 한 번도 나오지 않았어요.")
            secondary = _secondary_with_delta(delta, n_total, n_risk, n_caution)
            return (hero, secondary)

    # ── 3. Score moved meaningfully (±3 or more) ──
    if delta >= 3:
        if focus:
            hero = (f"지난번보다 <em>+{delta}점</em>.<br/>"
                    f"다음엔 {focus.name_ko}만 손보면 더 좋을 것 같아요.")
        else:
            hero = f"지난번보다 <em>+{delta}점</em>,<br/>전반적으로 안정적이었어요."
    elif delta <= -3:
        if focus:
            hero = (f"지난번보다 <em>{delta}점</em>.<br/>"
                    f"오늘은 <em>{focus.name_ko}</em>에서 아쉬웠어요.")
        else:
            hero = f"지난번보다 <em>{delta}점</em>,<br/>오늘은 평소만큼은 아니었어요."
    else:
        # ── 4. Score essentially flat — describe state but acknowledge history
        if overall >= 88 and n_risk == 0:
            hero = f"지난번과 비슷하게 <em>안정적</em>이었어요."
        elif focus:
            hero = (f"비슷한 점수, 같은 톤의 주행이에요.<br/>"
                    f"<em>{focus.name_ko}</em>에서 조금 더 여유를 가져 보세요.")
        else:
            hero = "지난번과 비슷한 흐름으로 안정적이었어요."

    secondary = _secondary_with_delta(delta, n_total, n_risk, n_caution)
    return (hero, secondary)


def _secondary_with_delta(delta: int, n_total: int,
                          n_risk: int, n_caution: int) -> str:
    """One-liner under the hero — what we found, with a quick history tag."""
    sign = "+" if delta > 0 else ""
    delta_str = f"점수 변화 {sign}{delta}점" if delta != 0 else "점수 변화 없음"
    if n_total == 0:
        return f"이번엔 큰 위험 없이 부드럽게 흘러갔어요 · {delta_str}."
    if n_risk > 0:
        return (f"총 {n_total}건의 핵심 순간, 그 중 {n_risk}건이 위험 구간이었어요 · "
                f"{delta_str}.")
    if n_caution > 0:
        return (f"총 {n_total}건의 핵심 순간, {n_caution}건이 주의가 필요했어요 · "
                f"{delta_str}.")
    return f"총 {n_total}건의 핵심 순간이 있었어요 · {delta_str}."


_SEVERITY_TO_BADGE = {
    "safe":    ("GOOD",   ""),
    "caution": ("REVIEW", "amber"),
    "danger":  ("RISK",   "risk"),
}


def _event_card_html(event, coaching, still_url: str, duration_s: float) -> str:
    """One key-moment card — still image + classification + headline +
    summary + a single line of VLM coaching."""
    badge_text, badge_cls = _SEVERITY_TO_BADGE.get(event.severity, ("EVENT", ""))
    tc = _fmt_duration(event.timestamp)
    coach_line = ""
    if coaching:
        # Action plan is the actionable take-away — use it as the coach line.
        coach_line = (coaching.action_plan or coaching.scene_analysis
                      or coaching.scene_description or "")
    img_el = (
        f'<img src="{still_url}" alt="{tc} {event.title}"/>'
        if still_url else
        '<div class="results-moment-fallback"></div>'
    )
    return f"""
    <article class="results-moment-card">
      <div class="results-moment-img">
        {img_el}
        <span class="results-moment-tc">{tc}</span>
        <span class="results-moment-badge {badge_cls}">{badge_text}</span>
      </div>
      <div class="results-moment-cat">{(event.category or '').upper()}</div>
      <h4>{event.title}</h4>
      <p>{event.summary}</p>
      {f'<div class="results-moment-coach"><b>코칭</b><span>{coach_line}</span></div>' if coach_line else ''}
    </article>
    """


def _timeline_markers_html(events, duration_s: float) -> str:
    """Build timeline DOM: a colored ±1-second band UNDER each event +
    the marker line above. Bands come first so markers sit on top."""
    if duration_s <= 0 or not events:
        return ""
    bands, markers = [], []
    for e in events:
        pct = max(0.0, min(100.0, (e.timestamp / duration_s) * 100))
        _, cls = _SEVERITY_TO_BADGE.get(e.severity, ("", ""))
        # ±1 second window — the moment "around" the event
        band_start = max(0.0, ((e.timestamp - 1) / duration_s) * 100)
        band_end   = min(100.0, ((e.timestamp + 1) / duration_s) * 100)
        band_w = max(0.0, band_end - band_start)
        bands.append(
            f'<div class="results-tl-band {cls}" '
            f'style="left:{band_start:.2f}%; width:{band_w:.2f}%"></div>'
        )
        label = f"{_fmt_duration(e.timestamp)} · {e.title}"
        markers.append(
            f'<div class="results-tl-marker {cls}" '
            f'style="left:{pct:.1f}%" data-l="{label}"></div>'
        )
    return "".join(bands) + "".join(markers)


def _ticks_html(duration_s: float, count: int = 3) -> str:
    if duration_s <= 0:
        return "<span>00:00</span>" * count
    parts = []
    for i in range(count):
        t = duration_s * (i / (count - 1))
        parts.append(f"<span>{_fmt_duration(t)}</span>")
    return "".join(parts)


def _category_bars_html(score) -> str:
    if not score or not score.categories:
        return ""
    rows = []
    for cat in score.categories:
        w = max(0, min(100, cat.score))
        tier = _category_tier(cat.score)
        rows.append(f"""
        <div class="results-cat-row {tier}">
          <span class="results-cat-name">{cat.name_ko}</span>
          <span class="results-cat-bar"><span class="results-cat-fill" style="width:{w}%"></span></span>
          <span class="results-cat-num">{cat.score}</span>
        </div>
        """)
    return "".join(rows)


def _score_delta_html(score, prior) -> str:
    """Small chip under the big score number — '+3 vs 지난 주행' / '−2 vs 지난 주행'
    / '첫 분석' when there's no prior. Empty string if no score either."""
    if not score:
        return ""
    if prior is None:
        return ('<div class="results-score-delta first">'
                '첫 분석 · 다음부터 비교 시작'
                '</div>')
    delta = score.total - prior.score.total
    if delta > 0:
        cls, arrow, n = "up", "▲", delta
    elif delta < 0:
        cls, arrow, n = "down", "▼", -delta
    else:
        cls, arrow, n = "flat", "·", 0
    label = "변화 없음" if delta == 0 else f"{arrow} {n}점"
    return (f'<div class="results-score-delta {cls}">'
            f'<span class="delta-n">{label}</span>'
            f'<span class="delta-l">vs 지난 주행</span>'
            f'</div>')


def results_screen_html(
    video_path: str = "",
    filename: str = "",
    duration: float = 0.0,
    score=None,
    events=None,
    coachings=None,
    event_stills: dict | None = None,
    session_id: str = "—",
    prior=None,
) -> str:
    """The cinematic RESULTS finale — one HTML blob in v4 tone.

    Sections, top to bottom:
      nav · stepper (all done) · hero sentence + score · timeline ·
      key-moment cards · annotated video · category breakdown · CTA · footer.

    `prior`: most recent past AnalysisRecord (from core.history.load_prior).
    When set, the hero sentence and score area both reference it — turning
    the report from a one-shot scorecard into a longitudinal coaching beat.
    """
    hero, secondary = _hero_sentence(score, events, prior=prior)
    score_comment = _score_comment(score)
    delta_html = _score_delta_html(score, prior)
    overall = score.total if score else 0
    grade = score.grade if score else "—"
    safe_name = filename or "주행 영상"
    events = events or []
    coachings = coachings or []
    event_stills = event_stills or {}
    vurl = _video_url(video_path)

    # Pair events with their coachings — assume same order
    moment_cards = ""
    for i, ev in enumerate(events[:3]):  # show up to 3 cards
        co = coachings[i] if i < len(coachings) else None
        still = event_stills.get(ev.frame_idx, "")
        still_url = _video_url(still) if still else ""
        moment_cards += _event_card_html(ev, co, still_url, duration)

    if not moment_cards:
        moment_cards = (
            '<div class="results-moments-empty">'
            '큰 이벤트 없이 부드럽게 흘러간 주행이었어요.'
            '</div>'
        )

    video_block = ""
    if vurl:
        video_block = f"""
        <section class="results-video-wrap">
          <div class="results-section-head">
            <span class="label label-signal">Annotated · 주석 영상</span>
            <h3>검출 결과를 영상 위에 직접 표시했어요.</h3>
          </div>
          <div class="results-video-frame">
            <video src="{vurl}" controls preload="metadata" playsinline></video>
            <span class="ready-br ready-br-tl"></span>
            <span class="ready-br ready-br-tr"></span>
            <span class="ready-br ready-br-bl"></span>
            <span class="ready-br ready-br-br"></span>
          </div>
        </section>
        """

    cat_bars = _category_bars_html(score)
    cat_section = ""
    if cat_bars:
        cat_section = f"""
        <section class="results-categories">
          <div class="results-section-head">
            <span class="label label-signal">Breakdown · 카테고리</span>
            <h3>5개 항목으로 본 오늘의 주행.</h3>
          </div>
          <div class="results-cat-grid">{cat_bars}</div>
        </section>
        """

    return f"""
<div class="dc-v3-root results-root">

  <nav class="ready-nav">
    <a class="brand" href="#dc-top" aria-label="DrivingAssis">
      <span class="brand-mark" aria-hidden="true">{_BRAND_SVG}</span>
      <span>DRIVING<span style="color:var(--signal)">ASSIS</span></span>
    </a>
    <div class="ready-nav-right">
      <span class="ready-session">SESSION · {session_id}</span>
    </div>
  </nav>

  <div class="ready-stepper-wrap">
    <div class="ready-stepper" role="list">
      <div class="ready-step done"><span class="num">01</span><span class="check">✓</span><span>업로드</span></div>
      <div class="ready-step done"><span class="num">02</span><span class="check">✓</span><span>검토</span></div>
      <div class="ready-step done"><span class="num">03</span><span class="check">✓</span><span>분석</span></div>
      <div class="ready-step current"><span class="num">04</span><span class="pulse"></span><span>리포트</span></div>
    </div>
  </div>

  <section class="results-hero">
    <div class="results-hero-left">
      <span class="label label-signal">Drive Report · {safe_name}</span>
      <h1 class="results-hero-sentence">{hero}</h1>
      <p class="results-hero-secondary">{secondary}</p>
    </div>
    <div class="results-hero-score">
      <div class="results-score-num">{overall}<span class="results-score-unit">/100</span></div>
      {delta_html}
      <div class="results-score-comment">{score_comment}</div>
      <div class="results-score-grade">GRADE · <b>{grade}</b></div>
    </div>
  </section>

  <section class="results-timeline-wrap">
    <div class="results-timeline-label">
      <h4>Timeline · 검출된 의사결정</h4>
      <div class="results-tl-ticks">{_ticks_html(duration)}</div>
    </div>
    <div class="results-tl">
      {_timeline_markers_html(events, duration)}
    </div>
  </section>

  <section class="results-moments-wrap">
    <div class="results-section-head">
      <span class="label label-signal">Key Moments · 핵심 순간</span>
      <h3>다시 봐야 할 순간과 한 줄 코칭.</h3>
    </div>
    <div class="results-moments-grid">
      {moment_cards}
    </div>
  </section>

  {video_block}

  {cat_section}

  <section class="results-cta">
    <button class="ready-btn-go" type="button" id="results-again-btn">
      또 다른 주행 분석하기 {_arrow_go_svg()}
    </button>
  </section>

  <footer class="ready-foot">© 2026 DRIVINGASSIS · 분석 세션 {session_id}</footer>

</div>
"""


# ─── HISTORY — '내 주행 기록' page ────────────────────────────
# Shows past analyses as a list, plus a sparkline of the score trend and
# the top-3 repeated event categories across all drives. The data comes
# from `core.history.load_recent()` — list[AnalysisRecord]. When there are
# 0 records the page falls back to an empty-state with an upload CTA.

from datetime import datetime as _dt


def _relative_date(iso_ts: str) -> str:
    """ISO timestamp → human-friendly Korean relative date."""
    try:
        then = _dt.fromisoformat(iso_ts)
    except (TypeError, ValueError):
        return iso_ts or "—"
    diff = _dt.now() - then
    days = diff.days
    if days < 0:
        return then.strftime("%Y.%m.%d")
    if days == 0:
        hours = diff.seconds // 3600
        if hours <= 0:
            return "방금 전"
        return f"{hours}시간 전"
    if days == 1:
        return "어제"
    if days < 7:
        return f"{days}일 전"
    if days < 28:
        return f"{days // 7}주 전"
    return then.strftime("%Y.%m.%d")


def _sparkline_svg(scores: list[int], w: int = 1000, h: int = 120) -> str:
    """SVG line chart for the score trend. Auto-scales Y to a tight range so
    visit-to-visit changes are visible (otherwise an 85→92 jump on a 0-100
    axis would look almost flat)."""
    if len(scores) < 2:
        return ""
    pad_x, pad_y = 12, 14
    lo, hi = min(scores), max(scores)
    span = max(8, hi - lo)  # never tighter than 8pts for visual breathing room
    lo = max(0, (lo + hi - span) // 2)
    hi = min(100, lo + span)
    span = hi - lo
    inner_w = w - 2 * pad_x
    inner_h = h - 2 * pad_y

    pts: list[tuple[float, float]] = []
    n = len(scores)
    for i, s in enumerate(scores):
        x = pad_x + (i / (n - 1)) * inner_w
        y = pad_y + (1 - (s - lo) / span) * inner_h
        pts.append((x, y))

    path = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    area = (f"M {pts[0][0]:.1f} {h - pad_y}"
            + " L " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts)
            + f" L {pts[-1][0]:.1f} {h - pad_y} Z")
    dots = "".join(
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" class="dot"/>'
        for x, y in pts
    )
    # Highlight the latest point with a bigger ring
    lx, ly = pts[-1]
    return f"""
    <svg class="history-sparkline" viewBox="0 0 {w} {h}" preserveAspectRatio="none">
      <defs>
        <linearGradient id="dcv3-sparkfill" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="rgba(0,229,154,0.18)"/>
          <stop offset="100%" stop-color="rgba(0,229,154,0)"/>
        </linearGradient>
      </defs>
      <path class="area" d="{area}"/>
      <path class="line" d="{path}"/>
      {dots}
      <circle cx="{lx:.1f}" cy="{ly:.1f}" r="6" class="dot-latest-halo"/>
      <circle cx="{lx:.1f}" cy="{ly:.1f}" r="4" class="dot-latest"/>
    </svg>
    """


def _aggregate_patterns(records) -> list[tuple[str, int, int]]:
    """Across all records, return (category_ko, total_event_count, drives_with_it)
    sorted by total events desc. Used by the 'repeated patterns' Top 3 section."""
    from core.schema import SCORE_CATEGORY_DEFS
    key_to_ko = {key: ko for key, _en, ko, _icon in SCORE_CATEGORY_DEFS}
    totals: dict[str, int] = {}
    drives: dict[str, int] = {}
    for rec in records:
        seen: set[str] = set()
        for ev in rec.events:
            totals[ev.category] = totals.get(ev.category, 0) + 1
            seen.add(ev.category)
        for cat in seen:
            drives[cat] = drives.get(cat, 0) + 1
    rows = [(key_to_ko.get(k, k), totals[k], drives.get(k, 0))
            for k in totals]
    rows.sort(key=lambda r: (-r[1], -r[2]))
    return rows


def _history_card_html(record, idx_in_list: int, total: int) -> str:
    """One card per past analysis. Shows score, focus area, event count, and
    a relative date. Cards are read-only for now — click-to-drill is a Week-3
    nice-to-have."""
    score = record.score
    focus = score.focus_area
    n_events = len(record.events)
    n_risk = sum(1 for e in record.events if e.severity == "danger")
    rel = _relative_date(record.analyzed_at)
    # ordinal: list is newest-first, so total - idx_in_list = "N번째 분석"
    nth = total - idx_in_list
    focus_html = (f'<span class="history-card-focus"><span class="k">FOCUS</span>'
                  f'<span class="v">{focus.name_ko}</span></span>')\
                 if focus else (
                  '<span class="history-card-focus"><span class="k">FOCUS</span>'
                  '<span class="v" style="color:var(--signal)">없음</span></span>')
    risk_dot = ('<span class="history-card-risk"></span>'
                if n_risk > 0 else '')
    return f"""
    <article class="history-card">
      <button class="history-card-del" type="button"
              data-session-id="{record.session_id}"
              data-nth="{nth:02d}"
              aria-label="이 분석 삭제">
        <svg viewBox="0 0 16 16" fill="none" stroke="currentColor"
             stroke-width="1.6" stroke-linecap="round">
          <path d="M3 3 L13 13 M13 3 L3 13"/>
        </svg>
      </button>
      <div class="history-card-head">
        <span class="history-card-nth">#{nth:02d}</span>
        <span class="history-card-date">{rel}</span>
      </div>
      <div class="history-card-score">
        <span class="num">{score.total}</span>
        <span class="unit">/100</span>
        <span class="grade">{score.grade}</span>
      </div>
      <div class="history-card-name" title="{record.video_name}">
        {record.video_name or '주행 영상'}
      </div>
      <div class="history-card-meta">
        {focus_html}
        <span class="history-card-events">
          <span class="k">EVENTS</span>
          <span class="v">{n_events}{risk_dot}</span>
        </span>
      </div>
    </article>
    """


def _pattern_card_html(rank: int, name_ko: str, total: int,
                       drives: int, n_records: int) -> str:
    """One pattern card — 'X가 N건, 전체 주행의 M%에서 반복'."""
    pct = round(drives / n_records * 100) if n_records else 0
    return f"""
    <article class="history-pattern-card">
      <span class="history-pattern-rank">TOP {rank}</span>
      <h4>{name_ko}</h4>
      <div class="history-pattern-stats">
        <div class="ps">
          <span class="ps-n">{total}</span>
          <span class="ps-l">총 발생</span>
        </div>
        <div class="ps">
          <span class="ps-n">{pct}<small>%</small></span>
          <span class="ps-l">의 주행에서</span>
        </div>
      </div>
    </article>
    """


def history_screen_html(records=None, session_id: str = "—") -> str:
    """The '내 주행 기록' page — list of past analyses, score trend sparkline,
    repeated-pattern Top 3. Falls back to an empty-state when records is empty."""
    records = list(records or [])
    n = len(records)

    if n == 0:
        return f"""
<div class="dc-v3-root history-root">
  <nav class="ready-nav">
    <a class="brand" href="#dc-top" aria-label="DrivingAssis">
      <span class="brand-mark" aria-hidden="true">{_BRAND_SVG}</span>
      <span>DRIVING<span style="color:var(--signal)">ASSIS</span></span>
    </a>
    <div class="ready-nav-right">
      <span class="ready-session">MY HISTORY</span>
    </div>
  </nav>

  <section class="history-empty">
    <div class="history-empty-icon">
      <svg viewBox="0 0 48 48" fill="none" stroke="currentColor"
           stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round">
        <rect x="6" y="10" width="36" height="30" rx="2"/>
        <path d="M6 18h36"/>
        <path d="M14 6v8M34 6v8"/>
      </svg>
    </div>
    <h1>아직 분석한 주행이 없어요.</h1>
    <p>첫 영상을 분석하면, 다음 주행부터<br/>이 자리에 패턴과 변화가 쌓입니다.</p>
    <button class="ready-btn-go" type="button" id="history-upload-btn">
      첫 영상 업로드 {_arrow_go_svg()}
    </button>
  </section>

  <footer class="ready-foot">© 2026 DRIVINGASSIS · MY HISTORY</footer>
</div>
"""

    # ── Non-empty: sparkline + patterns + card grid ──
    # Sparkline takes scores oldest-to-newest (left-to-right = time forward)
    scores_chrono = [r.score.total for r in reversed(records)]
    spark = _sparkline_svg(scores_chrono) if len(scores_chrono) >= 2 else (
        '<div class="history-sparkline-empty">'
        '두 번째 분석부터 점수 추이가 그려집니다.</div>'
    )

    latest = records[0].score.total
    oldest = records[-1].score.total
    delta_all = latest - oldest

    patterns = _aggregate_patterns(records)[:3]
    if patterns:
        pat_html = "".join(
            _pattern_card_html(i + 1, ko, total, drives, n)
            for i, (ko, total, drives) in enumerate(patterns)
        )
    else:
        pat_html = ('<div class="history-pattern-empty">'
                    '반복되는 패턴이 아직 없어요. 깨끗한 주행이 이어지고 있다는 뜻이에요.</div>')

    cards = "".join(_history_card_html(r, i, n) for i, r in enumerate(records))

    delta_summary = ""
    if len(records) >= 2:
        sign = "+" if delta_all > 0 else ""
        delta_summary = (f'<div class="history-trend-delta">'
                         f'<span class="k">처음 분석 대비</span>'
                         f'<span class="v {"up" if delta_all >= 0 else "down"}">'
                         f'{sign}{delta_all}점</span></div>')

    return f"""
<div class="dc-v3-root history-root">

  <nav class="ready-nav">
    <a class="brand" href="#dc-top" aria-label="DrivingAssis">
      <span class="brand-mark" aria-hidden="true">{_BRAND_SVG}</span>
      <span>DRIVING<span style="color:var(--signal)">ASSIS</span></span>
    </a>
    <div class="ready-nav-right">
      <span class="ready-session">MY HISTORY · {n}건</span>
    </div>
  </nav>

  <section class="history-header">
    <span class="label label-signal">My Drive History · 내 주행 기록</span>
    <h1>
      지금까지 <em>{n}건</em>의 분석.<br/>
      <span class="em">당신의 패턴이 보이기 시작합니다.</span>
    </h1>
  </section>

  <section class="history-trend-wrap">
    <div class="history-section-head">
      <span class="label label-signal">Trend · 점수 추이</span>
      <h3>시간을 따라 본 오늘까지의 흐름.</h3>
    </div>
    <div class="history-trend-card">
      {spark}
      <div class="history-trend-foot">
        <span class="k">처음</span><span class="v">{oldest}</span>
        <span class="sep">→</span>
        <span class="k">최근</span><span class="v">{latest}</span>
        {delta_summary}
      </div>
    </div>
  </section>

  <section class="history-patterns-wrap">
    <div class="history-section-head">
      <span class="label label-signal">Repeated · 반복 패턴</span>
      <h3>당신이 가장 자주 만나는 순간 Top 3.</h3>
    </div>
    <div class="history-pattern-grid">
      {pat_html}
    </div>
  </section>

  <section class="history-list-wrap">
    <div class="history-section-head">
      <span class="label label-signal">All Reports · 전체 분석</span>
      <h3>지난 분석들, 최근 순서로.</h3>
    </div>
    <div class="history-grid">
      {cards}
    </div>
  </section>

  <section class="history-cta">
    <button class="ready-btn-go" type="button" id="history-upload-btn">
      새 영상 분석하기 {_arrow_go_svg()}
    </button>
  </section>

  <footer class="ready-foot">© 2026 DRIVINGASSIS · MY HISTORY · {n}건</footer>

</div>
"""


# ─── Always-on header / footer for non-IDLE screens ───────────
# When IDLE is hidden, the v3 nav (inside idle_hero_html) is also hidden
# — so we render a minimal header/footer here for UPLOADED/ANALYZING/RESULTS.
# Both are wrapped in .dc-v3-root so v3 styles apply.

def app_header_html() -> str:
    """Minimal always-visible header for non-IDLE screens.

    The full v3 fixed nav lives inside `idle_hero_html()`; that one is
    visible only on the IDLE screen. This one is a *static* (non-fixed)
    header that shows on UPLOADED/ANALYZING/RESULTS so the user can still
    click the brand to go home.
    """
    return f"""
    <div class="dc-v3-root" style="background: transparent;">
      <div style="padding: 18px var(--v3-pad); display: flex;
                  align-items: center; justify-content: space-between;">
        {_brand_html()}
      </div>
    </div>
    """


def footer_html() -> str:
    """Compact footer for non-IDLE screens (the full v3 footer lives in IDLE)."""
    return """
    <div class="dc-v3-root" style="background: transparent;">
      <div class="foot-bar" style="padding: 28px var(--v3-pad); margin-top: 0;
                                    border-top: 1px solid var(--line);">
        <div class="left">© 2026 DrivingAssis</div>
        <div class="right">
          <span>KR · KO</span>
          <a href="#">Status</a>
          <a href="#">Security</a>
        </div>
      </div>
    </div>
    """
