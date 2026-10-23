# Facilitator guide and source-grounded answer key

**Status:** unevaluated teaching prototype, developed with AI assistance.
The source checks described here are internal preparation, not an independent
review or a finding about learning. All examples are fictional. Read the
[research standard](../docs/RESEARCH_STANDARD.md) before running the session.

## Preparation and delivery

Plan for 55 minutes using the schedule in [the teaching README](README.md).
Print the [learner handout](learner_handout.md), or share it in a readable
format, and retain this guide for the discussion. Learners can use paper or
a spreadsheet throughout. Give them time to inspect the complete source packet
before showing the answer key. No live model interaction is needed.

Introduce the activity as practice in examining a claim's evidential basis.
The narrow fictional setting removes the need for prior jurisdictional
knowledge. It does not test or establish competence in actual legal research.

During the support stage, ask learners to state exactly what A.2 establishes.
During the qualification stage, ask them to compare "days" and "working days"
before agreeing on a label. During the contradiction stage, ask what additional
evidence would be needed to decide which draft governs. Then have pairs prepare
the revised paragraph before discussing the report.

The report can be read from the handout. If demonstrating the CLI, use the
commands in the README without changing the fixture. Do not present the
expected warnings as software failures or remove them to manufacture a clean
result. A successful structural check is not a successful substantive review.

## Answer key: the four source tasks

### P1. Logging: support within the stated draft

`SRC-draft-a`, **A.2**, supports: "Draft A states that each request is entered
in a log before a reviewer examines it." The words "before a reviewer examines
it" establish the sequence.

`SRC-draft-b`, **B.1**, says that a coordinator keeps a register of requests
and responses. It does not specify when logging occurs relative to review.
For the sequencing claim, B.1 is context. Its silence about sequence is not a
contradiction of A.2 and does not establish the same sequence in Draft B.

### P2. Response unit: qualification and a precise rewrite

`SRC-draft-a`, **A.3**, says "within five working days". Use `qualifies`
against the underspecified draft phrase "five days", explaining that the
response unit must be preserved. A precise replacement is:

> Draft A states that the reviewer responds within five working days (A.3).

Once the proposition includes "working", A.3 supports that revised wording.
The relation changes because the proposition changed.

The relation is an analytical judgment. A learner might use `contradicts` if
they expressly interpret the draft's "days" as calendar days, or `supports`
if they read it as shorthand. Credit a clear explanation which still restores
the exact source wording. The fixture does not define a working day or a date
from which time starts; do not invent those details.

### P3. Shared deadline: preserve the discrepancy

`SRC-draft-a`, **A.3**, specifies five working days. `SRC-draft-b`, **B.2**,
specifies ten working days. A.3 supports the five-day statement within Draft A.
B.2 contradicts the proposition that **both drafts specify the same five-day
deadline**.

This does not mean that a response on day five would violate a ten-day limit.
The discrepancy concerns the deadlines stated in the drafts, not every
possible instance of performance.

No supplied paragraph establishes precedence. The labels "A" and "B" are
not a rule of authority. Both source records use the same `as_of` and accessed
dates. Preserve the conflict as `contested`, or rewrite the proposition to
report the two drafts separately and retain a note that the governing choice
is unresolved. A rewritten descriptive comparison can be supported by both
passages without resolving which procedure governs.

### P4. Further review: absence of supporting text

Read **A.1 to A.3 and B.1 to B.2**, the entire supplied packet. No passage
states a further review procedure after an initial decision. A.1 concerns
receiving requests; B.1 concerns maintaining a register. Neither establishes
an appeal or further review right.

Remove the affirmative claim or replace it with a bounded statement:

> The supplied texts do not state a further review procedure.

Do not infer that further review is legally prohibited or unavailable in any
real system. The ledger's original `context` link with a missing pinpoint is
an intentionally incomplete record. Adding a convenient but irrelevant
pinpoint cannot supply the missing evidence.

## One possible replacement paragraph

> Draft A requires logging before examination (A.2) and a response within five
> working days (A.3). Draft B specifies ten working days (B.2). The materials
> do not establish which draft governs. Neither supplied draft states a
> further review procedure (A.1 to A.3; B.1 to B.2). The ledger records a
> person's declared review; a checked status does not establish legal validity
> or factual truth.

This is an answer for the fictional exercise. It is not a legal opinion and
does not record a real human review of the ledger. Alternative paragraphs
are acceptable if they preserve the evidence and its limits.

## Answer key: the software report

| Handout question | Expected reasoning |
| --- | --- |
| Four rows, three propositions | `CLAIM-timing` has two evidence links, so it appears twice in the flat matrix. |
| Add B.2 to the remedy claim | This can fill the field and remove the missing-pinpoint warning. B.2 concerns response time and does not establish further review. The substantive gap remains. |
| Prefer Draft B | Preference is not evidence of precedence. The fixture provides no governing rule, so preserve or explain the unresolved discrepancy. |
| False but well-formed statement | The validator checks structure and declared metadata. It does not read source text, decide support, authenticate the reviewer or establish truth. |
| Meaning of `checked` | It records the entry author's declaration of human review, with required metadata. Here the reviewer and date are fictional training details. |

The unchanged fixture produces these exact warning locations:

| Code | JSON location |
| --- | --- |
| `UNREVIEWED_CLAIM` | `$.claims[1]` |
| `MISSING_PINPOINT` | `$.claims[1].evidence[0].pinpoint` |
| `CONTESTED_CLAIM` | `$.claims[2]` |

Normal `validate` returns exit `0`; `validate --strict` returns exit `2` for
these warnings. The Markdown report contains two sources, three propositions
and four evidence rows. The CSV has the same four evidence rows. There is no
automated source retrieval or substantive verification.

## Review declarations and assessment

Do not fill a new `review.reviewer` or `review.date` field for a learner, and
do not ask a model to claim a person reviewed a source. New working entries
remain `unreviewed` until the relevant person actually performs and declares
their review. Preserve the supplied fixture unchanged; its fictional review
record is an example, not a template identity to copy.

Use the [rubric](assessment_rubric.md) to describe the reasoning shown in
this exercise. Do not report scores as proof of learning gains or general
legal accuracy. If a learner challenges a relation label, inspect the scope
of their proposition and their explanation before scoring it.

End by asking: "Which uncertainty remains after every required field is
filled?" A useful answer identifies an interpretive or source-authority
question rather than suggesting that every warning should be suppressed.

Capture optional feedback with the [blank form](feedback_template.md).
Record actual observations separately from suggestions and do not publish
participant identities, private work or fabricated testimonials.
