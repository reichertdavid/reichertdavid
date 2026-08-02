# Setup

> This file is just notes for you — GitHub only renders `README.md` on a profile.

## 1. Make it your profile repo

A GitHub profile README lives in a repo **named exactly like your username**, on the default branch, public.

```bash
cd reichertdavid
git init -b main
git add .
git commit -m "profile: neon glass README"
gh repo create reichertdavid --public --source=. --remote=origin --push
```

If the repo already exists, just `git remote add origin …` and push instead.

## 2. Turn on the snake

`.github/workflows/snake.yml` renders your contribution graph as an animated snake and pushes it to an `output` branch.

1. Push the repo (step 1).
2. **Settings → Actions → General → Workflow permissions → Read and write permissions.**
3. **Actions → generate snake → Run workflow** once, so the `output` branch exists before someone loads your profile. It re-runs daily after that.

Until that first run finishes, the snake section shows a broken image — that's expected.

## 3. Editing the artwork

Everything visual is generated:

```bash
python3 tools/build_assets.py     # rewrites assets/*.svg
```

Knobs, all near the top of `tools/build_assets.py`:

| What | Where |
| :-- | :-- |
| Colours | `MAGENTA / VIOLET / CYAN / PINK / MINT` |
| Tech chips | `ROW_A` (languages & frontend) and `ROW_B` (data & infra) |
| Marquee speed | `marA` / `marB` durations in `build_stack()` |
| Headline, tagline, rotating lines | `build_hero()` — the `lines` list |
| Stat pills | `build_hero()` — the `pills` list |
| Timeline milestones | `build_timeline()` — `bars` and `nodes` |

**Prune `ROW_A` / `ROW_B`.** I filled them with a broad fullstack set to match "a little bit of all" — delete anything you'd rather not be asked about in an interview.

To preview locally without pushing:

```bash
python3 -m http.server 8731
open http://127.0.0.1:8731/tools/preview.html
```

## 4. Things worth knowing

- **Cache busting.** GitHub proxies images through camo and caches hard. After changing an SVG, bump the URL (`./assets/hero.svg?v=2`) if the old one sticks around.
- **Animations.** Pure SVG + CSS keyframes, no JS — that's the only kind that survives GitHub's `<img>` sandbox.
- **Fonts.** Nothing external is loaded; every text run is pinned with `textLength`, so the layout holds up on any machine.
- **Light mode.** The cards carry their own dark background on purpose, so they read as intentional panels on GitHub's light theme instead of needing a second asset set.
- **Third-party cards.** The stats / streak / trophy / activity-graph images come from community services (`github-readme-stats`, `streak-stats.demolab.com`, `github-profile-trophy`, `github-readme-activity-graph`). They occasionally rate-limit or go down. If one is flaky for you, delete that line — the page still holds together.
- **Contact links get scraped.** Anything you put in the badge row at the top of the README — an address, a handle — is public and machine-readable. Prefer a profile link over a raw address.
