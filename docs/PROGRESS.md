# Development progress

## 11 November 2026: workbench citation scope reconciled

Updated the Evidence Ledger-only citation title and description to identify the
existing `regnav-workbench` distribution and both installed components,
`regnav_evidence` and `regnav_esg`. README and release guidance now distinguish
that scope from checkout-only experiments and the separate private extension.
The author identity, source version `0.1.0`, console commands and reserved rights
are unchanged. No release, DOI or independent validation is asserted.

On Python 3.12.14, `python scripts/check_installed_wheel.py` passed: the built
wheel contained 26 members, its installed imports resolved inside the fresh
virtual environment, and both console scripts worked outside the checkout.
The fictional ledger and text-ingestion/report path passed. These are packaging
observations; optional parsers and independent use were not tested in this pass.
Next: assess an exact publication candidate against the remaining release
criteria, including archive scope, applicable rights and honest evaluation limits.

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

## 25 October 2026

### Literal evidence text in Markdown exports

Reproduced a concrete presentation defect in GitHub-flavoured Markdown:
a proposition containing `~~excluded~~` renders the enclosed words as
struck through, even though the original ledger records those characters
literally. A changed visual emphasis can misrepresent a research note in an
evidence matrix.

Extended the existing table-cell escaping in `regnav_evidence/reports.py` to
include `~` and added a focused regression for a ledger title, proposition
and source title. The change is confined to the rendered Markdown view;
JSON records, source links, review declarations, CSV output and schema are
unchanged. An offline renderer demonstration using Python 3.13.5 and Mistune
3.2.1 confirmed the before/after distinction; this local demonstration was
not the repository's full regression suite. No runtime dependency was added.

Next action: verify the proposed branch through GitHub Actions, inspect the
reviewed diff and merge only if checks pass. The separate priorities remain
actual human review of the first Singapore case and independent first-use
observations. Neither export escaping nor CI demonstrates legal accuracy,
external adoption or commercial demand.

### Operator-scoped local agent gateway

Following the maintainer's explicit request for agent-to-agent collaboration,
added an isolated MCP stdio interface to the existing Source Watch check. The
operator selects a baseline and trusted source directory at startup; the client
cannot replace that configuration or request arbitrary paths, URLs or commands.
The gateway exposes capability metadata and a read-only check, targeting MCP
protocol version 2025-11-25. It adds no runtime dependencies, network listener,
payment capability, source edits or human-review declarations.

Added a machine-readable project catalogue, an actual generated fictional
subprocess exchange, integration instructions and an opt-in public technical
issue form. The catalogue contains no invented external partners or endpoint.
The network design distinguishes a callable local tool from third-party discovery,
external task delegation and commercial operation. Existing rights and the
coauthored book's boundaries are preserved.

Twenty-five focused tests passed locally on Python 3.13.5, covering lifecycle,
version negotiation, exact underlying output, unchanged/changed/unavailable
sources, non-mutation, rejected path and command inputs, input limits and error
privacy. The demo was run and its output matched the saved exchange. The reused
Source Watch file matched its inspected remote Git blob SHA exactly. New relative
documentation links and the issue-form YAML were checked locally. Direct GitHub
network access failed DNS resolution, so connector reads/writes were used. No
full local repository suite, official MCP SDK/client test, independent agent
trial or live issue-form rendering is claimed; remote CI is separate evidence.

The boundary remains a trusted, stable filesystem. The gateway is not a hostile
filesystem sandbox or an authenticated multi-tenant service. Returned metadata
may be transmitted by the client to its own model provider. No raw manuscript,
client data, credentials or financial plan was published by this change.

Next action: obtain one permitted independent client reproduction with fictional
material, record setup effort and interpretation errors, and fix observed
interoperability defects before adding network transport or registry distribution.
No registered marketplace, external partnership, deployment, adoption or payment
is established by this internal implementation.

### Direct entry for agent operators

The inspected root README linked Source Watch but did not lead directly to its
MCP gateway. Added a short agent-operator entry linking the existing gateway,
generated fictional exchange, capability catalogue, collaboration guide and
pilot invitation. The entry asks for a non-confidential client/version, task and
desired result, while retaining execution permissions and private commercial
terms as separate decisions. It creates no new service or licence.

The new Markdown section was parsed locally with Python 3.13.5 and Mistune 3.2.1.
Its five relative targets matched the inspected remote tree; all six links and
the heading rendered in the local HTML. The existing invitation was read back,
and no comments were present at that observation. These are documentation and
link-target checks, not a browser usability test, notification-delivery check or
independent agent reproduction. No software tests were rerun locally for this
prose-only change. The full remote diff and applicable CI results require review
before merge.

Next action: qualify an actual operator response and one permissioned independent
reproduction. Preserve the one-off nature of previous invitations; do not repeat
mentions to manufacture activity. No new participant, collaboration, registry
listing, buyer or payment is established by this entry-point improvement.

### Evidence-handover development record

Recorded a public technical plan with six stable work-item IDs, implementation
conditions, exclusions and eighteen proposed acceptance cases. Linked it from the
roadmap so future development can distinguish existing components from conditional
extensions. All new capability work remains specified or deferred; the acceptance
cases remain `NOT_RUN`. No source code, executable tests, schema, dependencies,
fixtures, rights or citation metadata changed.

Locally checked the new Markdown and appended passages for rendering, relative
link targets, six unique work-item IDs, eighteen unique case IDs, valid case-to-work
references and preservation of the source design's not-run states. Screened the
new text for private correspondence, customer names, private workspace links and
financial details. These are documentation checks, not runtime, professional-review
or independent-user tests. No local software regression suite was rerun. Remote
diff review and any automatically triggered CI are separate evidence.

Next action: qualify one permitted task and use existing behaviour where adequate;
otherwise agree an explicit export contract before starting RN-M01. Preserve prior
progress history and do not infer a delivery, deployment, customer or paid outcome
from publication of this plan.

### Experimental implementation of the evidence-handover plan

Following the maintainer's explicit instruction to implement the six recorded
items for testing, added one isolated workflow under experiments/evidence_handover/.
It uses a RegNav-owned fictional export contract, not a presumed customer format.
The adapter retains the entire export as a validated sidecar and generates only
unreviewed core-schema records. The existing ledger comparator, Source Watch,
text-safe renderers and MCP lifecycle are reused without modifying their files.

Implemented separate source, record, process and supplied-inventory observations;
exact scope-field and supplied-anchor checks; declared assurance-set consistency;
version-specific supplied declarations and new-file history extension; JSON,
Markdown and CSV views; and an opt-in operator-configured MCP handover tool. No
source-text parsing, causal model diagnosis, professional assurance, authenticated
reviewer identity, remote endpoint, payment function or runtime dependency is added.
The original specification remains linked at its immutable pre-implementation commit.

Forty-seven focused tests passed locally on Python 3.13.5. They include executable
versions of all eighteen disclosed engineering cases and regressions for malformed
input, safe paths, file limits, immutable inputs, exclusive outputs, history,
command exit codes and a real local subprocess protocol exchange. The benchmark
runner separately executed the eighteen cases and generated a receipt with source
hashes. The actual fictional demo reproduced its saved sample, a deterministic
view of selected report fields rather than an operational snapshot. Blank independent
comparison records remain NOT_RUN; no human review or participant is invented.

Direct git network access failed DNS resolution. The inspected dependencies were
reconstructed locally and their Git blob identities matched the remote source.
This local result covers the new focused suite, not a complete fresh local clone.
The existing GitHub workflow discovers the new tests and must be inspected at the
actual reviewed head before merge. Documentation, fixture JSON and new-file privacy
checks were also performed. Remote CI is separate evidence, not presumed from a
local pass. No official MCP SDK/client test or independent-user evaluation ran.

Next action: evaluate the disclosed contract and handover with one permitted
independent operator, document actual setup and review effort, and repair concrete
failures with regression tests. Continue bounded evidence-led improvement rather
than automatically growing the feature list. Existing rights, code/schema,
source-review declarations, private material and financial records remain unchanged.

### Singapore case: annual reporting versus immediate market disclosure (26 October 2026)

The existing first case already supported Rule 711A report timing and Rule
711B(3) internal review, but its source map did not expressly separate the
annual timetable from the Mainboard Rule 703 immediate-disclosure analysis.
Refined the same two **unreviewed** propositions rather than adding a new case.
The 26 October primary-source pass reopened SGX Mainboard Rules 711A and 711B,
Practice Note 7.6 (notably paragraphs 1.2, 5.3, 6.1, 6.2 and 6.4), and inspected
Mainboard Rule 703(1)-(3). The 23 October amendment redline was not re-opened,
and its earlier access date remains unchanged. The additional Rule 703 source
was recorded with its actual 26 October inspection date and without inventing
an effective-date marker on the section page.

The editorial improvement separates: (i) annual-report timing from possible
immediate market announcements; (ii) reported content from evidence of an
internal-review process; and (iii) reporting and metric scope from supervision,
liability, claimant standing and remedy. The distinctions are consistent with
Tan's published 2026 comparative-accountability framework, but that article's
30 July legal cut-off and scholarship are not substitutes for the current SGX
sources. A short factual-intake matrix records unknown issuer, reporting-period,
review-process and Rule 703 facts; a clearly fictional contrast illustrates
why missing review records do not prove non-performance. No actual issuer,
violation, external assurance decision or professional review is claimed.

Files affected: the existing Singapore case ledger and guide, the root case
pointer, this history entry and the legal-review priority. The case retains two
unreviewed claims and five pinpointed source records. Added a scoped CI step to validate the updated ledger and generate Markdown
and CSV matrices alongside the existing synthetic checks. Inspect the actual
branch result and diff before merging; no passing result is inferred merely
from adding a command. A structural pass cannot establish legal correctness. Next action:
independent qualified review of both claims, all five sources, the additional
Rule 703 relationship and the precise period/application assumptions before
any checked declaration or case expansion.

### Singapore case: bounded common law authority map

Added `cases/singapore-sustainability-reporting/common-law-authorities.md`, linked from the existing case README. On 26 October 2026 an AI source-inspection pass opened three Singapore Court of Appeal judgments (*Spandeck*, *Panatron* and *Ho Kang Peng*) and one English House of Lords judgment (*Hedley Byrne*). The map identifies negligence, deceit and company-directed directors' duties, with judgment pinpoints and distinct claimant, standing and remedy questions. English law is labelled comparative rather than controlling; no case is presented as a sustainability-reporting holding. The two original SGX ledger propositions and their unreviewed statuses are unchanged. No new statutory causes of action, issuer-specific findings, current-law completeness, or human review is claimed. Next: independent qualified human review and subsequent-treatment/statutory checks before further ledger expansion.

## 28 October 2026

### Singapore common law case: standing and corporate recovery

Under the 26 October owner instruction to continue issue-selected common law research, expanded the existing Singapore sustainability-reporting authority map without modifying the original four-case tranche, case ledger, source records, review declarations, CLI or code. Added primary Singapore judgments concerning shareholder and corporate injury, reflective loss, statutory derivative-action permission, the 2015 expansion of Companies Act section 216A to listed companies and the liquidation exception. Located limited subsequent treatment and mapped the still-open questions of causation, remoteness, defences, limitation, remedies, assurance contracts and securities/statutory consequences. Updated the case entry and roadmap to acknowledge that this AI-prepared source mapping is authorised, while independent qualified human review is still required before any legal claim is marked checked.

The research uses an analytical distinction reflected in Albert Tan's published *Converging Standards, Divergent Accountability* (online 1 October 2026; legal cut-off 30 July 2026): reporting duties, representations, claimant reliance and liability must be assessed separately. This is a scholarly organising method, not a judicial holding or an ESG-specific decided case. Primary judgments were inspected through the official Singapore Judiciary eLitigation database on 28 October 2026. Later treatment was sampled only. Direct retrieval of the current consolidated Companies Act from Singapore Statutes Online returned HTTP 403; period-specific legislation, the recorded *Zhuang* appeal, statutory investor remedies and contractual assurance duties remain unverified. The law is not declared exhaustive or certified current in all respects. No actual issuer or litigant, independent human legal review, released product or independently used case is asserted.

This is a documentation/source-map change. Verification consists of the primary judgment inspection, source and pinpoint review, scoped GitHub diff, retained-ledger identity/status checks and any repository CI that can actually be tied to the exact branch/merge commit. Structural validation of an unchanged ledger would not validate the new judicial interpretation. Next review: confirm the present Companies Act text and relevant appeal/subsequent treatment, then seek independent human review of the source-to-question map before any checked ledger claim or issuer-specific conclusion.

### Local ESG workbench implementation

Under the maintainer's explicit 28 October implementation instruction, added
`regnav_esg` alongside the unchanged original evidence ledger. The new package
reads local PDFs/text/Markdown, retains page and parser provenance, optionally
performs local English OCR and geometric table extraction, produces page-labelled
Markdown, locates quotations, retrieves pages and extracts configurable candidate
passages. It imports explicit activity records from CSV/XLSX, calculates emissions
using supplied versioned factors, screens financial and impact perspectives
separately, resolves exact supplied standards references and generates action
plans from supplied gaps. An offline HTML view and an adapter to unreviewed
core-ledger context records make the workflow reproducible.

The optional model adapter makes no request without explicit network opt-in,
model selection and credentials. Its tests use mocked Responses API outputs.
Quotation presence and literal numeric-field checks do not establish semantic
support. No live model performance is claimed. The configurable materiality
rubric uses exact rational arithmetic for threshold decisions and separately
records rounded display scores. Missing activity evidence and unobserved scope
buckets remain explicit; a factor citation is not proof of an activity quantity.

The original 126 tests passed before the change. The expanded public suite
passed 237 tests locally on Python 3.12.14. Actual local exercises covered
text-PDF extraction, an image-only OCR fixture, geometric table cells, XLSX,
two original fictional report PDFs, source navigation targets and core-ledger
validation. A complete 8,366,023-byte public CDL 2025 report was processed as
217 physical pages and 703,197 text characters. Its default rule results reached
the disclosed twenty-candidate cap in each of ten fields; this demonstrates
execution, not completeness or measured accuracy. The initial incomplete
download was rejected. Real company source contents and outputs are not included
in this repository. A local wheel build succeeded.

AI-assisted adversarial code review identified and repaired altered captured
values, source/extraction mismatches, malformed imported records, invisible CSV
formula prefixes, falsey invalid assessment inputs, a materiality rounding edge
case and Markdown table literal-text changes. Regression cases accompany these
repairs. This development review is not independent professional or human
validation. Public files contain original code and clearly fictional fixtures;
private research, client data and proprietary rule packs are excluded.

Next action: inspect exact-head CI, then evaluate a permitted report pair with
independently checked reference data and an operator-configured model. Record
precision, recall, abstentions, missing coverage and review effort separately.
No hosted service, customer adoption, full platform parity, assurance opinion or
automated legal judgement is established.

### README feature showcase and reproducible entry route

Following the maintainer's request to make the upgraded capabilities clear on
GitHub, rewrote the README around the public ESG workbench, concrete fictional
outputs and a complete first-use route. The page now leads with a capability
table, retained PDF passages, a downloadable HTML example and correctly ordered
installation and execution instructions. The demo command includes fictional
source URLs so it actually produces the advertised ledger export. Calculation,
materiality and planning examples are explicitly separate from the saved HTML
sample, whose assessment section is empty.

Added a clearly labelled high-level description of the separate private
research extension and its two fictional comparison outcomes. Its code,
contracts, private artifacts and unpublished research remain outside the public
repository. Corrected wording to distinguish supplied completion reports from
verified performance and facility totals grouped by entity from separate entity
aggregates. Preserved research attribution, rights, teaching and integration
entry points. Updated the roadmap's component description and next evaluation
step. No executable code, schema, fixture, dependency or rights file changed.

On Python 3.12.14, executed the README's PDF generator, workbench, ledger
validation, activity import, inventory, materiality, standards lookup, planning
and core-ledger examples in a fresh temporary checkout using already available
dependencies. The PDF workflow produced two documents, five physical pages and
33 candidates; all five quoted passages matched their retained physical pages.
Confirmed the stated calculation, screening and planning outputs, and the
synthetic ledger's three expected warnings. Checked 56 relative file/section
targets, Markdown fences and the absence of private paths or content; retrieved
the newly linked public HTML download. The 237-test local result and three-version
CI result linked in the README are the recorded implementation evidence, not a
new local regression run or independent performance evaluation.

Next action: have a permitted independent evaluator follow the README, record
installation and interpretation difficulties, then evaluate a report pair with
reference data and a configured model. Inspect any automatically triggered CI
at the actual documentation commit before merge.

### README demonstration: an observed fictional ledger run

Added a near-top “See it in action” section with a self-contained SVG showing
the bundled ledger's two source records, three propositions, four evidence rows
and explicit review gaps. The visual is a diagram of observed CLI fields, with
a link to captured output and the existing generated matrix and quickstart.

On Python 3.12.14, normal validation returned zero errors and the three expected
UNREVIEWED_CLAIM, MISSING_PINPOINT and CONTESTED_CLAIM warnings, exiting 0. Strict
validation exited 2. Markdown and CSV export both exited 0; the generated Markdown
matched the existing sample's generated section and the CSV had four evidence
rows. The public transcript identifies source revision
17e173491f42ddf7f62bd40aae976d324bd5fe54. Runtime code, fixtures, review declarations
and rights remain unchanged. Hosted checks are separate from these local results.

Next action: use the existing usability protocol to record actual first-use
friction and prior demo exposure when an authorised independent pilot occurs.
This presentation change establishes no legal review, external adoption or
measured usability benefit.

## 29 October 2026

### Contributor issue-routing clarification

A maintainer-led community check found that the existing agent-interoperability
issue form was missing from the contribution-route table. The guide also did
not distinguish reports about the separately packaged Apache-2.0 RegNav Source
Watch GitHub Action from reports about this repository's reserved-rights local
Source Watch and MCP experiments. Updated `CONTRIBUTING.md` to direct reports to
the appropriate existing issue tracker without creating another issue or
altering licences, software behaviour or permission requirements.

This correction is based on inspection of the two repositories' current public
entry points. It is not an independent user complaint, completed external
integration, verified adoption or commercial outcome. Next action: assess real
incoming issues against the documented route, request only necessary synthetic
reproduction details, and leave unresolved reports open.

### Landmark and key case workflow rationale

At the maintainer's request, recorded the collection's agreed direction in
[CASE_LAW_WORKFLOW.md](CASE_LAW_WORKFLOW.md). The guide sets out the global
ambition, a practical decision guide, case-selection criteria, proposition-level
provenance, later treatment, applicable instruments, conditional applications,
coverage limits, review responsibilities and useful measures of progress. It
identifies future structured records and automated maintenance as development
directions and retains the actual AI-prepared status of the existing case map.

Linked the guide from the root README, case collection, research standard and
workstream instructions so ordinary case work encounters it. Updated the next
case-development action in the roadmap while preserving the outstanding human
review and external evaluation priorities. The existing source records, ledger,
runtime, schema, rights and scheduled jobs are unchanged.

Local documentation checks on Python 3.12.14 covered all seven changed Markdown
files: 88 relative link targets and 13 section anchors resolved, fenced blocks
were balanced and the diff passed whitespace checks. An AI documentation review
inspected the complete guide and related changes for source/review distinctions,
scope, ownership and private material. It prompted clearer separation of
retention and republication permissions and explicit identification of party
submissions within judgment analysis. This is an internal documentation review;
it does not establish substantive human legal review. No executable examples
or runtime behaviour changed, so no local software regression suite was rerun.
Applicable GitHub CI remains separate evidence tied to the reviewed commit.

Next action: agree and trial a small structured tranche from the existing
Singapore authority map with core development, preserving source context and
review status and publishing the tranche's coverage gaps. Publication of this
guide establishes the recorded direction, rather than completion of the planned
repository, independent legal review or demonstrated user benefit.

### 30 October 2026: newly linked source byte-drift attention

The evidence-handover workflow captures source observations even for recorded
files that are not yet linked to a claim. Its Source Watch baseline intentionally
covers only previously linked files. An earlier comparison omitted the
corresponding byte-drift notice when a previously unlinked file changed locally
and was subsequently linked to an existing claim. A normal claim-link change was
recorded, but the source-file divergence was not separately visible.

The targeted correction compares the two observed SHA-256 values only when the
source ID and local path are stable, its earlier links were absent, and it
has a current claim link. It flags the newly linked claim without changing the
raw Source Watch observations or claiming source authentication or legal truth.
Additional fictional regression cases cover changed bytes, unchanged bytes and
a previously missing baseline. The original eighteen disclosed synthetic
benchmark cases remain separate; no new independent reviewer has been observed.

The next gate remains independent reproduction of the full reviewer workflow,
including what source differences mean for a genuinely useful task. No new
licence, customer processing authority, release or commercial claim is created.

## 30 October 2026

### ESG workbench: duplicate-source HTML navigation

Inspection of the offline workbench identified that supplying the same source
bytes twice gave both document cards the same automatic source identity and
HTML fragment links. A source-page link in the second card could therefore
open the first card's page, obscuring which input entry was being inspected.
The ledger export already rejected duplicate source identities; the read-only
HTML path did not.

The HTML renderer now rejects repeated source anchors with an actionable
message before building the workspace. A synthetic regression covers a direct
renderer call, the same input path twice and a separate path containing the
same bytes. It also checks that no partial output directory is created.
Existing source extraction, schema, rights and review declarations are unchanged.

The next gate is an independent first-use check of source navigation and
candidate review. Passing engineering tests cannot establish extraction
accuracy, human legal review, usability benefit or external adoption.

### Case map: financial-audit remoteness and liability boundary

On 30 October 2026, the Legal Evidence Cases lane inspected official Singapore judgments *Deloitte & Touche LLP v Hin Leong Trading* [2026] SGCA 33, *JSI Shipping* [2007] SGCA 40 and *PlanAssure* [2007] SGCA 41, recording paragraph-specific holdings and qualifications in the existing common law authority map. The 2026 Court of Appeal distinguished breach, factual causation, contractual remoteness and available defences, and struck out an audited company's trading-loss claim as too remote. The 2007 judgments locate audit-verification standards and fact-sensitive contributory fault. The selection is informed by the published reporting-versus-liability framework and a proposed distinction between accurate content and evidence of proper preparation. That proposed distinction is not settled law or a new verified judicial rule. No private manuscript text or working register is published. The existing first tranches and original SGX JSON ledger remain unchanged and unreviewed.

This is documentary case research, not a software change, legal clearance or external case review. Checked references are official eLitigation HTML with inspection date 30 October 2026. Subsequent treatment was sampled through the 2026 decision's citations, not exhaustively traced. SGX sustainability assurance, independent investor duty, relevant contractual terms, current statute and loss quantification remain unresolved. No benefit, customer adoption or completed qualified human review was observed. Next: seek primary assurance-engagement terms/recognised rights and verify current statutory context before attempting an issuer-specific or investor proposition.

### 31 October 2026: concealed formula-like activity cells

The ESG activity importer rejected visible `=`, `+`, `-` and `@` cell
prefixes, including ordinary whitespace before them, but Python's
`str.lstrip()` does not remove many Unicode format characters. A direct
synthetic prefix probe found that a word joiner or zero-width space could
precede an otherwise formula-like cell without triggering that guard.

The bounded correction inspects leading whitespace and Unicode control/format
characters before applying the existing formula-like prefix rejection. It
leaves input text unchanged, does not evaluate a formula, and continues to
accept benign identifiers containing format characters without a dangerous
prefix. Focused fictional CSV tests cover concealed prefixes, headers and
benign text; optional XLSX coverage checks a text-typed disguised prefix.
The output CSV's separate escape guard is not weakened.

This is a conservative import-validation improvement, not evidence that any
particular spreadsheet executed a disguised formula. The software regression
suite and GitHub checks must be verified at the reviewed PR revision. All
substantive legal propositions remain unreviewed, and independent usability
and reporting-value evaluations remain outstanding. Next: preserve these
regressions and seek a permissioned end-to-end reviewer observation.

## 1 November 2026

### ESG workbench output-write interruption recovery

The local workbench previously created its final directory and then wrote
individual report files sequentially. A later write exception could leave
partly written JSON/CSV/HTML and prevent a retry using the documented output
path. Added best-effort exception cleanup of filenames reserved by that
invocation, followed by removal of the new directory if empty. Exceptions
continue to propagate; an output failure is never reported as success.
A fictional regression simulates a partial second file and verifies that the
ordinary workflow can be retried without overwriting existing outputs.

This change does not claim atomic multi-file publication, recovery from process
termination without exception handling, protection against concurrent writers,
improved extraction accuracy, a completed human review or measured user savings.
The current version's relevant unit and hosted checks are to be recorded against
the exact PR/merge revisions. The next external gate remains a permitted
independent full-workflow reproduction with observed setup, checking and
correction effort.

## 2 November 2026

### Case map: appellate causation correction and third-party rights

**Issue and baseline:** The existing 30 October map correctly distinguished financial-audit analogies from unverified sustainability assurance, but its contractual-privity gap lacked a Singapore third-party-rights authority and a directly pertinent appellate treatment of a published professional fact-finding report. The next risk was incorrectly treating a negative High Court duty analysis as definitively affirmed when an appeal existed.

**Evidence and change:** Opened official eLitigation HTML for *Tan Woo Thian* [2020] SGHC 171 [57], [74]–[80], [87]–[92] and the actual appeal, *Tan Woo Thian* [2021] SGCA 20 [6]–[12], [14]–[19]. The Court of Appeal dismissed the negligence appeal on **lack of causal evidence of actual loss**, while expressly leaving the duty question **undecided**. Opened *CLAAS Medical Centre* [2010] SGCA 3 [25]–[30], [33]–[37], which distinguishes intended and incidental contractual beneficiaries under the then-applicable Contracts (Rights of Third Parties) Act. The official current-statute search result displayed the 2020 Revised Edition's s 2(1)–(4), but direct Singapore Statutes Online full-text retrieval returned **HTTP 403**. The complete current Act was therefore not independently opened. These documents concern corporate investigation and shareholder non-compete, not an ESG assurance engagement.

**Delivery and testing:** Extended only the existing `cases/singapore-sustainability-reporting/common-law-authorities.md` authority map, its dated source/change row and two relevant issue-coverage cells. Preserved prior tranches, original SGX ledger, all two `unreviewed` statuses and source records. Updated the roadmap's next case gate. This is AI source inspection and documentation, not a new ledger claim, legal opinion, test of external counsel, completed human review or release. The documentary source links/pinpoints were inspected; the repository change and any actual CI result require commit-specific verification before claiming a pass.

**Intellectual context and next evidence:** The private knowledge foundation's distinction between reporting, preparation and legal consequence informed issue selection; it supplies **no legal holding** and no private text was copied. Next: directly inspect current CRTPA exceptions and full s 2, obtain the relevant assurance engagement and any promised third-party benefit/reliance limitations, and search subsequent treatment before moving to a checked legal proposition. For fictional Investor B, existence of actual causally linked damage is distinct from quantification. Cash cost and owner effort were **not recorded**, not assumed zero. Independent use is unknown.

### Owner-requested foundations whitepaper, 2 November 2026

Added an original AI-assisted Wiki-source paper covering proposition-level evidence,
source and review distinctions, the comparability problem, public-interest purpose,
ideal progression and measurable defeat conditions. It preserves reserved rights,
the private-extension boundary and all unreviewed legal states. Added a bounded
publisher that preserves existing Wiki content and records an initialisation blocker
rather than claiming a live page. Local checks cover source links and six publisher
preservation/refusal cases; hosted results are recorded against the actual commit.
No independent user, legal or social-benefit evaluation is implied. Next: initialise
the Wiki and verify page readback; the existing independent report-pair and qualified
source-review priorities remain unchanged.

## 4 November 2026

### Case map: non-party assurance-contract benefit, remedy and forum

**Question and baseline:** The 2 November map distinguished third-party contract benefits from independent tort duty, but did not separately cover a non-party's contractual remedy, available promisor defences, potential duplicate recovery and the procedural forum. An inaccurate leap from an exclusion/indemnity benefit to an automatic right to arbitrate would be especially misleading for a sustainability-assurance example.

**Sources actually inspected:** Opened official Singapore eLitigation judgments *VKC v VJZ* [2021] SGCA 72 [53]–[65] and *Low Jun Hong v Hong Qi Yu* [2026] SGHCR 11 [23]–[25], [34]–[49]. The Court of Appeal rejected third-party reliance on an exclusive-jurisdiction clause via an implied benefit; the subsequent Registrar decision rejected inferred arbitration-stay rights in a different contract notwithstanding expressly conferred defensive benefits. Opened *Independent State of Papua New Guinea v PNG Sustainable Development Program Ltd* [2016] SGHC 19 [36]–[38] for the historical company constitution exclusion. The official Singapore Statutes Online search index showed the 2020 Revised Edition and relevant CRTPA ss 2, 4, 6–9, but **direct statute pages returned HTTP 403**. That index is a lead, not a full-text direct verification of the current Act.

**Change and scope:** Added a fifth issue-selected tranche and one coverage row to the existing Singapore common-law authority map, plus its dated source/change entry. Preserved earlier tranches. The structured SGX JSON ledger and its two `unreviewed` statuses remain unchanged. Private knowledge foundation's distinction between the communication, authority and legal consequence informed issue selection only; it was not published as independent legal authority or copied into GitHub.

**Verification and limits:** Checked the original judgment locations, documentary links and diff. The exact PR/CI outcome must be independently checked before calling any automated run passed; documentation checking does not verify legal accuracy. No actual ESG assurance engagement, beneficiary designation, investor loss, limitation period, appellate outcome for the 2026 Registrar case or third-party remedy has been established. No qualified human review or external adoption is claimed. Cash cost and human effort are unknown, not zero. Next: obtain a period-matched assurance contract, full current statute and subsequent judicial treatment; then seek independent legal review before any checked proposition.

## 6 November 2026

### Singapore authority map: limitation accrual versus discovery

**Problem and source concept:** The 4 November authority map mentioned derivative-action protective proceedings and CRTPA limitation but did not distinguish the time when actionable economic loss first occurred from the later date on which a claimant knew enough to sue. Tan's *Converging Standards, Divergent Accountability*, published online 1 October 2026 with a 30 July legal cut-off, supplies the analytical distinction between reporting, metric and liability perimeters. This is intellectual context, not legal authority for statutory limitation or evidence of effectiveness.

**Primary judgments inspected 6 November:** Official eLitigation HTML for *Lian Kok Hong v Ow Wah Foong* [2008] SGCA 30 [14]–[15], [17]–[20], [24]–[28], [36], [41]–[42], [64] and *IPP Financial Advisers v Saimee bin Jumaat* [2020] SGCA 47 [37]–[46], [49]–[59], [62]–[63], [106]–[107]. The latter expressly applies the former at [44] and [46]. Both appellate dispositions were checked and their distinct factual settings preserved. Direct retrieval of the current consolidated Limitation Act s 24A on Singapore Statutes Online returned HTTP 403; historical quotations in judgments do not establish the complete applicable current Act.

**Change:** Updated only the existing common-law authority map's limitation coverage row, added one bounded issue-specific tranche and a dated source record, and linked this next source gate in the roadmap. The SGX JSON ledger was not edited, and both propositions remain `unreviewed`. No new adjudicated ESG disclosure or investor remedy is asserted. Subsequent-treatment coverage is one express appellate link, not a complete negative citation check.

**Verification and delivery state:** Confirm exact branch and source diff, commit SHA and remote readback after the write. GitHub CI must be inspected against the resulting PR-head SHA before calling it passed; documentation-only inspection does not constitute automated validation or independent legal review. No client input, real investor timeline, third-party engagement, expert review or demonstrated benefit is known. Cash cost and owner time were not measured. The next source step is directly checking current section 24A and any claim-specific exception, with the claimant's actual cause-of-action dates; then qualified human review before any checked proposition.

### 9 November 2026: Singapore assurance-contract authority and costs boundary

The case collection's existing common-law map gained a tightly scoped analysis of *Lee Hsueh Ching v Loh Kia Hui* [2025] SGHC 258, opened directly on Singapore eLitigation, at [160]–[180], [183]–[185] and [189]–[191]. It identifies an expressly protected former employee under CRTPA ss 2(1)(a), 2(3), but preserves the court's distinct costs discretion, the contractual reasonableness boundary and refusal to shift costs of an unsuccessful third-party claim. Neither the case nor the provision establishes a right for a reader of a public ESG report to sue an assurer. The official CRTPA index returned more relevant provisions and a current-version selector; direct full-Act retrieval still returned HTTP 403, so full-current-statute inspection remains incomplete. A bounded case-title search disclosed no verified appeal disposal; this is not a comprehensive treatment check. The two existing SGX propositions remain unreviewed, and no human reviewer, software change, new commercial offer or independent benefit is claimed. Documentation-only work; verify the exact PR/merge and remote CI result separately. Next: obtain the actual engagement form and full legislation before a third-party-rights conclusion; check appellate treatment and have a qualified independent reviewer assess the map.

## 10 November 2026: installed-wheel reproducibility gate

The release lane added `scripts/check_installed_wheel.py` and connected it to
the existing Python 3.10/3.12/3.14 CI matrix. It builds the distribution, prints
its file manifest and SHA-256, then checks a fresh virtual-environment installation
and both command-line interfaces from outside the checkout. The test is
deliberately separate from checkout-local examples and does not download or
upload private material. It expects only the ledger and ESG packages in the
wheel; research experiments and fixtures remain source-tree components.
Consult exact-commit CI for execution outcomes, not this implementation note.

This addresses the previously untested clean-install path as an engineering
gate. It does not create a released distribution or verify optional PDF parsers,
independent use, legal conclusions or rights. The intended release identity
and `CITATION.cff` scope remain a distinct release decision. No version
bump, release tag, customer entitlement or licensing change is introduced.

## 11 November 2026

### Singapore authority map: *Ikumene* as a non-client audit duty and causation boundary

**Scope and reason:** The existing sustainability-assurance discussion referenced other statutory financial-audit cases but omitted Singapore's direct appellate decision concerning an individual shareholder who also guaranteed a company's credit facilities. This is a source-selection/evidence defect, not a new SGX claim. The private knowledge foundation's reporting-versus-liability distinction informed the choice of issue; no private reference text has been copied into the public case.

**Primary judgments inspected:** Singapore eLitigation HTML for *Ikumene Singapore Pte Ltd v Leong Chee Leng* [1993] SGCA 50 [17]–[30], [32]–[38] and *Tan Juay Pah v Kimly Construction* [2012] SGCA 17 [69]–[75]. *Ikumene* rejected the guarantor's personal claim on duty and causation and distinguished shareholder loss belonging to the company. The later Court of Appeal decision expressly discussed *Ikumene* [70]–[72] under *Spandeck*, a specific subsequent-treatment finding but not an exhaustive citator result.

**Change and limits:** Added one bounded section, a dated source/change row and a refined duty-coverage entry in `cases/singapore-sustainability-reporting/common-law-authorities.md`. The source reasoning is historical and confined to its statutory audit context; neither case decides an ESG assurance provider's investor-facing liability. The five-source SGX ledger and both `unreviewed` propositions remain unchanged. The applicable current Companies Act and CRTPA texts, any actual engagement or relevant investor reliance and further judicial treatment remain unverified. Human legal review has not occurred.

**Execution evidence:** Documentation and pinpoints were inspected against official judgment text. Local `git` access failed DNS resolution for github.com, so no local full-regression run or local CLI ledger report is claimed. GitHub connector comparison and exact-commit CI/readback must be reconciled separately; any workflow pass belongs only to the SHA on which it ran. The intended beneficiary is a legal researcher testing duty, claimant and causation before inferring remedy. Independent use, customer demand, cost and owner effort are unknown, not zero. Next: current period-specific statute and engagement evidence, further adverse-treatment check and independent qualified human review.

## 13 November 2026

### Singapore authority map: fiduciary limitation and separate equitable defences

**Problem and knowledge use:** Prior mapped limitation cases focused on tort and negligent misstatement. A reader could wrongly apply the s 24A knowledge extension to a company-owned equitable fiduciary remedy, or collapse delay-based defences into a single rule. The user's internal knowledge foundation differentiates a source of duty, its claimant, applicable period and remedy. That is an editorial selection guide, **not** a legal source, copied manuscript or evidence of deployment.

**Primary source inspection:** Direct eLitigation HTML for *Robert Tantular v The Stephanie Karina* [2025] SGHC(A) 8, Appellate Division judgment **1 July 2025**, Version No 1; inspected **13 November 2026**. At [123]–[125], the court applied the then-operative s 6(7)/s 6(1) time bar to an established ad hoc fiduciary's breach. At [127]–[128] it **did not decide** whether s 24A applies to equitable fiduciary claims, but assumed applicability for alternative reasoning. At [131] it applied *Lian Kok Hong* [42(a)] to an investor's contemporaneous financial compilation reports; [132]–[139] identified facts supporting knowledge by 2008. The Court found laches [154]–[159] but rejected acquiescence [162]–[163] and dismissed the appeal [164]. The distinct unjust-enrichment route was rejected at [145]–[146]. Case law cited in that judgment was not automatically counted as independently reopened.

**Bounded change:** Updated the existing case map's limitation coverage row, added a pinpointed appellate tranche, and added a dated source/change record. Roadmap updated to preserve the current-statute and fact-specific review gate. The existing Singapore SGX `ledger.json`, five source records, two `unreviewed` legal propositions, tests, software, rights and commercial enquiry content are unchanged. No actual issuer, investor, engagement, litigation instruction, expert clearance or new cause of action is asserted.

**Verification and state:** The official judgment's result and pinpoints were inspected, including the text's 2025 version label; this is **AI source inspection**, not independent legal review or a complete subsequent-treatment search. GitHub branch, diff and exact-head checks require separate confirmation before reporting merge/CI status. Prior direct current-Limitation-Act retrieval was blocked; the Act was not reopened on unchanged access conditions and the current statutory consolidation remains unverified. No local regression or report-generation result is claimed before an actual execution record. Cash cost, owner time and independent adoption are UNKNOWN. The intended beneficiary is a legal researcher avoiding a false limitation assurance. **Next:** inspect any further appellate treatment, obtain the applicable full consolidated statute and actual cause/remedy/knowledge evidence, then obtain qualified independent human review before a checked legal declaration.
