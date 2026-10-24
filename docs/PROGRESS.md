# Development progress

## 23 October 2026

### Starting point

The main branch contained one README linking two starter archives and naming
RegNav. No application source was tracked in that branch. The archives remain
linked in the new README as legacy material. Their content and rights were not
assumed to be part of this implementation.

### Work completed

- Added a standard-library Python evidence ledger with init, validate and report
  commands, schema documentation and explicit human-review declarations.
- Added a complete fictional training example with three intentional warnings.
- Added regression coverage for malformed input, identifiers, source references,
  dates, review metadata, safe exports and protection against input overwrite.
- Added this progress record, a focused roadmap, research standards, citation
  metadata and a GitHub Actions workflow.

### Verification

The implementation was tested locally on Python 3.12.14. All 24 regression
tests passed. The training example returned zero errors and three expected
warnings. Markdown and CSV generation succeeded. The workflow specifies
Python 3.10, 3.12 and 3.14; its results are recorded in GitHub Actions and must
be inspected separately from the local result.

The implementation and documentation were developed with AI assistance.
Automated tests and internal code review do not establish legal accuracy,
independent peer review or demonstrated user benefit.

### Current limitations and next action

There is no automatic source retrieval, source-change detection, authenticated
reviewer identity, browser interface or evaluated legal dataset. Source URLs
are checked for structure only. Existing review declarations can become stale
when a user edits the JSON.

At this stage, record-change comparison was the next technical priority.
The later entries below record parallel documentation and case preparation.
Record concrete progress here; do not generate commits solely to increase
visible activity.


### Teaching materials and external pilot preparation

Added a complete 55-minute exercise, with 45- and 60-minute variants, a learner
handout, facilitator answer key, descriptive assessment rubric and blank feedback form.
The exercise supplies the full fictional source packet and supports paper or
spreadsheet use as well as an optional command-line demonstration.

Added a protocol for an initial three-volunteer external usability pilot.
It records five tasks, assistance, obstacles and observation limits. Completed
participant records remain private. Public issues may contain only sanitised
reproduction steps using the fictional material. No volunteers have completed
this pilot and no outcome or adoption claims are made.

Verification on Python 3.12.14: all 24 existing regression tests passed. All
five source paragraphs in the learner handout match the training source
packet exactly. The report snapshot matches the fixture's identifiers,
propositions, pinpoints and declared review statuses. Normal validation
returned zero errors and three expected warnings; strict validation exited
with code 2. Markdown and CSV reports were generated successfully, with four
CSV evidence rows. Relative Markdown links resolve. An independent internal
review checked source interpretation, the answer key, review declarations,
rights and the treatment of participant data, with no blocking issues found.
This internal review is not external peer review or educational validation.

The code, source fixtures and rights notice are unchanged. These original,
AI-assisted materials do not reproduce the ANSWERABLE manuscript and do not
imply involvement or endorsement by its co-author or a publisher.

Next technical action: record-change comparison remains first in the roadmap.
Next evaluation action: arrange the three volunteer sessions and record actual
observations under the prepared protocol. Do not substitute invented sessions
or repeated self-testing for external evidence.

### First-use, source-case and contribution preparation

Added a ten-minute first-use guide with expected warnings, exit statuses, CSV
export, troubleshooting and a paper route. Added an unedited generated sample
report from the existing fictional fixture. The suggested timing has not been
measured with independent users.

Added the first real-source case: two narrow SGX Mainboard propositions, four
official source records and exact provision or page references. The preparation
pass opened Rules 711A and 711B, Practice Note 7.6 and the linked amendment PDF.
It distinguished the 1 January 2026 version labels from the access date and
retained the relevant qualifications. Both propositions remain `unreviewed`;
no human review declaration, issuer-specific assessment or legal validation
has been recorded.

Added three issue forms, contribution guidance and a pull-request template.
These distinguish actual observations from untested suggestions, preserve
rights and provide concrete routes for reproducible bugs, source cases and
documentation feedback. No issues or comments were created to simulate
external activity. The project status page records the independent evidence
still needed, while workstream guidance and release criteria coordinate
maintenance without requiring an artificial stream of commits or releases.

Verification on Python 3.12.14: the unchanged fictional fixture returned zero
errors and three expected warnings; strict validation exited 2. Its generated
Markdown exactly matched the saved sample report; CSV export contained a
header and four evidence rows. The fixture was unchanged. The Singapore case
returned zero errors and two expected `UNREVIEWED_CLAIM` warnings; Markdown
report generation succeeded. Those case checks establish structure only.

The three issue forms passed a duplicate-key-rejecting YAML parse and local
checks against GitHub's documented form fields. The forms have not been
verified in GitHub's rendered issue-creation interface. Relative documentation
links were checked. Code, tests, citation version and the rights notice were
unchanged. The preceding merged teaching change's
[CI run](https://github.com/Albertito-AI/policykit/actions/runs/39947205410)
passed on Python 3.10, 3.12 and 3.14; the new pull request's checks must be
inspected separately before merge.

Next technical action: implement bounded record-change comparison. Next case
action: obtain an actual human review of the two prepared propositions before
expanding coverage. Next evaluation action: collect the three pilot sessions'
observations under the existing protocol. Maintenance should respond to those
results and substantive reports, rather than manufacturing evidence of use.

## 24 October 2026

### Read-only record-change comparison

Implemented `regnav_evidence compare before.json after.json` with optional
machine-readable `--json` output. It first requires both snapshots to pass
existing structural validation. The command compares stable identifiers,
source version and other substantive source fields, proposition text and notes,
evidence links, review declarations and ledger-level metadata. It ignores
display order, identifies metadata-only access-date changes, and treats
identifier renames as removal plus addition rather than inferring identity.
Previously `checked` or `contested` propositions receive a recheck flag
when a material part of their recorded basis changes. Neither source file nor
any review declaration is modified.

Added ten focused synthetic comparison tests and two CLI regression tests,
including invalid snapshot handling and non-mutation. The ten focused
comparison tests passed locally with Python 3.13.5. Existing test and workflow
results for this branch must be confirmed in GitHub Actions; a local unit
result is not a claim that all supported Python versions have passed.

The tool compares recorded metadata and links. It does not detect unrecorded
changes at a source URL, verify quotations, fetch law, authenticate a reviewer,
or determine whether a previous review remains sound. A changed access date
alone does not imply substantive source alteration. Changes to notes are
conservatively treated as potentially material because they can affect the
recorded interpretation.

Next technical action: investigate actual usability or comparison defects
before expanding features. Next legal evidence action: obtain a real human
review of the two unreviewed Singapore propositions. External adoption and
educational benefit remain untested.

### Manual first-use self-check

The no-Python quickstart now links directly to the existing source-grounded
facilitator answer key for use **after** the learner has completed the source
questions. This closes a navigational gap without changing the fictional
sources, CLI, reports, human-review declarations or rights. The roadmap
retains the key as post-task material and requires any prior exposure during
an observational pilot to be recorded.

Checked the source packet, answer-key heading and relative links. The packet
states five working days in A.3 and ten working days in B.2, and supplies no
further-review procedure or rule selecting a governing draft. This internal
source/document check does not establish independent usability, educational
benefit or actual external adoption. The next adoption step remains the
three-volunteer observational pilot using the existing protocol.

### Isolated source-file change experiment

Following the maintainer's request for a bounded technology-product experiment,
added `experiments/source_watch/` without changing the core ledger schema, CLI,
review declarations, citation version or rights statement. The utility snapshots
SHA-256 digests for explicitly listed local files and returns affected claim IDs
when later bytes change or a file cannot be observed. It does not fetch sources,
determine whether a change matters legally or run as a hosted monitoring service.

Seventeen focused tests passed locally on Python 3.13.5, including malformed
inputs, duplicate keys and IDs, traversal/symlink rejection, file-size limits,
missing sources, linked-claim selection, non-mutation, exact hashes and command
exit codes 0/1/2. Output creation refuses an existing path. The fictional demo
was actually run and its JSON output saved unchanged as `sample_report.json`.
A direct local clone failed DNS resolution; repository reads and writes used
the connected GitHub service. Local verification therefore covers this isolated
experiment, not a newly cloned full local suite. Remote CI is separate evidence.

The threat boundary is a trusted, stable local directory. This is not a sandbox
against malicious concurrent filesystem changes. Unchanged bytes establish only
identity with the saved baseline, not current law, authenticity, complete coverage
or legal correctness. Baseline integrity and semantic review remain external.

The next action is to observe independent reproduction and establish a recurring
user need before implementing a hosted adapter. No participant, paid customer,
external adoption, security certification or commercial licence is claimed.

### Source Watch discovery and evaluation path

Added a direct entry to the separate Source Watch experiment from the root
README, with a link to its existing generated fictional report. Replaced its
short pilot-interest paragraph with a fit check, a three-line enquiry prompt and
a description of the matters to agree before any pilot. Readers can inspect the
report without installing software or supplying contact details. The evaluation
route now explicitly preserves the existing reuse restrictions and distinguishes
an enquiry from permission, a contract or payment.

This is a documentation-only change. Source code, dependencies, tests, fixtures,
review declarations, rights and citation metadata are unchanged. The new Markdown
passages were parsed locally on Python 3.13.5 and their five relative link targets
checked against the inspected repository tree; the evaluation heading matches the
new anchor. These checks cover the edited passages, not a live-browser usability
test. The full remote diff and applicable automated check results are separate
review evidence. No local software regression suite was rerun for these prose
changes. No independent visitor, enquiry, pilot completion, conversion increase
or revenue is established by publication of this path.

Next action: inspect genuine evaluation enquiries and obtain the necessary
permission before any executable pilot. Record whether a recurring need and
usable result are observed before expanding the component.

### Contributor routing for the Source Watch experiment

The contributor guide now distinguishes public, synthetic Source Watch bug and
usability reports from private evaluation, rights and commercial enquiries.
This closes a routing ambiguity following the new demonstration entry in the
root README. The guide provides a path without implying an executable licence
or inviting confidential workflow details into public issues. Source Watch,
issue templates, rights, software, fixtures and publication status are unchanged.
Both linked repository assets were read back by exact path and confirmed to
exist. No executable command changed, so no local runtime tests were rerun.
No external enquiry, pilot, customer or revenue follows from this correction.

### Canonical website link

Added the maintainer's [website](https://www.alberttansinhon.com/) to the
README's introductory links, retaining the institutional profile and ORCID.
The destination returned HTTP 200 with normal TLS certificate verification.
This change affects documentation only; no code or executable examples changed,
and no local runtime tests were rerun.

Next maintenance action: check the canonical website address during the next
public-link review. The existing research and evaluation priorities continue.
