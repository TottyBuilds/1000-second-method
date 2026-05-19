# The five protocols

The full description of what gets installed. Read this if you want to understand what you're committing to before you run the wizard.

Each protocol has the same shape:
1. **The verb** — what you actually do
2. **Why it works** — the behavioral science or operational observation underneath
3. **Where it lives** — which file, which slash command, what schedule
4. **How to grade yourself** — what 8/10 looks like

---

## Protocol 1 — The 1000 Second Sweep

### The verb

Once a day, you spend 16 minutes and 40 seconds (1000 seconds) on the single highest-leverage thing on your list, in one block, with no context-switching.

That's it. No phone. No email tab. No second monitor pulling at your peripheral. One block, one thing, sixteen minutes forty.

### Why it works

1000 seconds is the smallest unit that counts as evidence to yourself that you did the thing. Shorter and you can dismiss it. Longer and you start dodging it.

The behavioral science: Gollwitzer's work on implementation intentions shows that "I will do X at Y time in Z place" produces a 2-3x increase in follow-through over vague intent. Huang on chunking confirms that small, fixed-duration blocks compound where variable-duration sessions do not.

The operational observation: 16:40 is the threshold below which most operators stop tracking and above which most operators stop starting. It threads the needle.

### Where it lives

- **File:** `protocols/01-sweep.md` — personalized to your specific placed slot from Part 1 of the interview
- **Command:** `/sweep`
- **Log:** `log/sweeps.md` — append-only entry per run
- **Schedule:** Daily, at your placed slot
- **Optional routine:** Daily sweep reminder at your placed slot (off by default)

### How to grade yourself

- **9/10:** 5-6 sweeps per week, started on time, on the single highest-leverage thing
- **7/10:** 4-5 sweeps per week, started within 15 minutes of slot, on one thing
- **5/10:** 2-3 sweeps per week, sometimes started late, occasionally on second-priority work
- **3/10:** Less than 2 sweeps per week, or "split" the time across multiple things

Below 5/10 for two consecutive weeks is the drift signal. The system will surface it if you have the drift-alert routine on.

---

## Protocol 2 — The Leverage Matrix

### The verb

Once a week, you run a 2x2 on whatever is filling your time. The axes are **compounding** (does this generate more leverage over time) and **reversibility** (can you undo it if it's wrong).

Anything in the "low compounding, low reversibility" quadrant dies. Anything in "high compounding, high reversibility" gets prioritized. The other two quadrants need a real conversation.

The matrix kills about 60% of most operators' backlogs the first time they run it. After the first run, it kills about 10-20% per week of new commitments before they become commitments.

### Why it works

"Should I do this" is too vague a question to answer well when you're tired. "Where does this sit on the 2x2" is a question you can answer in 30 seconds because it's two binary calls.

The two axes were chosen carefully:
- **Compounding** captures whether the work makes future work easier or just adds to throughput
- **Reversibility** captures the cost of being wrong

Other axes I considered and rejected: importance (too vague), urgency (creates the urgency trap), enjoyment (creates the comfort trap), feasibility (creates the smallness trap).

### Where it lives

- **File:** `protocols/02-leverage-matrix.md` — personalized to your typical backlog domains (work, personal, both)
- **Template:** `templates/leverage-matrix.md` — blank 2x2 you fill weekly
- **Command:** Run as part of `/friday`
- **Log:** Kills written to `log/kills.md`
- **Schedule:** Weekly, Friday afternoon
- **Optional routine:** Friday pre-compose at Thu 23:00 (on by default — silent prep, no notification)

### How to grade yourself

- **9/10:** Run weekly, kill at least 1-2 things per run, no second-guessing
- **7/10:** Run weekly, kill occasionally, sometimes second-guess kills mid-week
- **5/10:** Skip every 3-4 weeks, struggle to kill anything
- **3/10:** Run sporadically, treat as journaling instead of triage

---

## Protocol 3 — The Agent Brief

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

- **File:** `protocols/03-agent-brief.md` — personalized to your AI stack from Part 2
- **Template:** `prompts/agent-brief-template.md` — generic 5-part template
- **Seeded example:** `prompts/seeded-example.md` — pre-filled brief for one task you mentioned deferring in Part 3 (if you mentioned one)
- **Command:** `/brief` — walks through the 5 parts interactively
- **Schedule:** Ad-hoc, whenever you're delegating

### How to grade yourself

Brief quality is the grade. Grade your first-pass briefs honestly. Most operators grade their first-pass briefs at 6/10. The second pass, after one rewrite, grades at 8.5/10. That delta is the protocol.

---

## Protocol 4 — The Weekly Kill List

### The verb

Friday at 4pm, you write down what you stopped doing this week, and why. Not what you did. What you killed.

This sounds like nothing. After 8 weeks you have a paper trail of your taste calibrating in real time. The killed-stuff log is more useful than the shipped-stuff log because it tells you what you've gotten better at not doing.

### Why it works

Most people track wins. Wins are vanity metrics; you'd track them whether or not you got better. Kills require taste — naming the trade-off, the cost of the kill, the thing you said no to that would have been easier to say yes to.

After 12 weeks of weekly kill lists, the pattern of your kills tells you what you're becoming. That information is not available from looking at your shipped work.

### Where it lives

- **File:** `protocols/04-kill-list.md`
- **Command:** Run as part of `/friday`
- **Log:** `log/kills.md` — append-only entry per week
- **Schedule:** Weekly, Friday 4pm

### How to grade yourself

- **9/10:** 3-5 kills per week, named with the trade-off, no rationalization
- **7/10:** 2-3 kills per week, sometimes light on the trade-off
- **5/10:** 1 kill per week, often vague ("stopped checking email less" is not a kill)
- **3/10:** No kills, treats the list as a complaint log

---

## Protocol 5 — The Public Commitment Slot

### The verb

Once a week, in front of a small group or a specific person, you commit to one 1000-second block of work, by name, by time. You name the thing. You name when. You name where. You say it in a place where someone else will see it.

The witness is the protocol. The slot without the witness is a journal entry.

### Why it works

Ariely and Karlan's commitment-device research is unambiguous: external witnesses lift follow-through by 15-25 percentage points. The effect is larger when the witness is a peer (not a coach) and when the commitment is specific (not aspirational).

This protocol is also the bridge to Grit Collective. A solo witness slot held weekly for a month is the muscle. A defined hard outcome with a group of 8 in a Pursuit is the next scale of the same mechanic.

### Where it lives

- **File:** `protocols/05-commitment-slot.md` — personalized to your witness from Part 4
- **Command:** Run as part of `/friday` (drafts the message); paste into your witness's channel when ready
- **Log:** `log/commitments.md` — append-only entry per week (text + outcome at week end + self-grade)
- **Bundle:** `bundles/witness-this-week.md` — the actual draft message
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

The protocols are not independent. They form a weekly cadence:

| Day | Protocol | What you do |
|---|---|---|
| Mon-Fri | Protocol 1 | Daily sweep at your placed slot |
| Any day | Protocol 3 | Brief whenever you delegate to an LLM |
| Friday 4pm | Protocols 2 + 4 + 5 (one ritual via `/friday`) | Matrix → kills → next week's commitment → witness draft |
| Saturday | Send the witness message |

That's the whole rhythm. Two rituals, one daily utility. The system runs you, not the other way around.
