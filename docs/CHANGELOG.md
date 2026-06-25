# Changelog

All notable changes to The 1000 Second Method installer.

## v2.4.0 -- 2026-06-24

The health release. Oura and Strava become first-class Physical-pillar sources, and the recommendation engine starts choosing load vs. recovery from real data.

What changes:
- **Oura + Strava are first-class sources.** No MCP exists for either, so the agent reads their REST APIs directly with your own credentials, stored locally in the gitignored `system/health/`. Nothing routes through a server I control. `/sources` walks the one-time setup (Oura token; Strava developer-app + OAuth) and can test or remove them.
- **The Physical pillar now reads recovery.** The engine reads a normalized `system/health/health-data.json` and applies recovery rules: low readiness or poor sleep demotes hard training and promotes mobility; 2+ days since a workout promotes movement; a workout already logged today stops it double-pushing. If neither source is connected, nothing changes.
- **New Health tab on the render.** Beside Today and Log: today's readiness, sleep, HRV, and resting HR with green/amber/red status, two-week trend sparklines (inline SVG, no chart libraries), recent Strava training, and a one-line "how this shaped tonight's Physical pick." Read-only.
- **One small script.** `system/health/strava_token.py` (stdlib only) handles the Strava 6-hour token refresh and rotation. Everything else (Oura GETs, Strava GETs, normalization) is agent-inline.

What stays the same:
- Five protocols. Same names. Same IP.
- The single-file, paste-one-URL install. No backend, no account -- your health data and credentials live in your workspace.
- Voice rules. Sources sovereign. Free, MIT.

Breaking: nothing. v2.3.x installs run `/1000s-update` to pick up the health integration, then `/sources` to connect Oura or Strava. Operators who connect nothing see no change. Logs and `OPERATOR.md` preserved.

## v2.3.0 -- 2026-06-24

The honest-render release. The web view stops pretending it tracks anything on its own, and it shows up without being asked.

What changes:
- **`/1000seconds` renders the web view automatically.** Running the daily command now generates and opens `today.html` at the end of its run, in addition to the terminal output. You no longer have to remember `/render` -- it stays as the on-demand refresh.
- **The render is an honest companion, not a fake tracker.** A browser page cannot write to your local files, so it never could log a 1000 by itself. The page now says so: a companion-view note up top, and checking an item (or finishing the in-page timer) copies a ready-to-paste line you drop back into your agent (Claude or ChatGPT), which keeps the real `log/sweeps.md`. The agent owns the log; the page is the surface.
- **Finishing the timer stays visibly done.** The hero used to snap back to the "Start the 1000" button a few seconds after you finished. It now settles into a persistent "done on this page" state (with a copy-again and an Undo) that survives a reload, so a completed 1000 stays on screen until you confirm it with your agent.
- **Removed two commands that never existed.** The checkbox told you to run `/sync` and the timer copied a `/1000seconds log "..."` command -- neither is a real command. Both are gone, replaced by the paste-ready confirmation line.

What stays the same:
- Five protocols. Same names. Same IP.
- The single-file, paste-one-URL install. No backend, no account, no phone sync -- the log still lives in your workspace.
- `/render` still exists. The page is still read-only with respect to your files.

Breaking: nothing. v2.2.x installs run `/1000s-update` to pick up the auto-render step in `/1000seconds` and the manual-refresh note on `/render`. The honest copy lands on its own, since the template is fetched fresh on every render. Logs and `OPERATOR.md` preserved.

## v2.2.1 -- 2026-06-14

The public-release hardening pass. No new protocols, no new mechanics -- this is the release that makes the installer safe to hand to a stranger from a single pasted URL.

What changes:
- **The install and self-update URLs are real.** They shipped with a `[brent]` placeholder, which meant the headline install link and the `/1000s-update` fetch both pointed nowhere. Both now resolve to `github.com/TottyBuilds/1000-second-method`.
- **`/render` is actually installed.** v2.2.0 announced the `/render` command and its HTML view, but the installer never wrote the command and the template was a loose mock. `/render` now installs as the seventh always-on command. It fetches a data-driven template (`docs/render-template.html`) and fills in your real punchlist, so the view stays in sync with the engine and can evolve through the newsletter without a re-install.
- **One version, stamped consistently.** A new Manifest block at the top of `INSTALL.md` is the single source of truth for version, file count, command list, and protocol names. Generated files (`OPERATOR.md`, your README, `.installed-version`) now all stamp the same version instead of drifting between 2.0.0 and 2.2.0.
- **A self-check before "done."** The installer now lints its own output before closing: no em dashes, no leftover `[PLACEHOLDER]` tokens, matching version stamps, the expected command set. That is what catches the class of bug this release fixes.
- **Voice fixes.** Removed the em dashes that had crept into the engine template, `PRINCIPLES.md`, and this changelog. The "no em dashes" rule now holds across every shipped and generated file.
- **Honest counts.** "~17 files" corrected to "~18"; the generated README's `/routines` mention is now conditional, so it never points at a command that wasn't installed.

What stays the same:
- Five protocols. Same names. Same IP.
- The single-file, paste-one-URL install. The installer is still one document you point Claude Code at -- that simplicity is the product.
- Voice rules. Sources sovereign. Free, MIT, lives in your workspace.

Breaking: nothing. v2.2.0 installs can run `/1000s-update` to pick up `/render`, the version stamp, and the corrected URLs. Logs and `OPERATOR.md` preserved.

## v2.2.0 -- 2026-06-07

The naming-and-rendering release. Protocol 1 gets a more honest name, and the system gets a real visual + interaction layer.

What changes:

- **Protocol 1 renamed: "The 1000 Second Sweep" → "The Daily 1000."** The word "sweep" implied clearing/passing through, which is the opposite of what the protocol does -- you're putting 1000 seconds ONTO one specific thing, not sweeping through anything. The new name names the action plainly and matches how operators already talk about the unit ("did your 1000 today?"). The five-protocols-don't-rename rule in PRINCIPLES.md updated: concepts stay stable, names can be sharpened when they're materially wrong. This is the first and so far only rename.
- **The internal file `protocols/01-sweep.md` and the log file `log/sweeps.md` keep their stable filenames** to avoid migration churn for v2.1.0 installs. Filenames are internal; the protocol's display name is what changes.
- **New `/render` command** (ships v2.2.0). Generates an HTML view at `1000-second-system/today.html` that the operator opens in their browser. The view shows tonight's 1000 with the override-promoted reason, other candidates from today's punchlist, parked outcomes on hold, what the system filtered out, and a "weekly loop" surface that maps the daily 1000 to the rest of the commands (`/friday`, `/brief`, `/pursuit-check`, `/sources`).
- **The render is interactive**: a real in-browser 16:40 timer (no need to switch to the terminal), checkboxes per item (state in localStorage), and clipboard-bridge sync that copies a paste-ready `/1000seconds log` command for the operator to reconcile with `log/sweeps.md` on demand.
- **The render has a "Log" tab** showing your evidence: streak count framed as evidence (not as a streak-shame device), 30-day count of completed 1000s, pillar split with a colored bar, a four-week calendar grid color-coded by pillar of the day's 1000, and a chronological timeline of recent 1000s with the why behind each pick.
- **Render footer surfaces the Every Expert link** (`everyexpert.com/totty`) -- the right CTA for an installed operator wanting a 45-minute senior read on a pattern, not the install CTA which would be incoherent here.

What stays the same:
- Six slash commands plus optional `/routines` (now plus `/render` = seven). The principle of "no new daily commands" stays -- `/render` is read-only and ad-hoc.
- The five protocol concepts. Only Protocol 1's display name moves.
- Filenames inside `1000-second-system/` -- nothing renamed on disk for v2.1.0 installs.
- The learning rules in the punchlist engine from v2.1.0. The render is a NEW surface, not a replacement.
- Voice rules. Sources sovereignty. Free, MIT, lives in your workspace.

Breaking: v2.1.0 installs need `/1000s-update` to pick up the rename in `protocols/01-sweep.md` body text and the new `/render` command. Log files and OPERATOR.md preserved.

## v2.1.0 -- 2026-06-05

The learning release. The punchlist engine stops being amnesiac and the install stops leaking high-need operators at Phase 0.

What changes:
- **The punchlist engine learns from its own logs.** It now reads `log/sweeps.md`, `log/kills.md`, `log/commitments.md`, yesterday's `PUNCHLIST.md`, and `bundles/witness-this-week.md` as inputs alongside external source data. Concretely:
  - Completed sweep items are dropped from candidate lists for 3-5 days.
  - Categories the operator killed in the last 2-4 weeks get downweighted; matches go straight to "Proposed skips."
  - Categories the operator overrode the suggested default to 2+ times in 7 days get promoted into the suggested-default position.
  - Parked outcomes from `pursuits-parking-lot.md` get auto-decomposed into 1-2 next-physical-actions per parked outcome and surfaced with a `★` badge. Preferential surfacing when source signal is thin or a pillar is quiet.
  - One parking-lot item per pillar per day, max.
- **Slot adherence check.** The engine compares the placed slot to actual sweep times in `log/sweeps.md` weekly. If the placed slot held ≤2/5 last week, the daily punchlist footer surfaces a one-time suggestion to revise the slot. No automatic change.
- **Stale-state recovery.** If `PUNCHLIST.md` is >48h old (operator skipped 2+ days), the new output leads with "You missed N days. Re-ranking from sources, dropping anything that timed out." Yesterday's queue is not shown verbatim.
- **Unsent witness draft surface.** If `bundles/witness-this-week.md` sat unsent >48h with no matching `log/commitments.md` entry, the daily punchlist footer surfaces a one-line note: "Witness draft sat unsent since [date]. Send via `/friday` or kill it."
- **Phase 0 non-Claude-Code branch.** The installer now detects when an operator is not in Claude Code (paste into ChatGPT, Claude.ai web, notes app) and exits cleanly with a pointer to `brenttotty.com/installer` for the newsletter signup, instead of trying to walk through an install that cannot complete.
- **Phase 1.2 tiered source paths.** Three explicit paths: "Calendar only" (60 seconds, minimal), "Full wire-up" (5-15 min, recommended), "Skip for now" (write files from interview alone, add sources later via `/sources`). All three land at Phase 2 with files written.
- **Phase 1.2 escape hatch.** If two source connections fail in a row, the installer offers to skip the remaining sources and proceed to file generation. Recovers the most painful failure mode (stalling AFTER the interview but BEFORE Phase 2 writes files, leaving no anchor to return to).
- **Phase 3 witness hardening.** The interview no longer accepts "solo until Week 4" as the first answer to "who's your witness?" Three softer options are surfaced first: a peer at work, partner/family member, public log. Solo is only accepted after the operator sees the alternatives.
- **`/friday` confirmation step.** After drafting the witness message, the command asks "Sending now or later this weekend?" If now, the operator confirms send and `log/commitments.md` gets a `sent_at` timestamp. If later, a `bundles/.witness-pending` flag is created; the daily punchlist surfaces the unsent draft until resolved.
- **Phase 4 routines collapse.** Twelve per-routine yes/nos collapsed into three category-level questions: silent ops (yes/no), active reminders (where: email/Telegram/Slack/skip), reactive alerts (yes/no). Operators tune individual routines later via `/routines`.
- **Inline first `/1000seconds` at end of Phase 3.** The install session no longer ends without the operator seeing a real punchlist generated from their actual data. This is the load-bearing "this saw me" moment that predicts retention.

What stays the same:
- Five protocols. Same names. Same IP. Mechanics get sharper, names do not change.
- Six slash commands (plus optional `/routines`). No new commands. The simulation explicitly recommended against adding any.
- Voice rules. First person, plain, no hype, no em dashes.
- The graduation path. Every Expert, Backstage, Grit Collective.
- Sources sovereign. Connected source data still lives in the operator's Claude session and the third-party services they already authenticate with. The learning rules read the operator's OWN logs (already on their disk); no new server, no new database, no new phone-home.
- Free. MIT. Lives in your workspace.

Breaking: v2.0.0 installs need `/1000s-update` to pick up the new engine prompt and command behavior. Logs and `OPERATOR.md` are preserved. The new `bundles/.witness-pending` flag is created on first `/friday` post-update.

Rationale: a 50-persona simulation of v2.0.0 (8 deep personas + 42 sketches, install + 14-day usage projection, multi-agent dispatch) surfaced a converging pattern across all 5 batches: the installer earns the operator's investment and the daily engine spends it. The interview consistently surfaces the operator's real unspoken thing (deferred book, unmade call, parked outcome). Then the engine regenerated from raw sources each morning and ignored its own outputs. By Day 7 the engine started feeling static. By Day 14 about half the completers were drifting. v2.1.0 closes that gap. Full simulation findings: `Brent Totty Personal Brand/.simulation/SYNTHESIS.md`.

## v2.0.0 -- 2026-05-24

The watching release. The installer stops asking you what you do all day and starts observing it.

What changes:
- **The Daily Punchlist.** New core output. The system reads your connected sources (calendar, Slack, meeting transcripts, physical tracking, family/personal calendar) every morning and produces a stack-ranked list of 1000-second actions for the day, organized by three pillars: Physical, Mental, Emotional. Floor stays one sweep a day. Anything beyond that is bonus.
- **Three pillars.** Same framing as Grit Collective. Work lives inside Mental, not as a fourth bucket. The pillars are visual organization, not a daily gate. Balance is surfaced over a 7-day window, never enforced day to day.
- **Source connections replace the tools interview.** Phase 1 Part 2 is now MCP server setup, not "what task manager do you use." The system learns from real data, not self-report.
- **Lighter interview.** Leverage signal is no longer asked up front; it gets inferred from the first week of connected source data and surfaces during the first `/friday`. The Day 0 interview is now ~12 minutes instead of ~20.
- **New `/1000seconds` command** (replaces v1's `/sweep`). One verb for the daily action. Shows the punchlist and either starts your 16:40 timer or exits cleanly if you just wanted to peek. The peek-versus-commit choice is a branch inside one command, not two separate commands.
- **Sources are sovereign.** Connected source data lives in your Claude session and on the third-party services you already use (Google, Slack, etc.). It does not pass through any Brent-controlled server or database. The "no phone home" promise narrows to "no phone home TO ME."

What stays the same:
- Five protocols. Same names. Same IP. The mechanics get sharper. The names do not change.
- Voice rules. First person, plain, no hype, no em dashes.
- The graduation path. Every Expert, Backstage, Grit Collective.
- Free. MIT. Lives in your workspace.

Breaking: v1.0.0 installs will need to run `/1000s-update` to migrate. Logs and `OPERATOR.md` are preserved. New files (`PUNCHLIST.md`, `system/`, pillar context section in `OPERATOR.md`) are added.

## v1.0.0 -- 2026-05-19

First public release.

What this ships:
- The wizard (`INSTALL.md`) -- a ~20-minute interview that generates a personalized operating system in your workspace
- Five protocols, installed as files: the 1000 Second Sweep, the Leverage Matrix, the Agent Brief, the Weekly Kill List, the Public Commitment Slot
- Five slash commands: `/sweep`, `/friday`, `/brief`, `/pursuit-check`, `/1000s-update`
- Optional cloud routines via Claude routines for silent log aggregation, weekly review pre-compose, and graduation-signal detection
- A graduation path that surfaces when you're ready to scale solo work into 1:1 (Every Expert or Backstage) or group (Grit Collective)

Brent's notes on what's deliberately minimal in v1.0.0:
- No videos. The protocols teach themselves through the files in your workspace.
- No course. Installation is the product.
- No paywall. The installer is free. Money lives in the tier you graduate into when you're ready.
- No nudges. The system records and reflects. It does not pester.

What's coming next, based on dogfooding and early operator notes:
- Sharper Agent Brief examples for common deferred-task patterns
- A `/routines` command for managing cloud routines without re-running the wizard
- Better signal recognition in `/pursuit-check` as more operator log data accumulates
