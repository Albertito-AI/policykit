# Contributing to RegNav

RegNav is an early research prototype for recording the evidence behind legal
propositions. Useful contributions identify a concrete problem, make the
evidence inspectable and keep the proposed change small enough to review.
Independent usability and legal-dataset evaluation remain to be done.

Read the [README](README.md), [roadmap](docs/ROADMAP.md),
[research standard](docs/RESEARCH_STANDARD.md) and [rights notice](RIGHTS.md)
before proposing substantial work. For repository changes, also follow
[AGENTS.md](AGENTS.md).

## Choose a contribution route

Search existing issues for the same problem, then use the relevant form in
the repository's New issue menu. One focused issue is usually sufficient.

| Route | What makes a useful contribution | A bounded starting point |
| --- | --- | --- |
| Reproducible bug | Actual commands, a small synthetic input, expected and observed behaviour, software and Python versions | Show one command that fails on a public fixture or mishandles a documented input |
| Source-grounded research case | A narrow proposition, jurisdiction, primary-source links, exact pinpoints, source versions and interpretive limits | Propose one sustainability-disclosure question with a small set of inspectable authorities |
| Documentation or usability feedback | The page or task, what was unclear, what actually happened and a proposed correction if available | Clarify one instruction, report one observed obstacle or identify one misleading explanation |

An untested suggestion is welcome when labelled as a suggestion. A report of
one person's experience is not evidence of broad adoption or effectiveness.
Do not invent external users, quotations, endorsements, review activity or
results. The [teaching pack](teaching/README.md) and
[usability protocol](docs/evaluation_protocol.md) provide bounded activities
for collecting actual observations.

## Reproduce a software problem

Use the supplied fictional ledger or construct the smallest synthetic example
which still exhibits the behaviour. Include the command, relevant output,
exit code if known, and steps another person can repeat. Distinguish an
unexpected error from an intentional warning.

The unchanged training fixture has zero structural errors and three warnings.
Normal validation exits `0`; strict validation exits `2` while warnings remain.
Those results do not establish the truth of a proposition. The program does
not retrieve source text or decide whether it supports a claim.

If you cannot reproduce a problem again, say so. Record what you observed and
what remains unknown rather than inventing a cause or a successful test.

## Propose a research case

Begin with one question and a small number of propositions. Follow the
[schema](docs/schema.md) and distinguish a source's publication, commencement,
version and consultation dates. Use the issuing institution's primary text
where possible and provide a reproducible section, paragraph, page or
provision. Explain each `supports`, `qualifies`, `contradicts` or `context`
relation rather than treating a URL as evidence by itself.

State which passages you personally examined and what remains unresolved.
Identify translation status where relevant. Separate a source's words from
your interpretation and retain contrary material. A summary or search result
is insufficient for a disputed passage. Link to the source instead of
uploading a full third-party publication.

New entries remain `unreviewed` until the relevant person actually conducts
and declares review. `checked` records a person's declaration; the software
does not authenticate that person or certify legal accuracy. Neither an
automated check nor an AI-generated statement may stand in for completed
human review. Label fictional examples clearly and do not invent authorities,
quotations, citations or reviewer details.

## Keep public contributions suitable for publication

Issues and pull requests are public. Do not include personal, student or
client data, private manuscripts, credentials or identifying local paths.
Use synthetic fixtures and inspect logs and screenshots before sharing them.
Do not upload completed participant feedback forms. A sanitised account of
an observed difficulty is sufficient; obtain agreement before publishing a
participant's quotation.

If the problem cannot be described safely in public, contact the maintainer
through the [institutional profile](https://research.rug.nl/en/persons/tan-sin-hon-albert-tan/)
to discuss an appropriate route. Do not attach sensitive material to the
initial enquiry.

## Rights and attribution

The prototype currently has no general reuse or open-source licence. Public
availability, these contribution instructions and the issue forms do not
change [RIGHTS.md](RIGHTS.md). No contributor licence agreement or blanket
copyright assignment is introduced here.

Before substantial work involving reused code, teaching materials, manuscripts
or other third-party content, clarify the relevant permissions and proposed
use with the maintainer. Identify original and reused material, preserve
attribution and existing notices, and state any uncertainty. Do not assume
that a public webpage or jointly authored work may be incorporated freely.
Link to permission information where it is public; do not publish private
agreements or correspondence.

Credit actual contributions and disclose material AI assistance concisely.
AI assistance does not establish independent review, authorship by another
person or an endorsement of the resulting analysis.

## Prepare a pull request

Keep the change focused and explain the problem, what changes and the result.
Use the pull request template. Link an existing issue when relevant; a small
correction does not need a new issue merely to create a reference.

Preserve the offline, standard-library design unless a dependency has a
documented benefit. For code changes, run the relevant regression checks
and example commands, recording actual results and the Python version:

```bash
python -m unittest discover -s tests -v
python -m regnav_evidence validate examples/synthetic_ledger.json
python -m regnav_evidence report examples/synthetic_ledger.json --format markdown
```

For a documentation-only change, check links, source consistency and any
commands you change. Do not add tests which merely repeat prose. Report
checks not run and any remaining uncertainty. Update the progress record and
next actionable roadmap item when the change warrants them, as required by
the repository guidance.

## Maintainer triage

For each substantive new report, identify whether it is a contributor
observation, a maintainer finding or an untested proposal. Check for duplicates,
then record the evidence needed for the next decision. Prioritise reproducible
failures that block the documented workflow or misrepresent evidence and
review status. Assess research cases against the source and scope requirements;
assess documentation feedback against the actual task it obstructs.

A useful triage note states the problem, what was reproduced or inspected,
what remains missing and one next action. Request only information needed
to resolve that uncertainty. Explain a deferral or out-of-scope decision.
No response time or acceptance is promised.

When a scheduled review finds no substantive change, record that result in
the workflow summary. Do not manufacture issues, comments, pull requests or
external activity to make the repository appear active.
