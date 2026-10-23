# RegNav roadmap

## Purpose

Make the evidence and interpretive choices behind legal propositions easier to
inspect. Begin with legal accountability in sustainability reporting across
Asian jurisdictions. Build reusable methods before expanding coverage.

## Current component

Version 0.1 provides an offline evidence ledger, structural validation,
Markdown and CSV reports, a synthetic worked example and regression tests.
The code has no external runtime dependency. A complete fictional teaching
exercise, external usability protocol, first-use guide and contribution routes
are available. A narrow Singapore case records two unreviewed propositions
against official primary sources. Real-world usefulness, educational benefit
and legal dataset quality still require evaluation. See the
[project status](project_status.md) for the evidence baseline.

## Next work in priority order

1. **Protect review history when records change.** Design a comparison command
   that identifies modified propositions, source versions and evidence links.
   Record when prior review should be reconsidered. Add cases for substantive
   edits, metadata-only edits and renamed identifiers. Do not silently change
   a person's review declaration.
2. **Obtain human review of the first worked case.** The
   [Singapore example](../cases/singapore-sustainability-reporting/README.md)
   now records two narrow propositions, inspected primary sources and exact
   pinpoints. Both remain unreviewed. A reviewer should examine the source
   versions, reporting-period limits and each evidence relationship before
   entering an actual declaration. Do not expand case volume ahead of this
   review or represent an AI inspection as completed human assessment.
3. **Run the first external usability pilot.** Use the prepared
   [protocol](evaluation_protocol.md) with three independent volunteers. Record
   task completion, assistance, misunderstandings and reproducible difficulties
   privately. Revise concrete defects and report bounded, anonymous results.
   The manual-first sequence is not a controlled comparison and cannot establish
   a productivity or learning benefit. Design any later comparative evaluation
   separately.
4. **Improve entry and review.** Choose a CSV import or an accessible browser
   editor only after observing where users struggle. Preserve offline access
   and the JSON record. Check import ambiguities and export fidelity.
5. **Extend the legal comparison.** Add the second jurisdiction when the first
   worked case is stable. Distinguish disclosure duties, supervision, liability,
   standing and remedies. Record disagreements rather than forcing equivalence.
6. **Prepare a citable release.** Follow the
   [release criteria](release_readiness.md), including rights, documentation,
   evaluation limits and outstanding defects. Use a stable version and an
   archival record if an appropriate connection and rights permit it. No DOI
   has yet been assigned.

## Proposed first twelve weeks

| Period | Intended outcome | Evidence needed |
| --- | --- | --- |
| Weeks 1 to 2 | Reliable ledger and record-change design | Passing relevant checks and reproducible example |
| Weeks 3 to 4 | Human review of the first narrow legal case | Actual review of source versions, pinpoints and documented limits |
| Weeks 5 to 8 | Usability pilot and targeted revision | Actual task observations and a correction record |
| Weeks 9 to 12 | Evaluated demonstration and release decision | Complete documentation, rights review and honest results |

These are planning targets, not delivery or adoption guarantees. Reorder the
work when actual defects, user feedback or source availability justify it.

## Other programmes

The [teaching exercise](../teaching/README.md) is a first, unevaluated resource
for legal education with AI. It examines how a written answer can be traced
to sources and revised when its claims exceed the evidence. The next teaching
action is to observe a small pilot using the prepared protocol, then revise
the instructions in response to actual difficulties. These materials are
separate from the coauthored ANSWERABLE book project. Sports governance can
supply later case studies once the core workflow is useful.
