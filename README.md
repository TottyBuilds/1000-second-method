# The 1000 Second Method

> *Five protocols. One install. The system watches so you can focus -- and learns as you go.*

A free, agent-native installer for operators who use AI like infrastructure, not magic.

You point Claude Code at the installer. It runs a 12-minute interview, connects to the data sources you already use (calendar, work messaging, meeting transcripts, physical tracking, family calendar), and writes a personalized operating system into your workspace.

From then on, every morning, the system produces a Daily Punchlist: stack-ranked 1000-second actions across three pillars -- Physical, Mental, Emotional -- pulled from what is actually happening in your life. Your job collapses to picking one and running it.

The floor is one 1000-second sweep a day. Anything beyond that is bonus.

**v2.1.0:** the punchlist engine now learns from your own logs -- every override, every kill, every parked outcome you wrote down at install. Day 1 it generates from raw sources. By Day 7 it starts feeling specific. By Day 14 it should feel like yours. If it doesn't, file an issue.

## Who this is for

Mid-career P/E/O leaders. Director-to-VP. AI-fluent but not chasing the next tool. Already performing well, want sharper systems for themselves, not just their teams. Skeptical of hustle content. The "I've read Atomic Habits, I don't need motivation, I need verbs" crowd.

If you've got great tools and a shit workflow, you're who I built this for.

## The three pillars

Same framing as Grit Collective. Every action the system surfaces sits in one of three places.

- **Physical** -- the body. Movement, strength, endurance, sleep, mobility.
- **Mental** -- the mind. Deep work, deliberate practice, strategy, decisions. Work lives here.
- **Emotional** -- the harder thing between the two. The conversations you keep parking. The people you owe presence to.

Work does not get its own bucket. That choice is on purpose. The pillars are visual organization, not a daily gate. Floor stays one sweep a day, any pillar. The system surfaces 7-day balance as ambient signal.

## What you get

The wizard installs five protocols into your workspace as files. Each one is the smallest thing that durably shifts a week:

1. **The Daily 1000** -- A daily 16:40 deep block on the punchlist's top item. (Renamed from "The 1000 Second Sweep" in v2.2.0 -- "sweep" implied clearing through things, but the protocol is the opposite: putting 1000 seconds onto one thing.)
2. **The Leverage Matrix** -- A weekly 2x2 (now ingested from your sources, not pasted) that kills about 60% of most operators' backlogs the first run
3. **The Agent Brief** -- A 5-part template for handing work to an LLM that turns 6/10 outputs into 8.5/10 outputs
4. **The Weekly Kill List** -- A Friday 4pm log of what you stopped doing, and why
5. **The Public Commitment Slot** -- A weekly witnessed commitment that lifts follow-through 15-25 percentage points

Full descriptions in [`docs/PROTOCOLS.md`](docs/PROTOCOLS.md).

Plus the Daily Punchlist (the engine that feeds Protocol 1) and seven slash commands for the daily and weekly cadence (including `/render` for a visual, in-browser view and `/sources` to manage source connections):

| Command | When | What |
|---|---|---|
| `/1000seconds` | Daily | Show today's punchlist. Either start your 16:40 on the top item (or override), or just peek and exit. |
| `/render` | Ad-hoc | Open today's punchlist as a web page -- in-browser 16:40 timer, checkboxes, and a Log tab of your evidence |
| `/friday` | Weekly | One ritual: matrix → kills → next week's commitment → witness message draft |
| `/brief` | Ad-hoc | Walk through the 5-part Agent Brief, paste-ready |
| `/pursuit-check` | When the data warrants | Read your logs, surface the graduation signal |
| `/1000s-update` | When the newsletter ships one | Pull installer improvements (preserves your local edits) |
| `/sources` | Ad-hoc | Manage connected data sources (add, remove, reconfigure, test) |

Optional cloud routines for silent background prep (morning punchlist regen, Friday pre-compose, signal aggregation) and reactive notifications (pursuit-readiness ping, drift alert). All opt-in, all preserve a no-nudge default.

## Connected sources

The system reads from data sources you already use. Each one is opt-in during install. None of them route through any server I control.

| Source | What it informs |
|---|---|
| Google / Apple / Outlook Calendar | Mental + Emotional items; placed slot collision check |
| Slack | Mental items (@-mentions, DM debt, parked threads) |
| Granola or other meeting transcripts | Mental items (unresolved decisions, action items) |
| Strava / Apple Health / Garmin | Physical items (gaps, recovery flags) |
| Family or personal calendar | Emotional items (relational commitments, missed presence) |
| Linear / Notion / GitHub / Asana | Backlog items for the weekly matrix |

Bring the ones you use. Skip the rest. The punchlist quality scales with how many honest sources you connect.

## What this is NOT

Not a course. Not a SaaS. Not paywalled. Not a template. Not a nudge machine.

Read [`docs/PRINCIPLES.md`](docs/PRINCIPLES.md) before complaining that it doesn't do something you wanted it to do.

## Install

Paste this into Claude Code:

```
Read this and install the 1000 Second Method into my workspace:
https://raw.githubusercontent.com/TottyBuilds/1000-second-method/main/INSTALL.md
```

Claude Code fetches the installer, runs the 12-minute interview, sets up your connected sources, generates a `1000-second-system/` folder in your workspace, and adds the slash commands.

The interview is conversational -- no forms. It asks about your whole life shape (work AND personal), your pillar context, your witness situation, then walks you through connecting the data sources you already use. The depth of your answers and the breadth of your connected sources determines the quality of your install.

## Run it for thirty days

That's the test. Thirty days of `/1000seconds` on weekdays. Four `/friday` rituals. One `/pursuit-check` if the signal warrants. Then grade yourself.

If you're at 8/10+ across the board and you've got a hard outcome in your parking lot, you're ready for the next tier. The installer's `WHEN_YOU_RE_READY.md` describes the three graduation paths.

## Graduation paths

When solo execution stops being enough, three tiers exist:

| Tier | What it is | When it's right |
|---|---|---|
| **Every Expert** -- `everyexpert.com/totty` | One-off intro session with me | You have a specific pattern or decision you want a senior read on |
| **Backstage** -- Kajabi product | Ongoing async relationship with me in your workspace | A recurring judgment gap that ongoing read time would solve |
| **Grit Collective** -- `gritcollective.com` | Group Pursuit, 10-22 weeks, expert in the chat | You have a defined hard outcome and want a crew committed alongside |

None of these gate the installer. They are what's available when the data in your own logs says you're ready.

## The newsletter

[**Time Well Spent**](https://brenttotty.com) ships Tuesdays. Essays plus installer updates (new prompts, new templates, sharpened slash command behavior, new source integrations). Subscribers get running improvements to their installed system, not just content.

## Versioning

Semantic. Current version is in [`docs/CHANGELOG.md`](docs/CHANGELOG.md). The five protocols are stable IP -- they will not be renamed. Everything else evolves through the newsletter cadence.

## Feedback

[GitHub issues](https://github.com/TottyBuilds/1000-second-method/issues) is the right channel. Bugs, friction, suggestions all welcome. I read weekly.

## License

MIT. Use it. Fork it. Build on it. If you ship something interesting, send me a link.

---

Brent Totty
[brenttotty.com](https://brenttotty.com)
