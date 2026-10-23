# Learner handout: what does the evidence actually establish?

**Fictional training exercise.** All source text, dates and existing reviewer
details are invented. No passage describes actual law, an actual institution
or a legal opinion. This is an unevaluated prototype developed with AI
assistance. You need only this handout and paper or a spreadsheet.

## 1. Your task

You are helping an editor inspect an AI-assisted style of draft. The following
passage was constructed for this exercise; it is not a captured answer from a
tested model. Check it against the complete sources below. Do not search for
the fictional URLs or add outside law.

> Draft A states that each request is entered in a log before examination.
> Draft A gives the reviewer five days to respond. Both drafts specify the
> same deadline of five working days. After an initial decision, a requester
> can ask for further review. The ledger's checked flag proves that these
> conclusions have been legally verified.

Your final outputs are an evidence table, a replacement paragraph of no more
than 100 words and a short explanation of the software report's limits.

## 2. Complete source packet

The wording and paragraph labels below reproduce
[examples/training_sources.md](../examples/training_sources.md).

### Draft A: `SRC-draft-a`

**A.1** A coordinator receives requests submitted to the fictional project.

**A.2** The coordinator enters each request in a log before a reviewer examines it.

**A.3** The reviewer responds within five working days.

### Draft B: `SRC-draft-b`

**B.1** A coordinator keeps a register of requests and responses.

**B.2** The reviewer responds within ten working days.

The fixture supplies no rule establishing which draft governs. Neither draft
states that a further review is available after the initial decision. In the
ledger, both sources have `as_of` date `2025-01-01` and accessed date
`2025-01-02`. The names A and B, and these dates, do not establish precedence.

## 3. Trace and classify the evidence

A relation describes your reasoned assessment of a source against a particular
proposition. It is not a classification supplied by the software.

| Relation | Question to ask |
| --- | --- |
| `supports` | Does this passage substantiate the proposition within its stated scope? |
| `qualifies` | Does this passage require a limitation, condition or more precise wording? |
| `contradicts` | Does this passage conflict with what the proposition asserts? |
| `context` | Does this passage provide background without establishing the asserted point? |

Work through these stages in order. A defensible explanation matters more than
choosing a label in isolation.

1. **Support:** Find the exact passage supporting "Draft A states that each
   request is logged before a reviewer examines it". Does B.1 independently
   establish that same sequence?
2. **Qualification:** Inspect "Draft A gives the reviewer five days to respond".
   Which word in A.3 must be retained? Record a `qualifies` relation and a
   precise rewrite. If you favour a different label, explain how you interpreted
   the unspecified word "days".
3. **Contradiction:** Test "Both drafts specify the same deadline of five
   working days". Record both A.3 and B.2. Explain the disagreement and whether
   you can choose a governing draft from these materials.
4. **Unsupported inference:** Find any passage establishing a further review
   procedure. Distinguish "the supplied texts do not state it" from "it is
   prohibited". What should the editor do with this sentence?

Copy this table onto paper or into a spreadsheet. Use a second line within a
row, or a duplicate row, when one proposition has multiple evidence links.

| Item | Proposition or precise rewrite | Source ID and pinpoint | Relation and reason | Action or unresolved question |
| --- | --- | --- | --- | --- |
| P1: logging | | | | |
| P2: response unit | | | | |
| P3: shared deadline | | | | |
| P4: further review | | | | |

Leave any new ledger entries `unreviewed` while this work is incomplete. In a
private working copy, a person may later record their own actual review and
its limits. Do not adopt the fixture's invented reviewer identity, invent a
review date or ask a model to assert that a human review has occurred.

## 4. Repair the passage

Write a paragraph of no more than 100 words which:

- preserves the supported logging statement;
- states the response unit precisely;
- reports both drafts' deadlines without selecting an unsupported governing
  rule;
- describes the limit of the supplied evidence on further review;
- explains what a `checked` status can and cannot establish.

**Replacement paragraph:**

...........................................................................

...........................................................................

...........................................................................

## 5. Inspect the existing ledger report

This snapshot reproduces the important entries in
[examples/synthetic_ledger.json](../examples/synthetic_ledger.json). Its
propositions are deliberately not all the same as your repaired paragraph.
The single `checked` entry is an example of a declaration by a **fictional
reviewer**, not evidence that a real person has reviewed your work.

| Claim ID | Proposition | Recorded status | Source and pinpoint | Relation |
| --- | --- | --- | --- | --- |
| `CLAIM-logging` | Draft A states that requests are entered in a log before review. | `checked` | `SRC-draft-a`, A.2 | `supports` |
| `CLAIM-remedy` | The drafts provide a further review procedure after an initial decision. | `unreviewed` | `SRC-draft-b`, pinpoint missing | `context` |
| `CLAIM-timing` | The draft procedure specifies a response within five working days. | `contested` | `SRC-draft-a`, A.3 | `supports` |
| `CLAIM-timing` | The draft procedure specifies a response within five working days. | `contested` | `SRC-draft-b`, B.2 | `contradicts` |

The validator reports **zero structural errors and three warnings**:

| Warning | Recorded problem |
| --- | --- |
| `UNREVIEWED_CLAIM` | `CLAIM-remedy` has no completed review declaration |
| `MISSING_PINPOINT` | Its link to Draft B has no pinpoint |
| `CONTESTED_CLAIM` | `CLAIM-timing` is recorded as contested |

Answer these questions after inspecting the report and the sources together:

1. Why are there four evidence rows but only three propositions?
2. Would adding `B.2` to the remedy claim's empty pinpoint make that claim
   supported? Explain the difference between a filled field and relevant evidence.
3. Should the timing warning disappear merely because a reviewer prefers
   Draft B? What information is missing?
4. If a well-formed entry contained a false statement and a claimed human
   review, could this software determine that the statement was false?
5. What is the strongest justified statement you can make about `checked`?

No installation is required. If you already have the repository and Python
3.10 or newer, you may generate the same view from its root directory:

```bash
python -m regnav_evidence validate examples/synthetic_ledger.json
python -m regnav_evidence report examples/synthetic_ledger.json --format markdown
```

## 6. Exchange and reflect

Exchange your table and paragraph with a partner. Ask them to reproduce one
pinpoint and identify one retained qualification or unresolved disagreement.
Record one change you made, or a disagreement you still have and why.

**Change or disagreement:**

...........................................................................

For optional feedback, use the [blank template](feedback_template.md). Do not
include names, student records, private research or client information in
anything intended for publication.
