#!/usr/bin/env python3
"""
Generates the animated SVG assets for the profile README.

Everything is pure SVG + CSS keyframes (no JS, no external fonts) so it renders
and animates inside GitHub's <img> sandbox. Text uses `textLength` so the layout
is deterministic no matter which fonts the visitor happens to have installed.

    python3 tools/build_assets.py
"""

from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"

# ── palette ───────────────────────────────────────────────────────────────────
BG0, BG1 = "#05030e", "#0b0720"
MAGENTA = "#ff2e97"
PINK = "#ff6ec7"
VIOLET = "#7b5cff"
CYAN = "#22e0ff"
MINT = "#6ef7c1"
TEXT = "#eae6ff"
MUTED = "#9a93c7"
FAINT = "#5b5390"

ACCENTS = [MAGENTA, CYAN, VIOLET, PINK, MINT]

SANS = "ui-sans-serif,-apple-system,BlinkMacSystemFont,'Segoe UI',Inter,Roboto,Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"

MONO_ADV = 0.6  # monospace advance width as a fraction of font-size


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def mono_w(text: str, size: float) -> float:
    """Deterministic width for a monospace run."""
    return round(len(text) * size * MONO_ADV, 2)


def mono(text, x, y, size, fill, weight=400, anchor="start", opacity=None, cls=None):
    w = mono_w(text, size)
    a = f' opacity="{opacity}"' if opacity is not None else ""
    c = f' class="{cls}"' if cls else ""
    return (
        f'<text x="{x}" y="{y}" font-family="{MONO}" font-size="{size}" '
        f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" '
        f'textLength="{w}" lengthAdjust="spacing"{a}{c}>{esc(text)}</text>'
    )


def sans(text, x, y, size, fill, weight=700, anchor="start", length=None,
         spacing=None, cls=None, opacity=None):
    tl = f' textLength="{length}" lengthAdjust="spacing"' if length else ""
    ls = f' letter-spacing="{spacing}"' if spacing else ""
    c = f' class="{cls}"' if cls else ""
    a = f' opacity="{opacity}"' if opacity is not None else ""
    return (
        f'<text x="{x}" y="{y}" font-family="{SANS}" font-size="{size}" '
        f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{ls}{tl}{c}{a}>'
        f"{esc(text)}</text>"
    )


def shell(w, h, body, defs="", style=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none" role="img">\n'
        f"<defs>\n{defs}\n</defs>\n"
        f"<style>\n<![CDATA[\n{style}\n]]>\n</style>\n"
        f"{body}\n</svg>\n"
    )


# ── shared defs ───────────────────────────────────────────────────────────────
def common_defs(uid, w, h, rx=26):
    return f"""
<linearGradient id="neon-{uid}" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0%" stop-color="{MAGENTA}"/>
  <stop offset="45%" stop-color="{VIOLET}"/>
  <stop offset="100%" stop-color="{CYAN}"/>
</linearGradient>
<linearGradient id="sheenG-{uid}" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0%" stop-color="#ffffff" stop-opacity="0"/>
  <stop offset="50%" stop-color="{PINK}" stop-opacity="0.13"/>
  <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
</linearGradient>
<linearGradient id="glass-{uid}" x1="0" y1="0" x2="0.4" y2="1">
  <stop offset="0%" stop-color="#ffffff" stop-opacity="0.10"/>
  <stop offset="55%" stop-color="#ffffff" stop-opacity="0.03"/>
  <stop offset="100%" stop-color="#ffffff" stop-opacity="0.06"/>
</linearGradient>
<linearGradient id="edge-{uid}" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0%" stop-color="{MAGENTA}" stop-opacity="0.55"/>
  <stop offset="50%" stop-color="{VIOLET}" stop-opacity="0.20"/>
  <stop offset="100%" stop-color="{CYAN}" stop-opacity="0.55"/>
</linearGradient>
<linearGradient id="bgfill-{uid}" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0%" stop-color="{BG0}"/>
  <stop offset="100%" stop-color="{BG1}"/>
</linearGradient>
<radialGradient id="blobA-{uid}"><stop offset="0%" stop-color="{MAGENTA}" stop-opacity="0.85"/><stop offset="100%" stop-color="{MAGENTA}" stop-opacity="0"/></radialGradient>
<radialGradient id="blobB-{uid}"><stop offset="0%" stop-color="{CYAN}" stop-opacity="0.75"/><stop offset="100%" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>
<radialGradient id="blobC-{uid}"><stop offset="0%" stop-color="{VIOLET}" stop-opacity="0.9"/><stop offset="100%" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>
<radialGradient id="blobD-{uid}"><stop offset="0%" stop-color="{MINT}" stop-opacity="0.45"/><stop offset="100%" stop-color="{MINT}" stop-opacity="0"/></radialGradient>
<filter id="soft-{uid}" x="-60%" y="-60%" width="220%" height="220%">
  <feGaussianBlur stdDeviation="52"/>
</filter>
<filter id="glow-{uid}" x="-80%" y="-80%" width="260%" height="260%">
  <feGaussianBlur stdDeviation="6" result="b"/>
  <feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
<filter id="grain-{uid}" x="0" y="0" width="100%" height="100%">
  <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" stitchTiles="stitch"/>
  <feColorMatrix type="saturate" values="0"/>
</filter>
<pattern id="grid-{uid}" width="44" height="44" patternUnits="userSpaceOnUse">
  <path d="M44 0H0V44" stroke="{TEXT}" stroke-opacity="0.045" stroke-width="1" fill="none"/>
</pattern>
<clipPath id="card-{uid}"><rect x="6" y="6" width="{w - 12}" height="{h - 12}" rx="{rx}"/></clipPath>
"""


def aurora(uid, w, h):
    """Slow-drifting blurred colour blobs — the 'aurora' behind the glass."""
    return f"""
<g filter="url(#soft-{uid})" opacity="0.9">
  <circle class="b1" cx="{int(w*0.18)}" cy="{int(h*0.30)}" r="{int(h*0.55)}" fill="url(#blobA-{uid})"/>
  <circle class="b2" cx="{int(w*0.78)}" cy="{int(h*0.72)}" r="{int(h*0.60)}" fill="url(#blobB-{uid})"/>
  <circle class="b3" cx="{int(w*0.52)}" cy="{int(h*0.10)}" r="{int(h*0.50)}" fill="url(#blobC-{uid})"/>
  <circle class="b4" cx="{int(w*0.92)}" cy="{int(h*0.20)}" r="{int(h*0.40)}" fill="url(#blobD-{uid})"/>
</g>"""


AURORA_CSS = """
.b1,.b2,.b3,.b4 { transform-box: view-box; }
.b1 { animation: drift1 26s ease-in-out infinite alternate; }
.b2 { animation: drift2 31s ease-in-out infinite alternate; }
.b3 { animation: drift3 23s ease-in-out infinite alternate; }
.b4 { animation: drift4 37s ease-in-out infinite alternate; }
@keyframes drift1 { from { transform: translate(0,0) scale(1); } to { transform: translate(170px,-40px) scale(1.25); } }
@keyframes drift2 { from { transform: translate(0,0) scale(1.1); } to { transform: translate(-190px,-70px) scale(0.85); } }
@keyframes drift3 { from { transform: translate(0,0) scale(0.9); } to { transform: translate(120px,90px) scale(1.2); } }
@keyframes drift4 { from { transform: translate(0,0) scale(1); } to { transform: translate(-140px,60px) scale(1.3); } }
"""


def card(uid, w, h, rx=26):
    """Frosted glass panel: aurora, grid, grain, border."""
    return f"""
<g clip-path="url(#card-{uid})">
  <rect x="6" y="6" width="{w - 12}" height="{h - 12}" rx="{rx}" fill="url(#bgfill-{uid})"/>
  {aurora(uid, w, h)}
  <rect x="6" y="6" width="{w - 12}" height="{h - 12}" rx="{rx}" fill="{BG0}" opacity="0.55"/>
  <rect x="6" y="6" width="{w - 12}" height="{h - 12}" rx="{rx}" fill="url(#grid-{uid})"/>
  <rect x="6" y="6" width="{w - 12}" height="{h - 12}" rx="{rx}" fill="url(#glass-{uid})"/>
  <rect x="6" y="6" width="{w - 12}" height="{h - 12}" filter="url(#grain-{uid})" opacity="0.05"/>
  <rect class="sheen" x="-400" y="6" width="300" height="{h - 12}" fill="url(#sheenG-{uid})"/>
</g>
<rect x="6.5" y="6.5" width="{w - 13}" height="{h - 13}" rx="{rx}" fill="none"
      stroke="url(#edge-{uid})" stroke-width="1.4"/>"""


def sheen_css(w):
    return f"""
.sheen {{ transform-box: view-box; animation: sheen 9s ease-in-out infinite; }}
@keyframes sheen {{
  0%,55% {{ transform: translateX(0) skewX(-14deg); }}
  85%,100% {{ transform: translateX({w + 500}px) skewX(-14deg); }}
}}
"""


# ── 1. hero ───────────────────────────────────────────────────────────────────
def build_hero():
    W, H, U = 1200, 420, "h"
    X = 60
    body = [card(U, W, H)]

    # kicker
    body.append(
        f'<text x="{X}" y="112" font-family="{MONO}" font-size="14" font-weight="600" '
        f'fill="{CYAN}" letter-spacing="4.2" textLength="352" lengthAdjust="spacing" '
        f'class="fade-a">// FULLSTACK SOFTWARE ENGINEER</text>'
    )

    # wordmark
    body.append(
        f'<g class="fade-b"><text x="{X}" y="196" font-family="{SANS}" font-size="78" font-weight="800" '
        f'fill="url(#word-h)" letter-spacing="5" textLength="764" lengthAdjust="spacing" '
        f'filter="url(#glow-h)">DAVID REICHERT</text></g>'
    )

    # animated rule under the wordmark
    body.append(
        f'<g class="fade-b"><rect x="{X}" y="214" width="764" height="2.5" rx="1.25" fill="url(#neon-h)" opacity="0.75"/>'
        f'<rect class="pulse" x="{X}" y="212" width="120" height="6" rx="3" fill="{CYAN}" '
        f'opacity="0.9" filter="url(#glow-h)"/></g>'
    )

    # typewriter lines
    lines = [
        "fullstack · frontend, backend, infra, and the glue between",
        "11 years writing code · 9 years getting paid for it",
        "stack: whichever one the problem actually deserves",
    ]
    size = 18
    widths = [mono_w(t, size) for t in lines]
    for i, (t, wpx) in enumerate(zip(lines, widths)):
        body.append(
            f'<g clip-path="url(#type{i})">{mono(t, X, 264, size, TEXT, opacity=0.92, cls=f"tl{i}")}</g>'
        )
    body.append(
        f'<rect class="caret" x="{X}" y="248" width="9" height="21" fill="{PINK}" filter="url(#glow-h)"/>'
    )

    # glass stat pills
    pills = [("23", "years old"), ("11", "years hobby"), ("9", "years professional"), ("∞", "still curious")]
    px = X
    for i, (num, label) in enumerate(pills):
        acc = ACCENTS[i % len(ACCENTS)]
        nw, lw = mono_w(num, 17), mono_w(label, 12.5)
        pw = round(nw + lw + 46, 1)
        body.append(
            f'<g class="pill" style="animation-delay:{0.85 + i*0.12:.2f}s">'
            f'<rect x="{px}" y="312" width="{pw}" height="42" rx="21" fill="#ffffff" fill-opacity="0.05" '
            f'stroke="{acc}" stroke-opacity="0.45" stroke-width="1"/>'
            f'<circle cx="{px + 15}" cy="333" r="3" fill="{acc}" filter="url(#glow-h)"/>'
            f"{mono(num, px + 26, 339, 17, acc, weight=700)}"
            f"{mono(label, px + 26 + nw + 8, 338, 12.5, MUTED)}"
            f"</g>"
        )
        px += pw + 12

    # status strip
    body.append(f'<circle class="blink" cx="{X + 4}" cy="385" r="4" fill="{MINT}" filter="url(#glow-h)"/>')
    body.append(
        mono("AVAILABLE FOR INTERESTING PROBLEMS   ·   UPTIME 23Y   ·   STATUS: SHIPPING",
             X + 18, 389, 11.5, FAINT, cls="fade-c")
    )

    # orbital emblem
    cx, cy = 985, 210
    body.append(f'<g class="fade-b">')
    body.append(f'<circle cx="{cx}" cy="{cy}" r="150" fill="url(#blobC-h)" opacity="0.30"/>')
    for i, (rx_, ry_, rot, dur, acc, rev) in enumerate([
        (132, 132, 0, 24, MAGENTA, False),
        (146, 58, -24, 17, CYAN, True),
        (108, 108, 0, 31, VIOLET, False),
        (150, 44, 62, 21, MINT, True),
    ]):
        d = "reverse" if rev else "normal"
        body.append(
            f'<g class="orb" style="animation-duration:{dur}s;animation-direction:{d}">'
            f'<ellipse cx="{cx}" cy="{cy}" rx="{rx_}" ry="{ry_}" fill="none" stroke="{acc}" '
            f'stroke-opacity="0.30" stroke-width="1.2" transform="rotate({rot} {cx} {cy})"/>'
            f'<g transform="rotate({rot} {cx} {cy})">'
            f'<circle cx="{cx + rx_}" cy="{cy}" r="4.5" fill="{acc}" filter="url(#glow-h)"/>'
            f'<circle cx="{cx - rx_}" cy="{cy}" r="2.5" fill="{acc}" opacity="0.7"/>'
            f"</g></g>"
        )
    body.append(
        f'<g class="core"><circle cx="{cx}" cy="{cy}" r="52" fill="{BG0}" fill-opacity="0.72" '
        f'stroke="url(#neon-h)" stroke-width="1.6"/>'
        f'<circle cx="{cx}" cy="{cy}" r="52" fill="url(#blobA-h)" opacity="0.35"/></g>'
        f'<text x="{cx}" y="{cy + 13}" font-family="{SANS}" font-size="36" font-weight="800" '
        f'fill="url(#word-h)" text-anchor="middle" letter-spacing="2" filter="url(#glow-h)">DR</text>'
    )
    body.append("</g>")

    defs = common_defs(U, W, H) + f"""
<linearGradient id="word-h" x1="0" y1="0" x2="1" y2="0.6">
  <stop offset="0%" stop-color="{PINK}"><animate attributeName="stop-color" values="{PINK};{CYAN};{VIOLET};{PINK}" dur="12s" repeatCount="indefinite"/></stop>
  <stop offset="50%" stop-color="{TEXT}"/>
  <stop offset="100%" stop-color="{CYAN}"><animate attributeName="stop-color" values="{CYAN};{VIOLET};{PINK};{CYAN}" dur="12s" repeatCount="indefinite"/></stop>
</linearGradient>
""" + "".join(
        f'<clipPath id="type{i}"><rect class="rv{i}" x="{X}" y="244" width="{w}" height="30"/></clipPath>'
        for i, w in enumerate(widths)
    )

    # typewriter timing: 12s loop, three 4s acts (type 1.5s → hold → fade)
    type_css = """
.rv0,.rv1,.rv2 { transform-box: fill-box; transform-origin: left center; transform: scaleX(0);
                 animation: reveal 12s steps(48,end) infinite; }
.rv1 { animation-delay: 4s; }
.rv2 { animation-delay: 8s; }
@keyframes reveal { 0% { transform: scaleX(0); } 12.5%,33.33% { transform: scaleX(1); } 33.34%,100% { transform: scaleX(0); } }
.tl0,.tl1,.tl2 { opacity: 0; animation: peek 12s linear infinite; }
.tl1 { animation-delay: 4s; }
.tl2 { animation-delay: 8s; }
@keyframes peek { 0%,30% { opacity: .92; } 33.33%,100% { opacity: 0; } }
.caret { transform-box: view-box; animation: run 12s steps(48,end) infinite, blink .9s steps(2,end) infinite; }
""" + f"""
@keyframes run {{
  0% {{ transform: translateX(0); }}
  12.5%,33.33% {{ transform: translateX({widths[0]}px); }}
  33.34% {{ transform: translateX(0); }}
  45.83%,66.66% {{ transform: translateX({widths[1]}px); }}
  66.67% {{ transform: translateX(0); }}
  79.16%,100% {{ transform: translateX({widths[2]}px); }}
}}
"""

    style = AURORA_CSS + sheen_css(W) + type_css + f"""
@keyframes blink {{ 0%,100% {{ opacity: 1; }} 50% {{ opacity: 0; }} }}
.blink {{ animation: blink 1.8s ease-in-out infinite; }}
.pulse {{ transform-box: view-box; animation: slide 7s cubic-bezier(.5,0,.5,1) infinite; }}
@keyframes slide {{ 0%,100% {{ transform: translateX(0); }} 50% {{ transform: translateX(644px); }} }}
.orb {{ transform-box: view-box; transform-origin: {cx}px {cy}px;
        animation-name: spin; animation-timing-function: linear; animation-iteration-count: infinite; }}
@keyframes spin {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(360deg); }} }}
.core {{ transform-box: view-box; transform-origin: {cx}px {cy}px; animation: breathe 4.5s ease-in-out infinite; }}
@keyframes breathe {{ 0%,100% {{ transform: scale(1); opacity: .95; }} 50% {{ transform: scale(1.05); opacity: 1; }} }}
.fade-a,.fade-b,.fade-c,.pill {{ opacity: 0; animation: rise .9s cubic-bezier(.2,.8,.2,1) forwards; }}
.fade-a {{ animation-delay: .1s; }}
.fade-b {{ animation-delay: .35s; }}
.fade-c {{ animation-delay: 1.35s; }}
.pill  {{ transform-box: view-box; }}
@keyframes rise {{ from {{ opacity: 0; transform: translateY(14px); }} to {{ opacity: 1; transform: translateY(0); }} }}
"""
    (OUT / "hero.svg").write_text(shell(W, H, "\n".join(body), defs, style))


# ── 2. stack marquee ──────────────────────────────────────────────────────────
ROW_A = ["TypeScript", "React", "Next.js", "Vue", "Svelte", "Tailwind", "Vite",
         "Node.js", "Python", "Go", "Rust", "C#", ".NET", "PHP", "Java",
         "React Native", "Three.js", "HTML/CSS"]
ROW_B = ["PostgreSQL", "MySQL", "MongoDB", "Redis", "Docker", "Kubernetes", "Linux",
         "AWS", "GCP", "Nginx", "GraphQL", "REST", "gRPC", "CI/CD", "Terraform",
         "Git", "Bash", "Prisma"]


def build_stack():
    W, H, U = 1200, 300, "s"
    size = 14.5

    def row(items, y, offset):
        chips, x = [], 0
        for i, t in enumerate(items):
            acc = ACCENTS[(i + offset) % len(ACCENTS)]
            tw = mono_w(t, size)
            cw = round(tw + 46, 1)
            chips.append(
                f'<g transform="translate({x},0)">'
                f'<rect x="0" y="{y}" width="{cw}" height="42" rx="12" fill="#ffffff" fill-opacity="0.055" '
                f'stroke="{acc}" stroke-opacity="0.42" stroke-width="1"/>'
                f'<circle cx="17" cy="{y + 21}" r="3.4" fill="{acc}"/>'
                f"{mono(t, 30, y + 26, size, TEXT, opacity=0.9)}"
                f"</g>"
            )
            x += cw + 14
        return "".join(chips), x

    a_chips, aw = row(ROW_A, 118, 0)
    b_chips, bw = row(ROW_B, 186, 2)

    body = [card(U, W, H)]
    body.append(
        f'<text x="42" y="66" font-family="{MONO}" font-size="13" font-weight="600" fill="{CYAN}" '
        f'letter-spacing="4" textLength="300" lengthAdjust="spacing">// STACK — A LITTLE OF EVERYTHING</text>'
    )
    body.append(mono("the list rotates · the fundamentals don't", W - 42, 66, 12.5, FAINT, anchor="end"))
    body.append(
        f'<g mask="url(#fade-s)">'
        f'<g class="mA"><g>{a_chips}</g><g transform="translate({aw},0)">{a_chips}</g></g>'
        f'<g class="mB"><g>{b_chips}</g><g transform="translate({bw},0)">{b_chips}</g></g>'
        f"</g>"
    )

    defs = common_defs(U, W, H) + f"""
<linearGradient id="fadeG-s" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0%" stop-color="#000"/><stop offset="10%" stop-color="#fff"/>
  <stop offset="90%" stop-color="#fff"/><stop offset="100%" stop-color="#000"/>
</linearGradient>
<mask id="fade-s"><rect x="6" y="100" width="{W - 12}" height="150" fill="url(#fadeG-s)"/></mask>
"""
    style = AURORA_CSS + sheen_css(W) + f"""
.mA,.mB {{ transform-box: view-box; }}
.mA {{ animation: marA 46s linear infinite; }}
.mB {{ animation: marB 54s linear infinite; }}
@keyframes marA {{ from {{ transform: translateX(0); }} to {{ transform: translateX(-{aw}px); }} }}
@keyframes marB {{ from {{ transform: translateX(-{bw}px); }} to {{ transform: translateX(0); }} }}
"""
    (OUT / "stack.svg").write_text(shell(W, H, "\n".join(body), defs, style))


# ── 3. timeline ───────────────────────────────────────────────────────────────
def build_timeline():
    W, H, U = 1200, 320, "t"
    x0, x1 = 96, 1104
    y_axis = 214
    y0, y1 = 2015, 2026
    span = y1 - y0

    def px(year):
        return round(x0 + (year - y0) / span * (x1 - x0), 1)

    body = [card(U, W, H)]
    body.append(
        f'<text x="42" y="62" font-family="{MONO}" font-size="13" font-weight="600" fill="{CYAN}" '
        f'letter-spacing="4" textLength="250" lengthAdjust="spacing">// git log --reverse</text>'
    )
    body.append(mono("teenage side job → part-time helper → full-time engineer", W - 42, 62, 12.5, FAINT, anchor="end"))

    # axis + year ticks
    body.append(f'<line x1="{x0}" y1="{y_axis}" x2="{x1}" y2="{y_axis}" stroke="{TEXT}" stroke-opacity="0.12" stroke-width="1"/>')
    for yr in range(y0, y1 + 1):
        x = px(yr)
        major = yr % 2 == 1 or yr in (y0, y1)
        body.append(f'<line x1="{x}" y1="{y_axis - (7 if major else 4)}" x2="{x}" y2="{y_axis}" stroke="{TEXT}" stroke-opacity="{0.30 if major else 0.14}" stroke-width="1"/>')
        if major:
            body.append(mono(str(yr), x, y_axis + 22, 11.5, FAINT, anchor="middle"))

    # two draw-in bars
    bars = [
        (2015, "writing code", "11 years", MAGENTA, 144, 0.0),
        (2017, "getting paid for it", "9 years", CYAN, 184, 0.45),
    ]
    for i, (start, label, dur, acc, ybar, delay) in enumerate(bars):
        xs, xe = px(start), px(y1)
        length = round(xe - xs, 1)
        # A horizontal <line> has a zero-height bbox, so an objectBoundingBox filter
        # region collapses to nothing — the glow is painted as a wide soft halo instead.
        for sw, op in ((16, 0.18), (10, 0.28), (7, 0.9)):
            body.append(
                f'<line class="bar" x1="{xs}" y1="{ybar}" x2="{xe}" y2="{ybar}" stroke="{acc}" '
                f'stroke-width="{sw}" stroke-linecap="round" stroke-opacity="{op}" '
                f'stroke-dasharray="{length}" stroke-dashoffset="{length}" '
                f'style="animation-delay:{delay}s"/>'
            )
        body.append(mono(label, xs + 4, ybar - 16, 14, TEXT, opacity=0.9, cls="fade"))
        body.append(mono(dur, xe - 4, ybar - 16, 14, acc, weight=700, anchor="end", cls="fade"))
        # travelling packet
        body.append(
            f'<circle r="4" fill="{acc}" filter="url(#glow-t)" opacity="0.95">'
            f'<animate attributeName="cx" values="{xs};{xe}" dur="{6 + i}s" repeatCount="indefinite"/>'
            f'<animate attributeName="cy" values="{ybar};{ybar}" dur="{6 + i}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;1;1;0" dur="{6 + i}s" repeatCount="indefinite"/>'
            f"</circle>"
        )

    # milestone nodes on the axis
    nodes = [
        (2015, "first line of code", "age 12", MAGENTA),
        (2017, "first paid work", "age 14", VIOLET),
        (2026, "still shipping", "age 23", CYAN),
    ]
    for i, (yr, title, sub, acc) in enumerate(nodes):
        x = px(yr)
        # left-align every label except the last, so neighbouring captions never collide
        anchor = "end" if i == len(nodes) - 1 else "start"
        tx = x + (-6 if anchor == "end" else 8)
        body.append(f'<circle cx="{x}" cy="{y_axis}" r="7" fill="{BG0}" stroke="{acc}" stroke-width="2"/>')
        body.append(f'<circle class="ping" cx="{x}" cy="{y_axis}" r="7" fill="none" stroke="{acc}" stroke-width="1.5" style="animation-delay:{i*0.7}s"/>')
        body.append(f'<circle cx="{x}" cy="{y_axis}" r="3" fill="{acc}" filter="url(#glow-t)"/>')
        body.append(mono(title, tx, y_axis + 52, 13.5, TEXT, opacity=0.92, anchor=anchor, cls="fade"))
        body.append(mono(sub, tx, y_axis + 70, 11.5, FAINT, anchor=anchor, cls="fade"))

    defs = common_defs(U, W, H)
    style = AURORA_CSS + sheen_css(W) + """
.bar { animation: draw 2.4s cubic-bezier(.2,.8,.2,1) forwards; }
@keyframes draw { to { stroke-dashoffset: 0; } }
.ping { transform-box: view-box; transform-origin: center; animation: ping 2.6s ease-out infinite; }
@keyframes ping { 0% { transform: scale(1); opacity: .9; } 70%,100% { transform: scale(3); opacity: 0; } }
.fade { opacity: 0; animation: fade 1s ease-out .9s forwards; }
@keyframes fade { to { opacity: 1; } }
"""
    # `.ping` scales about the element bbox centre, which is the node centre.
    style = style.replace("transform-box: view-box;\n", "transform-box: fill-box;\n")
    style = style.replace(".ping { transform-box: view-box;", ".ping { transform-box: fill-box;")
    (OUT / "timeline.svg").write_text(shell(W, H, "\n".join(body), defs, style))


# ── 4. divider ────────────────────────────────────────────────────────────────
def build_divider():
    W, H = 1200, 26
    # <rect>, not <line> — a zero-height bbox degenerates an objectBoundingBox gradient.
    body = f"""
<rect x="0" y="12" width="{W}" height="2" fill="url(#dl)"/>
<g class="run">
  <circle cx="0" cy="13" r="3.5" fill="{CYAN}" filter="url(#dg)"/>
  <rect x="-70" y="12" width="70" height="2" fill="url(#tail)"/>
</g>"""
    defs = f"""
<linearGradient id="dl" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0%" stop-color="{MAGENTA}" stop-opacity="0"/>
  <stop offset="25%" stop-color="{MAGENTA}" stop-opacity="0.55"/>
  <stop offset="50%" stop-color="{VIOLET}" stop-opacity="0.75"/>
  <stop offset="75%" stop-color="{CYAN}" stop-opacity="0.55"/>
  <stop offset="100%" stop-color="{CYAN}" stop-opacity="0"/>
</linearGradient>
<linearGradient id="tail" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0%" stop-color="{CYAN}" stop-opacity="0"/>
  <stop offset="100%" stop-color="{CYAN}" stop-opacity="0.9"/>
</linearGradient>
<filter id="dg" x="-300%" y="-300%" width="700%" height="700%"><feGaussianBlur stdDeviation="3"/>
  <feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>
"""
    style = f"""
.run {{ transform-box: view-box; animation: sweep 6s cubic-bezier(.65,0,.35,1) infinite; }}
@keyframes sweep {{ 0% {{ transform: translateX(-80px); opacity: 0; }} 10%,90% {{ opacity: 1; }}
                   100% {{ transform: translateX({W + 80}px); opacity: 0; }} }}
"""
    (OUT / "divider.svg").write_text(shell(W, H, body, defs, style))


# ── 5. footer ─────────────────────────────────────────────────────────────────
def build_footer():
    W, H, U = 1200, 170, "f"
    body = [card(U, W, H, rx=22)]
    body.append(
        f'<text x="{W//2}" y="78" font-family="{SANS}" font-size="34" font-weight="800" '
        f'fill="url(#word-f)" text-anchor="middle" letter-spacing="1.5" filter="url(#glow-f)">'
        f'let\'s build something that outlives the demo</text>'
    )
    body.append(mono("// thanks for scrolling — the source of this README is in the repo", W // 2, 110, 12.5, MUTED, anchor="middle"))
    dots = "".join(
        f'<circle cx="{W//2 - 34 + i*17}" cy="138" r="3.5" fill="{ACCENTS[i % len(ACCENTS)]}" '
        f'class="dot" style="animation-delay:{i*0.16:.2f}s"/>'
        for i in range(5)
    )
    body.append(dots)
    defs = common_defs(U, W, H, rx=22) + f"""
<linearGradient id="word-f" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0%" stop-color="{PINK}"/><stop offset="50%" stop-color="{TEXT}"/><stop offset="100%" stop-color="{CYAN}"/>
</linearGradient>
"""
    style = AURORA_CSS + sheen_css(W) + """
.dot { transform-box: fill-box; transform-origin: center; animation: bob 1.6s ease-in-out infinite; }
@keyframes bob { 0%,100% { transform: translateY(0); opacity: .45; } 50% { transform: translateY(-7px); opacity: 1; } }
"""
    (OUT / "footer.svg").write_text(shell(W, H, "\n".join(body), defs, style))


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    build_hero()
    build_stack()
    build_timeline()
    build_divider()
    build_footer()
    for f in sorted(OUT.glob("*.svg")):
        print(f"  ✔ {f.relative_to(OUT.parent)}  ({f.stat().st_size // 1024 or 1} KB)")
