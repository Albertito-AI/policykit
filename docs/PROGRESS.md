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
