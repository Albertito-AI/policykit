# Coordinating project work

This file gives recurring maintenance a shared order of work. Read it with
[AGENTS.md](../AGENTS.md), the [roadmap](ROADMAP.md) and the
[progress record](PROGRESS.md). A scheduled check is an opportunity to make a
useful change, not a requirement to create a commit.

## Responsibilities

| Workstream | Primary responsibility | Evidence of useful progress |
| --- | --- | --- |
| Core development | `regnav_evidence/`, `tests/`, schema and technical roadmap | A reproducible defect fixed or a bounded capability demonstrated with relevant checks |
| Legal evidence cases | `cases/` and its primary-source registers | A narrow proposition with inspected sources, exact pinpoints, version information and honest review status |
| Adoption | Quickstart, examples and teaching entry points | A complete first-use route or a correction to an observed obstacle |
| Community care | Contribution guidance, issue forms and substantive issue or pull-request triage | A real report understood, a duplicate identified, a problem reproduced or a clear next action |
| Release readiness | Changelog, citation metadata and release checks | A specific candidate assessed against the published criteria, with unresolved limitations retained |
| Reach and impact | Public entry points and the project status record | Accurate links and attribution, or independently evidenced use and feedback recorded with permission |

For case selection, legal-data automation and expansion decisions, consult the
[landmark and key case workflow rationale](CASE_LAW_WORKFLOW.md). It is the
shared guide to purpose, coverage, proposition-level analysis and review gates.
Its structured-record requirements are a development direction; coordinate
schema and command changes with core development through the process below.

Broader academic collaboration and teaching work can supply concrete needs to
these streams. Public repository records should contain relevant evidence and
outputs, not private correspondence, unpublished manuscripts or business plans.

## Start from the current state

1. Read the current default branch, open issues and open pull requests before
   selecting work. Inspect relevant recent changes and the latest applicable
   CI results. Do not work from a stale local copy without comparing it.
2. Choose one bounded item from the roadmap or a substantive new report. Read
   existing work in the same area. If another branch already addresses it,
   review or extend that work through an explicit hand-off instead of creating
   a duplicate implementation.
3. Keep responsibility clear when a change crosses streams. Core development
   owns schema and command behaviour; cases must not silently redefine them.
   Update shared root documents once the component changes are ready to review.
4. Use a branch from the inspected base. Review the full diff and relevant
   checks. Before updating a ref or merging, compare the current head with the
   head actually reviewed. If either branch moved, inspect the intervening
   changes and reconcile them. Do not overwrite another contributor's work.
5. Record what changed, the evidence examined, checks actually run and one next
   action. Distinguish a software check, an AI source-inspection pass, a human
   review declaration and an independent external observation.

## What warrants a change

Prioritise a reproducible failure, misleading instruction, unsupported claim,
stale source record or material barrier to use. A new case must add a distinct
research question, rather than restating existing material for activity.
Release decisions follow the [release criteria](release_readiness.md).

When no substantive work is ready, leave the repository unchanged and report
the result in the maintenance summary. Do not create empty issues, routine
timestamp commits, artificial version increments or self-generated engagement.
Do not treat maintainer activity or AI assistance as independent adoption.

## Review and publication boundaries

Follow [CONTRIBUTING.md](../CONTRIBUTING.md) and [RIGHTS.md](../RIGHTS.md).
Automated preparation cannot complete a person's legal-review declaration.
Human review and external feedback must reflect work that actually occurred.
Keep completed participant records and private messages out of public changes.
Contacting people, distributing private material and changing public access
require the authority applicable to that action; routine repository maintenance
does not create such authority by itself.
