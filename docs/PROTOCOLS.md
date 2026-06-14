# The five protocols

The full description of what gets installed. Read this if you want to understand what you're committing to before you run the wizard.

Each protocol has the same shape:
1. **The verb** -- what you actually do
2. **Why it works** -- the behavioral science or operational observation underneath
3. **Where it lives** -- which file, which slash command, what schedule
4. **How to grade yourself** -- what 8/10 looks like

Before the protocols, two things give the system its shape: the three pillars and the Daily Punchlist. Both apply across every protocol below.

---

## The three pillars

Same framing as Grit Collective. Every action the system surfaces lives in one of three places.

- **Physical** -- the body. Movement, strength, endurance, sleep, mobility, the things that show up if you neglect them long enough.
- **Mental** -- the mind. Deep work, deliberate practice, strategy, decisions, learning. Work lives here. Your PRD is mental. Your code review is mental. Your reading is mental.
- **Emotional** -- the harder thing between the two. The conversations you keep parking. The people you owe presence to. The hard call. The apology. The Sunday with your kids that does not get photographed.

Work does not get a fourth bucket. It sits inside Mental. That choice is on purpose. If work had its own pillar, you would optimize the work and let the other two atrophy. You already know what that looks like.

The pillars are the lens, not the gate. The floor stays one 1000-second sweep a day, any pillar. The system surfaces 7-day balance as ambient signal so you can see what you have been neglecting. It does not lecture you about it.

---

## The Daily Punchlist

This is the engine. It is what the system does for you every morning so you do not have to think.

The installer connects to the data sources you already use:

- Calendar (Google, Apple, Outlook)
- Work messaging (Slack)
- Meeting transcripts (Granola or equivalent)
- Physical tracking (Strava, Apple Health, Garmin)
- Family and personal calendar
- Optionally: Linear, Notion, GitHub, Asana

Every morning, the punchlist generator reads the last 24 to 48 hours of activity across those sources, plus your `OPERATOR.md` pillar context, plus your `pursuits-parking-lot.md`, plus your recent logs. Then it produces a stack-ranked list of 1000-second actions across the three pillars.

**In v2.1.0 the engine learns from your logs, not just from external sources.** Every morning the engine reads:
- Your last 14 days of `log/sweeps.md` (what you actually did, whether you accepted the default or overrode, what category you overrode to)
- Your last 4 weeks of `log/kills.md` (what you decided not to do, tagged by category)
- Your last 4 weeks of `log/commitments.md` (your witness commitments and their outcomes)
- Yesterday's `PUNCHLIST.md` (what was promoted, what got marked done, what got skipped)
- `bundles/witness-this-week.md` if it exists (so unsent drafts can be surfaced)

That data drives the ranking:
- Items you completed in the last 3-5 days drop out of the candidate list
- Categories you killed get downweighted; matches go straight to "Proposed skips"
- Categories you overrode the default to 2+ times in 7 days get promoted into the suggested-default position
- Parked outcomes get auto-decomposed into 1-2 next-physical-actions and surfaced with a `★` badge

The output is a single file at `1000-second-system/PUNCHLIST.md`. The shape:

- **Floor:** one 1000s sweep a day. Suggested default is promoted at the top with a one-line reason citing the learning signal that drove it ("override-promoted from side practice -- you've chosen it 5 of 7 days").
- **7-day pillar coverage indicator:** P 5/7 · M 7/7 · E 2/7. Ambient. Informs the default suggestion when one pillar is under-served. Never enforced.
- **Physical section:** stack-ranked items, each with a one-line why and a source citation. Parked-outcome items (`★`) appear here.
- **Mental section:** same.
- **Emotional section:** same. Honest if the bucket is empty today. Parked outcomes get preferential surfacing here when coverage is ≤2/7.
- **Proposed skips:** what the system filtered out as low-leverage noise PLUS anything matching a category you killed in the last 2 weeks. You confirm or override.
- **Tonight's primary slot:** your placed sweep window from `OPERATOR.md`. If the slot held ≤2/5 last week, a one-line slot revision suggestion appears here.
- **Unsent draft surface (when applicable):** if your witness draft sat unsent >48 hours, a one-line note in the footer.
- **Stale-state lead line (when applicable):** if you skipped 2+ days, the output leads with "You missed N days. Re-ranking from sources, dropping anything that timed out."

The ranking logic prioritizes compounding over urgency. High-compounding items rise to the top unless something is both urgent AND irreversible. Most of what feels urgent is not.

The punchlist refreshes when you run `/1000seconds`. A silent cloud routine can regenerate it at a fixed time each morning if you opt in.

The system never invents context. If a pillar has nothing in it today AND the parking lot is empty for that pillar, the punchlist says so plainly. The Emotional pillar especially: the system errs conservative because the cost of inventing relational obligations is higher than the cost of leaving a section empty.

---

## Protocol 1 -- The Daily 1000

(Renamed in v2.2.0. Was "The 1000 Second Sweep" through v2.1.0. The word "sweep" implied clearing through things, which is the opposite of what the protocol does. You're not sweeping anything -- you're putting 1000 seconds onto one specific thing. The new name names the action plainly.)

### The verb

Once a day, you put 16 minutes and 40 seconds (1000 seconds) onto the single highest-leverage item from today's punchlist, in one block, with no context-switching.

That's it. No phone. No email tab. No second monitor pulling at your peripheral. One block, one thing, sixteen minutes forty.

You do not pick the item from a blank page. The punchlist already ranked the queue and promoted a default. You run `/1000seconds`, see the queue, then either start the timer on the default (or your override) or type `q` to exit without starting. Same single command serves both "morning peek" and "slot-time start."

### Why it works

1000 seconds is the smallest unit that counts as evidence to yourself that you did the thing. Shorter and you can dismiss it. Longer and you start dodging it.

The behavioral science: Gollwitzer's work on implementation intentions shows that "I will do X at Y time in Z place" produces a 2-3x increase in follow-through over vague intent. Huang on chunking confirms that small, fixed-duration blocks compound where variable-duration sessions do not.

The operational observation: 16:40 is the threshold below which most operators stop tracking and above which most operators stop starting. It threads the needle.

The punchlist's role: it removes the choice anxiety. Picking what to put your 1000 on is the part of the protocol that fails most often when you are tired. The system pre-decides so you do not have to.

### Where it lives

- **File:** `protocols/01-sweep.md` -- personalized to your placed slot from Part 1 of the interview. Filename kept stable from v2.1.0 to avoid migration churn; internally documents "The Daily 1000."
- **Command:** `/1000seconds` (shows the punchlist and either starts your 16:40 timer or exits cleanly if you just wanted to peek)
- **Log:** `log/sweeps.md` -- append-only entry per 1000 logged, tagged with pillar. Filename kept stable from v2.1.0.
- **Schedule:** Daily, at your placed slot
- **Optional routine:** Daily 1000seconds reminder at your placed slot (off by default), morning punchlist regeneration (on by default if you opted into silent routines)

### How to grade yourself

- **9/10:** 5-6 1000s per week, started on time, on the punchlist's top item or a deliberate override
- **7/10:** 4-5 1000s per week, started within 15 minutes of slot
- **5/10:** 2-3 1000s per week, sometimes started late, occasionally on something off the punchlist with no reason logged
- **3/10:** Less than 2 1000s per week, or "split" the time across multiple things

Below 5/10 for two consecutive weeks is the drift signal. The system will surface it if you have the drift-alert routine on.

---

## Protocol 2 -- The Leverage Matrix

### The verb

Once a week, you run a 2x2 on whatever filled your week. The axes are **compounding** (does this generate more leverage over time) and **reversibility** (can you undo it if it's wrong).

Anything in the "low compounding, low reversibility" quadrant dies. Anything in "high compounding, high reversibility" gets prioritized. The other two quadrants need a real conversation.

The matrix kills about 60% of most operators' backlogs the first time they run it. After the first run, it kills about 10-20% per week of new commitments before they become commitments.

In v2.0.0, the matrix no longer requires you to paste a backlog. The system ingests your week from the same connected sources that feed the punchlist: meetings you took, threads you participated in, items you @-mentioned on, tasks you closed. It pre-fills the four quadrants. Your job is to confirm or correct, then confirm kills.

### Why it works

"Should I do this" is too vague a question to answer well when you're tired. "Where does this sit on the 2x2" is a question you can answer in 30 seconds because it's two binary calls.

The two axes were chosen carefully:
- **Compounding** captures whether the work makes future work easier or just adds to throughput
- **Reversibility** captures the cost of being wrong

Other axes I considered and rejected: importance (too vague), urgency (creates the urgency trap), enjoyment (creates the comfort trap), feasibility (creates the smallness trap).

### Where it lives

- **File:** `protocols/02-leverage-matrix.md` -- references your connected sources
- **Template:** `templates/leverage-matrix.md` -- pre-filled by the system, you edit
- **Command:** Run as part of `/friday`
- **Log:** Kills written to `log/kills.md`
- **Schedule:** Weekly, Friday afternoon
- **Optional routine:** Friday pre-compose at Thu 23:00 (on by default -- silent prep, no notification). Pulls source data and stages the matrix so Friday's `/friday` is 80% done before you sit down.

### How to grade yourself

- **9/10:** Run weekly, kill at least 1-2 things per run, no second-guessing
- **7/10:** Run weekly, kill occasionally, sometimes second-guess kills mid-week
- **5/10:** Skip every 3-4 weeks, struggle to kill anything
- **3/10:** Run sporadically, treat as journaling instead of triage

---

## Protocol 3 -- The Agent Brief

### The verb

When you hand work to an LLM (or to a person, but mostly an LLM), you write a 5-part brief first.

The five parts:
1. **Goal:** what you want done, one sentence
2. **Constraints:** budget, scope, what to NOT touch
3. **Success criteria:** how you'll know it's good
4. **Format:** the output shape (markdown doc, code diff, slide outline)
5. **Anti-patterns:** things this should NOT look like

If you can't write a brief in 4 minutes, the work isn't ready to delegate.

### Why it works

The brief IS the work. The agent (human or LLM) just executes the brief. Most "bad output" complaints are actually bad-brief complaints.

A side effect of writing briefs: you find out which of your ideas weren't actually shaped enough to commit to.

### Where it lives

- **File:** `protocols/03-agent-brief.md`
- **Template:** `prompts/agent-brief-template.md` -- generic 5-part template
- **Seeded example:** `prompts/seeded-example.md` -- pre-filled brief generated from a deferred item the system saw in your sources
- **Command:** `/brief` -- walks through the 5 parts interactively
- **Schedule:** Ad-hoc, whenever you're delegating

### How to grade yourself

Brief quality is the grade. Grade your first-pass briefs honestly. Most operators grade their first-pass briefs at 6/10. The second pass, after one rewrite, grades at 8.5/10. That delta is the protocol.

---

## Protocol 4 -- The Weekly Kill List

### The verb

Friday at 4pm, you write down what you stopped doing this week, and why. Not what you did. What you killed.

This sounds like nothing. After 8 weeks you have a paper trail of your taste calibrating in real time. The killed-stuff log is more useful than the shipped-stuff log because it tells you what you've gotten better at not doing.

### Why it works

Most people track wins. Wins are vanity metrics; you'd track them whether or not you got better. Kills require taste -- naming the trade-off, the cost of the kill, the thing you said no to that would have been easier to say yes to.

After 12 weeks of weekly kill lists, the pattern of your kills tells you what you're becoming. That information is not available from looking at your shipped work.

### Where it lives

- **File:** `protocols/04-kill-list.md`
- **Command:** Run as part of `/friday`. The matrix surfaces a kill list candidate from your week's connected sources; you add anything else that did not show up there.
- **Log:** `log/kills.md` -- append-only entry per week
- **Schedule:** Weekly, Friday 4pm

### How to grade yourself

- **9/10:** 3-5 kills per week, named with the trade-off, no rationalization
- **7/10:** 2-3 kills per week, sometimes light on the trade-off
- **5/10:** 1 kill per week, often vague ("checked email less" is not a kill)
- **3/10:** No kills, treats the list as a complaint log

---

## Protocol 5 -- The Public Commitment Slot

### The verb

Once a week, in front of a small group or a specific person, you commit to one 1000-second block of work, by name, by time. You name the thing. You name when. You name where. You say it in a place where someone else will see it.

The witness is the protocol. The slot without the witness is a journal entry.

### Why it works

Ariely and Karlan's commitment-device research is unambiguous: external witnesses lift follow-through by 15-25 percentage points. The effect is larger when the witness is a peer (not a coach) and when the commitment is specific (not aspirational).

This protocol is also the bridge to Grit Collective. A solo witness slot held weekly for a month is the muscle. A defined hard outcome with a group of 8 in a Pursuit is the next scale of the same mechanic.

### Where it lives

- **File:** `protocols/05-commitment-slot.md` -- personalized to your witness from Part 3 of the interview
- **Command:** Run as part of `/friday` (drafts the message); paste into your witness's channel when ready
- **Log:** `log/commitments.md` -- append-only entry per week (text + outcome at week end + self-grade)
- **Bundle:** `bundles/witness-this-week.md` -- the actual draft message
- **Schedule:** Weekly, Friday afternoon (draft) → send when ready
- **Optional routine:** Saturday morning send nudge (off by default)

### How to grade yourself

- **9/10:** Witness slot held every week, specific commitment, sent by Saturday, outcome marked honestly
- **7/10:** Held most weeks, sometimes vague commitment, sometimes late send
- **5/10:** Held every other week, often skipped during travel or busy weeks
- **3/10:** Held rarely, witness has stopped tracking

If you've been holding the witness slot at 8/10+ for four weeks and you have a hard outcome in your parking lot, you're ready for a Grit Pursuit. Run `/pursuit-check` to confirm.

---

## How the protocols fit together

The protocols are not independent. They form a weekly cadence on top of the daily punchlist.

| When | What | Driven by |
|---|---|---|
| Every morning (silent) | Punchlist regenerates from connected sources | Cloud routine, off if not opted in |
| Any time, daily | `/1000seconds` -- shows the punchlist, optionally starts your 16:40 timer | Protocol 1 |
| Ad-hoc when delegating | `/brief` | Protocol 3 |
| Friday 4pm | `/friday` -- matrix → kills → next week's commitment → witness draft | Protocols 2 + 4 + 5 |
| Saturday | Send the witness message | Protocol 5 |
| Monthly or when data warrants | `/pursuit-check` -- read logs, surface graduation signal | Cross-protocol |

That's the whole rhythm. One daily verb. One weekly ritual. The system runs you, not the other way around.
