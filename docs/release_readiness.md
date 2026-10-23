# Release readiness

RegNav currently identifies its software as **0.1.0**, a research prototype.
The package, [citation metadata](../CITATION.cff) and
[changelog](../CHANGELOG.md) use that version. A version string in source is
not proof of a published GitHub release, archival deposit or DOI.

This page defines the evidence needed to decide whether a particular commit
is ready for a release. It does not schedule automatic publication.

## Current evidence and gaps

| Area | Evidence available on 23 October 2026 | Remaining limitation |
| --- | --- | --- |
| Software | 24 regression tests passed locally on Python 3.12.14; [CI on the preceding merged teaching change](https://github.com/Albertito-AI/policykit/actions/runs/39947205410) passed on Python 3.10, 3.12 and 3.14 | Check CI for the actual candidate commit before a release decision; a prior run cannot certify later changes |
| Reproduction | Fictional fixture, [quickstart](quickstart.md), generated [sample report](sample_report.md) and paper route | Independent first-use observations have not yet been collected |
| Legal example | [Singapore worked case](../cases/singapore-sustainability-reporting/README.md), primary-source links and two unreviewed propositions | AI source inspection and structural checks do not establish completed human review |
| Teaching | Complete fictional [exercise](../teaching/README.md) and [three-volunteer pilot protocol](evaluation_protocol.md) | No educational benefit or independent usability result has been demonstrated |
| Rights and attribution | Explicit [rights notice](../RIGHTS.md), citation metadata and contribution guidance | No general reuse licence or DOI has been supplied; any archival distribution requires appropriate rights |

The package does not retrieve sources, authenticate reviewers, establish
current law, determine whether a passage supports a proposition or invalidate
stale review declarations after an edit. Release notes must retain these
material limits.

## Candidate decision record

For a real candidate, record the following in its pull request or release
preparation record. Leave unknown items explicit rather than filling them
with assumed success.

1. **Purpose and exact revision.** Identify the candidate commit and the
   substantive changes since the previous published version. Give a user a
   concrete reason to adopt it. Documentation improvements alone need not
   change the software version.
2. **Behaviour and reproduction.** Run checks relevant to changed behaviour
   and the repository's required CI. Report Python versions, commands and
   actual results. Reproduce any changed example. Check warning expectations,
   exports and file protections where affected. Do not repeat unrelated tests
   merely to enlarge the verification record.
3. **Sources and review status.** Inspect changed legal passages in primary
   sources, with jurisdiction, version, date and pinpoint. Preserve unresolved
   qualifications. Identify which examples remain unreviewed and which human
   declarations, if any, actually exist. Do not label a dataset validated on
   the basis of a passing structural check.
4. **User-facing consistency.** Check README commands, sample output, schema,
   changelog, package version and citation metadata against the candidate.
   Keep a usable paper route for teaching material. Confirm important links.
5. **Rights and material to distribute.** Review the scope of the proposed
   archive and existing permissions. Exclude private participant records,
   manuscripts, credentials and third-party texts without the necessary
   permission. Do not introduce a licence or rights transfer during routine
   release preparation.
6. **Defects and decision.** Identify unresolved blockers and bounded known
   limitations. Release only if the evidence supports the description offered
   to users. A prototype may remain explicitly unevaluated; it must not be
   presented as an independently validated research instrument.

## Publication and citation

Publication is a separate action after a candidate is ready. Confirm the
actual tag, release status and distributed files before reporting publication.
An archival identifier must resolve to the intended version before being
added to citation metadata. Do not invent a DOI or imply that a GitHub commit
has received peer review. Preserve existing release history and unrelated
drafts. When publication is unavailable, retain a concrete candidate and its
remaining steps rather than claiming completion.
