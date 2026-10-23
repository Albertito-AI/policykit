# RegNav roadmap

## Purpose

Make the evidence and interpretive choices behind legal propositions easier to
inspect. Begin with legal accountability in sustainability reporting across
Asian jurisdictions. Build reusable methods before expanding coverage.

## Current component

Version 0.1 provides an offline evidence ledger, structural validation,
Markdown and CSV reports, a synthetic worked example and regression tests.
The code has no external runtime dependency. Real-world usefulness and legal
dataset quality still require evaluation.

## Next work in priority order

1. **Protect review history when records change.** Design a comparison command
   that identifies modified propositions, source versions and evidence links.
   Record when prior review should be reconsidered. Add cases for substantive
   edits, metadata-only edits and renamed identifiers. Do not silently change
   a person's review declaration.
2. **Create one source-grounded worked case.** Select a narrow sustainability
   disclosure question in Singapore or Thailand, record current primary sources
   and exact pinpoints, and state the interpretive limits. Keep human review
   status accurate. Start with a small, inspectable set of propositions.
3. **Evaluate a complete research task.** Compare a conventional source table
   with the ledger on the same materials. Define observable errors and review
   time in advance. Document a pilot honestly before making benefit claims.
4. **Improve entry and review.** Choose a CSV import or an accessible browser
   editor only after observing where users struggle. Preserve offline access
   and the JSON record. Check import ambiguities and export fidelity.
5. **Extend the legal comparison.** Add the second jurisdiction when the first
   worked case is stable. Distinguish disclosure duties, supervision, liability,
   standing and remedies. Record disagreements rather than forcing equivalence.
6. **Prepare a citable release.** Review rights, documentation, evaluation and
   outstanding defects. Use a stable version and an archival record if an
   appropriate connection and rights permit it. No DOI has yet been assigned.

## Proposed first twelve weeks

| Period | Intended outcome | Evidence needed |
| --- | --- | --- |
| Weeks 1 to 2 | Reliable ledger and record-change design | Passing relevant checks and reproducible example |
| Weeks 3 to 4 | One narrow legal worked case | Opened primary sources, pinpoints and documented limits |
| Weeks 5 to 8 | Usability pilot and targeted revision | Actual task observations and a correction record |
| Weeks 9 to 12 | Evaluated demonstration and release decision | Complete documentation, rights review and honest results |

These are planning targets, not delivery or adoption guarantees. Reorder the
work when actual defects, user feedback or source availability justify it.

## Other programmes

Legal education with AI is a possible second programme. A future teaching
exercise can use this ledger to examine what a written answer reveals about
understanding. Sports governance can supply later case studies. Neither adds
new obligations to this prototype before the core workflow is useful.
