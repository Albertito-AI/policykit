# Teaching pilot: checking propositions against fictional sources

**Status:** original, unevaluated teaching prototype. Suggested duration:
55 minutes, adjustable to 45 or 60 minutes. No learning benefit has yet been
demonstrated. Developed with AI assistance and checked against the repository's
fictional fixtures; this is not independent educational evaluation.

This exercise asks learners to inspect a model-style draft, locate its evidence,
repair its wording and explain what a structural validation report can establish.
It uses invented internal procedures to practise methods relevant to checking
AI-assisted legal writing. It supplies no actual law or legal opinion.

The materials are newly written for this repository. They are not an excerpt
from, or an authorised companion to, *ANSWERABLE: Teaching Law When the Machine
Can Write*. No contribution by a book co-author or endorsement by a publisher
is implied. The repository's [rights statement](../RIGHTS.md) remains applicable;
this pack does not introduce a reuse licence.

## What to prepare

Read the [facilitator guide](facilitator_guide.md), including the answer key.
Give learners the [handout](learner_handout.md) and access to
[the complete fictional sources](../examples/training_sources.md).
The handout reproduces all five source paragraphs, so a printed session needs
no computer, account, model access or software installation. A learner may
complete its evidence table on paper or in an ordinary spreadsheet.

The [assessment rubric](assessment_rubric.md) supports discussion of the
particular responses. It is not a validated measure of legal competence.
Use the blank [feedback template](feedback_template.md) to capture observations;
do not treat its empty fields as collected results.

## Session at a glance

| Minutes | Activity | Concrete output |
| --- | --- | --- |
| 0 to 5 | Establish the fictional setting and limits | Learners distinguish the exercise from actual legal advice |
| 5 to 13 | Read the sources and model-style draft | Four initial source judgments |
| 13 to 25 | Work through support, qualification and contradiction | Evidence table with exact pinpoints and reasons |
| 25 to 35 | Repair the draft and identify the unsupported claim | Revised paragraph of no more than 100 words |
| 35 to 45 | Inspect the report, with an optional CLI demonstration | Explanation of three warnings and the meaning of `checked` |
| 45 to 55 | Exchange reasoning and debrief | One correction or remaining disagreement recorded |

For 45 minutes, combine the initial reading with the evidence table and use
the handout's report snapshot. For 60 minutes, add five minutes to compare
alternative treatments of the ambiguous phrase "five days".

## Optional facilitator CLI route

The software demonstration is optional for learners. A facilitator with Python
3.10 or newer can run these commands from the repository root. There are no
third-party packages or network calls.

```bash
python -m regnav_evidence validate examples/synthetic_ledger.json
python -m regnav_evidence report examples/synthetic_ledger.json --format markdown
python -m regnav_evidence report examples/synthetic_ledger.json --format csv --output teaching-evidence.csv
```

The supplied ledger has zero structural errors and three intentional warnings:
`UNREVIEWED_CLAIM`, `MISSING_PINPOINT` and `CONTESTED_CLAIM`. Normal validation
exits `0`; the same example with `--strict` exits `2`. A CSV export has four
evidence rows because the timing claim links to two sources. Choose a different
output filename if `teaching-evidence.csv` already exists.

Do not change the distributed fixture merely to remove its warnings. Its named
reviewer is explicitly fictional. A learner's real review declaration, if one
is made, belongs in a separate local working record and must describe only
work that person actually performed. A model must not create a completed human
review on anyone's behalf.

For the separate observational software pilot with three external volunteers,
use the [evaluation protocol](../docs/evaluation_protocol.md). The teaching
session and that usability pilot address different questions. Neither has yet
produced participant data or demonstrated impact.
