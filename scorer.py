"""
Unit 2's scorer: decides whether an answer counts as correct.

`run_eval.py` calls `judge(question, expects, answer, results)` once per run,
once it finds this file. `expects` is the phrase you wrote in questions.py;
`answer` is what the model actually said; `results` are the Chunk objects
retrieval handed to it.

Why rapidfuzz instead of the plain substring check this started as
(`expects.lower() in answer.lower()`): the model paraphrases. "Cuts an 18
minute walk to about 6" doesn't contain the literal string "6 minutes", and
"colour" doesn't contain "color" spelled your way. A strict substring check
marks both of those wrong even though the answer is right. rapidfuzz scores
how close two strings are without demanding an exact match.

`fuzz.partial_ratio` is the specific one to use here, not plain `fuzz.ratio`:
it finds the best-aligned *substring* of the longer text and scores against
that, rather than scoring the two full strings against each other. That
matters because `answer` is usually a full sentence or two and `expects` is
meant to be a short phrase inside it (see questions.py) — `ratio` would
punish the answer just for containing extra words around the right one.
"""

from rapidfuzz import fuzz

# 0-100. Chosen by running this against my own five questions' real answers
# and checking the score didn't cross this line on a wrong answer, or fall
# short on a right one. Lower lets more paraphrasing through but risks
# passing a near-miss; higher approaches the exact-substring check this
# replaced.
THRESHOLD = 85


def judge(question, expects, answer, results) -> bool:
    expects = expects.strip()
    if not expects:
        return False

    score = fuzz.partial_ratio(expects.lower(), answer.lower())
    return score >= THRESHOLD
