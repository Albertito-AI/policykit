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
handout, facilitator answer key, descriptive rubric and blank feedback form.
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
