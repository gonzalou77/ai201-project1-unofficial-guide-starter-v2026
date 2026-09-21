# The Unofficial Guide

Louis Gonzalez — corpus: `advice_threads`

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does

This is a small retrieval-augmented question-answering system built on
`advice_threads`, a corpus of 23 short student advice threads — a posted
question plus several voted replies — covering things like commuting,
printing quotas, study spots, internship timing, and what to buy before a
first winter on campus. Ask it something specific ("will I need extra
printing credits?", "is a bike worth it for a 20 minute walk commute?") and
it retrieves the most relevant reply, grounds its answer in that text only,
and names the thread it came from. Questions clearly outside the corpus
(recipes, sports trivia, other universities) get refused before any model
call is made, rather than answered by guessing.

## Chunking Strategy

**Chunk size:**
**Overlap:**

<!-- What about YOUR documents made you pick these numbers? Short posts and
     long sectioned guides don't want the same chunking, and "800 seemed
     reasonable" earns nothing. Point at something you noticed when you read
     the documents in Milestone 1.

     If you changed your mind partway through, say so and say why. That's worth
     more than pretending you got it right first time.

     Milestone 3. -->

## Sample Chunks

======================================================================
Chunk 1  |  source: thread_bike_commute.txt#0  |  produced by: chunker.py::split_documents
======================================================================
THREAD: Is a bike worth it for a 20 minute walk commute?

Yeah. Cuts an 18 minute walk to about 6. The thing nobody mentions is storage — covered bike parking exists at three buildings and is full by 9am at all three.

======================================================================
Chunk 2  |  source: thread_first_gen.txt#1  |  produced by: chunker.py::split_documents
======================================================================
THREAD: Anything specific for first-generation students?

The thing I'd say: the unwritten rules are the hard part, not the coursework. Ask about the unwritten rules explicitly. People are happy to explain them and nobody volunteers them.

======================================================================
Chunk 3  |  source: thread_laptop_specs.txt#2  |  produced by: chunker.py::split_documents
======================================================================
THREAD: How much laptop do I actually need for CS courses?

I did two years on an 8GB machine and it was fine until the last project, at which point it very much wasn't. 16 is the answer.

======================================================================
Chunk 4  |  source: thread_parking.txt#1  |  produced by: chunker.py::split_documents
======================================================================
THREAD: Worth getting a parking permit?

Street parking on Verrill is legal and free and unmarked, which is why half the upper years do it.

======================================================================
Chunk 5  |  source: thread_sleep_schedule.txt#1  |  produced by: chunker.py::split_documents
======================================================================
THREAD: Everyone says fix your sleep. Does it actually matter?

The library being open until 2am is a trap. It's a resource, not a schedule.

For each one, ask: could someone answer a question using only this,
without reading what came before or after? Yes for all five — each pairs the
thread's question with exactly one reply, so there's one clear opinion per
chunk with nothing cut off mid-sentence and nothing from an unrelated reply
mixed in.

## Sample Answer

**Question:** Will I need to buy extra printing credits?

**Answer:**

```
For most people, the printing quota is enough, as $30 covers about 600 black and white pages. However, colour printing consumes the quota much faster because it costs eight times as much per page.

Source: thread_printing.txt
```

**My relevance cutoff:**

I set `THRESHOLD = 0.66` in `config.py`. My five in-corpus questions' best
distances ran 0.2802–0.5061; my five `OUT_OF_SCOPE` questions' best distances
ran 0.8189–0.9047. That's a wide, clean gap with no overlap, so I put the
cutoff at the midpoint (0.5061 + 0.8189 all over 2 ≈ 0.66), which gives about
0.15 of headroom on both sides — no real question comes close to being
wrongly refused, and no out-of-scope question comes close to sneaking past
the gate.

| Question | In corpus? | Best distance |
|---|---|---|
| When do employers close their applications for internships? | Yes | 0.2802 |
| How long would it take for a student to commute by bike? | Yes | 0.3616 |
| I've never lived in a place that snows, what should I buy so that I am prepared? | Yes | 0.4259 |
| Will I need to buy extra printing credits? | Yes | 0.4996 |
| what is a study spot that does not push you out? | Yes | 0.5061 |
| What is the recommended dosage of ibuprofen for a headache? | No | 0.8189 |
| How do I write a for loop in Rust? | No | 0.8606 |
| Who won the 1994 World Cup? | No | 0.8982 |
| What is the capital of Mongolia? | No | 0.8990 |
| How do I change the oil in a diesel engine? | No | 0.9047 |

## How I Used AI

**1.** I asked Claude why the fallback chunker produced a 2-character chunk
(`thread_meal_plan_tier.txt#1`, just `"t."`). It came back with the exact
cause: that document is 682 characters, under the 800-char chunk size, but
the loop still takes a second, empty-ish window because `680 < 682`. I used
that to decide against character-count chunking altogether — I wrote
`split_documents` to split on the `--- reply N ---` markers instead, since
that's a boundary these documents actually have.

**2.** I asked Claude to compare retrieval at `top_k=4` vs `top_k=5` on my
five test questions. It came back showing `k=5`'s extra slot never added a
second correct chunk, only ever noise from an unrelated thread. I changed
`TOP_K` from 5 to 4 because of that, and used the same distance numbers it
measured to move `THRESHOLD` from the starter's 0.6 to 0.66, the midpoint of
the actual gap.

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
