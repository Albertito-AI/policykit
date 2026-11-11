# RegNav roadmap

## Purpose

Make the evidence and interpretive choices behind legal propositions easier to
inspect. Begin with legal accountability in sustainability reporting across
Asian jurisdictions. Build reusable methods before expanding coverage.

## Current components

Version 0.1 provides an offline evidence ledger, structural validation,
Markdown and CSV reports, read-only comparison of saved snapshots,
a synthetic worked example and regression tests. The optional
[ESG workbench](ESG_WORKBENCH.md) adds report ingestion, source tracing,
candidate extraction, local retrieval, explicit inventory calculations,
materiality screening and action planning. Its PDF/table/spreadsheet parsers
have documented optional dependencies; the core ledger and text workflow
retain their standard-library implementation.

The [README](../README.md) now provides a feature overview, concrete fictional
outputs and a complete PDF-to-ledger quickstart, with the separately maintained
private research extension clearly identified. Teaching materials, an external
usability protocol and a narrow unreviewed Singapore case remain available.
Real-world usefulness, educational benefit and legal dataset quality still
require evaluation. See the [project status](project_status.md) for the evidence
baseline.

## Completed safeguard: compare saved ledger versions

The read-only `compare` command identifies substantive changes to propositions,
evidence links and source records and flags potentially stale prior declarations.
Metadata-only access-date and review-declaration updates are distinguished.
Identifiers are matched literally; any renamed identifier is recorded as a
removal and addition. No reviewer is authenticated and no review status is
changed by the command. Further refinement should be driven by actual review
friction rather than speculative features.

## Evidence-export integrity

Markdown evidence reports should retain the literal wording of recorded
propositions and source titles, including GitHub-flavoured Markdown's
strikethrough delimiters (`~~`). A targeted exporter regression protects
these delimiters from being interpreted as deletions in the rendered report.
The JSON remains the authoritative record; exported formatting is not evidence
that any proposition is correct. Follow up on concrete user-reported rendering
problems rather than adding speculative export formats.

## ESG workbench: duplicate-source navigation safeguard

When identical source bytes are supplied twice, the default source identity
and generated HTML page anchors coincide. The workbench now rejects these
ambiguous duplicate inputs before writing a workspace. A synthetic regression
covers duplicate paths and same-content copies, while ordinary single-source
work remains supported. This is a source-navigation integrity correction,
not verification of substantive evidence. Next, reproduce the first-use
workflow independently and assess actual review effort and anchor usability.

## ESG activity import: concealed formula-like prefixes

CSV, TSV and optional XLSX activity imports now reject a formula-like opening
character even when hidden after leading Unicode format/control characters.
The earlier guard only stripped ordinary whitespace; it missed examples such
as a word joiner followed by `=`. This prevents those strings from being
accepted as ordinary activity identifiers or headings. It does not evaluate
formulas, modify retained values or establish how every spreadsheet program
will handle such text. Continue to prioritise real first-use observations and
source-navigation evaluation; expand import rules only for a reproducible case.

## Next work in priority order

The maintainer's 28 October instruction adds a parallel, implemented technical
workstream: the [local ESG workbench](ESG_WORKBENCH.md). Its next actionable
item is a permissioned independent report-pair evaluation and a live,
operator-configured model test. Have the evaluator follow the README entry route
and record setup obstacles and output misunderstandings alongside anchor
correctness, field coverage, OCR/table errors and review effort. Use those
observations to prioritise further engineering. Do not equate implemented
functions with commercial-platform parity.
The source-review and teaching evaluation priorities below remain outstanding.

1. **Obtain human review of the first worked case.** The
   [Singapore example](../cases/singapore-sustainability-reporting/README.md)
   retains two unreviewed propositions, now including a narrow Mainboard
   Rule 703 qualification so an annual sustainability-report deadline is not
   mistaken for a waiver of separately triggered market disclosure. A reviewer
   should test the issuer's period, any assurance condition, actual internal
   review evidence, Rule 703 thresholds and exceptions, and each source link
   before declaring completion. The five-source case remains AI-prepared:
   preserve the independent human-review gate for every checked proposition.
   Under the 26 October expansion instruction, bounded, issue-selected
   [common law authority mapping](../cases/singapore-sustainability-reporting/common-law-authorities.md)
   may proceed as **AI-prepared research** while the two existing SGX propositions
   remain unreviewed. A source map does not authorise a checked legal finding,
   an issuer-specific remedy or a claim of exhaustive subsequent treatment.
   The 11 November bounded source correction adds the previously omitted *Ikumene* [1993] SGCA 50 [24]–[30], [32]–[38] on the statutory auditor's purpose, guarantor standing and causation, and checks *Tan Juay Pah* [2012] SGCA 17 [69]–[72] as express later appellate treatment. This does not decide investor-facing sustainability assurance duty. Future case research should test further subsequent treatment and the actual engagement before inferring a claimant or remedy; independent human review remains compulsory.
   The 9 November case-law pass adds an express-third-party indemnity and judicial-costs distinction from *Lee Hsueh Ching* [2025] SGHC 258 [160]–[180], [183]–[191]. It strengthens the contract-specific issue map without inferring an ESG investor's right. The official current-version CRTPA index now supplies provision-level text, but direct full-Act reading still returns 403. The next legal gate is full consolidated text, a real engagement contract and appellate-treatment review; the original SGX ledger remains unreviewed.
   The [landmark and key case workflow rationale](CASE_LAW_WORKFLOW.md), recorded
   on 29 October, guides this expansion. The 2 November case research pass corrected a particular **appeal-treatment risk**:
   *Tan Woo Thian* [2021] SGCA 20 dismissed the negligence claim on causation while
   expressly leaving the professional fact-finder's duty to non-clients **open**;
   *CLAAS* [2010] SGCA 3 maps a separate contractual-third-party route. The next
   case action is to verify the full current Contracts (Rights of Third Parties)
   Act, engagement-specific beneficiary/reliance terms and any later treatment,
   **then** agree and trial a small structured tranche with core development.
   Preserve source pinpoints, qualifications and unreviewed states. Record the
   tranche's coverage and gaps. Global coverage, treatment automation and
   application models remain development directions; actual qualified review
   of legal propositions and independent usability evidence remain outstanding.
2. **Run the first external usability pilot.** Use the prepared
   [protocol](evaluation_protocol.md) with three independent volunteers. Record
   task completion, assistance, misunderstandings and reproducible difficulties
   privately. Revise concrete defects and report bounded, anonymous results.
   Keep the answer key linked from the manual quickstart for post-task checking;
   do not supply it before observed responses, and record earlier exposure.
   The manual-first sequence is not a controlled comparison and cannot establish
   a productivity or learning benefit. Design any later comparative evaluation
   separately.
3. **Improve entry and review.** Choose a CSV import or an accessible browser
   editor only after observing where users struggle. Preserve offline access
   and the JSON record. Check import ambiguities and export fidelity.
4. **Extend the legal comparison.** Add the second jurisdiction when the first
   worked case is stable. Distinguish disclosure duties, supervision, liability,
   standing and remedies. Record disagreements rather than forcing equivalence.
5. **Prepare a citable release.** Follow the
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

## Bounded technical experiment: source-file changes

On 24 October 2026 the maintainer requested a separate technology-product
experiment alongside the research programme. [Source Watch](../experiments/source_watch/README.md)
checks byte changes in explicitly listed local files and returns their linked
claim identifiers. It is isolated from the ledger schema and command interface.
A runnable fictional demo and generated report make the proposed behaviour
inspectable without receiving confidential material or paying for a hosted service.

The next gate is independent reproduction under an agreed permission and a
concrete recurring user need, not more speculative features. CONTRIBUTING.md
now distinguishes public synthetic bug reports from private Source Watch
rights, evaluation and commercial enquiries.
The root README now leads to the generated report and a short evaluation enquiry route. Record
actual enquiries and permissions separately from completed evaluations or paid
work. Record missing sources, false-positive friction,
requested integrations and the limits of any observation. Do not build a hosted
API, external-source crawler or new dependency merely to fill a schedule.
The existing human source-review and teaching-pilot priorities remain outstanding.
No subscription, commercial licence, production service or customer adoption is
established by this experiment. Preserve the existing rights statement.

## Public website link

The README now links to [Albert Tan's website](https://www.alberttansinhon.com/).
At the next public-link review, check that this canonical address still resolves.

## Agent interoperability: one bounded first connection

The maintainer requested this integration on 25 October 2026. The
[local MCP gateway](../experiments/agent_gateway/README.md) now makes the existing
Source Watch check callable by a permitted local client without granting caller
control of paths, shell commands or the baseline. The
[network proposal](AGENT_NETWORK.md) and technical issue form provide an opt-in
route; the catalogue records no external partners, public endpoint or payment.

The next gate is one independent, permissioned MCP-client reproduction with
fictional inputs and an actual recurring workflow to assess. Record client and
protocol versions, setup effort, output interpretation and unresolved defects.
A public registry entry requires its own packaging, namespace, rights and
verification steps. External delegation needs separate authentication and task
controls. Do not describe the local prototype as a deployed marketplace or
substitute simulated exchanges for partners or customers. Existing human source
review and teaching-pilot priorities remain unchanged.

The root README now links directly to the gateway, generated exchange, catalogue
and existing pilot invitation. Use that route to qualify one operator's actual
task and agree the necessary permissions before an independent test. Record a
reply, a completed evaluation and a paid agreement separately; do not count this
navigation improvement as external use or a new participant.

## Experimental evidence-handover implementation

The [evidence-handover plan](EVIDENCE_HANDOVER_PLAN.md) now records the actual
implementation stage of all six items. The [local experiment](../experiments/evidence_handover/README.md)
accepts one explicit JSON contract, maps it to the unchanged ledger schema and
retains scope/process metadata separately. It composes source, record and process
observations, preserves supplied review history and offers an opt-in local MCP tool.
The eighteen disclosed engineering cases now have runnable tests and a generated
result; independent workflow evaluation remains outstanding.

An additional handover regression now checks byte divergence for a previously
unlinked, recorded source when it first gains a claim link. This preserves the
distinction between the existing Source Watch linked-file report and the full
snapshot's retained source observations.

The next action is one permitted independent reproduction and inspection of an
actual export. Do not claim customer compatibility from the fictional contract.
Use existing simpler tools when adequate. Fix observed defects before expanding
parsers, hosted services or protocols. Each material change needs a regression,
focused checks, updated benchmark evidence, full-diff review and applicable CI.
Preserve the original design in Git history, core-development/adoption ownership,
current human-review priorities, offline use, existing rights and no invented
human declarations. No deployment, professional assurance or commercial outcome
follows from internal implementation.

## Demonstration entry and next observation

The [README demonstration](../README.md#see-it-in-action) now connects the existing
fictional ledger, actual command output and generated evidence matrix in one
visual entry point. The next adoption action remains the prepared independent
usability pilot: record prior exposure to this demo and actual difficulties in
connecting warnings to source links. Use those observations to correct concrete
friction. The demonstration does not establish that a pilot or human legal review
has occurred, and it changes no runtime or reuse rights.

## 30 October 2026: legal case research gate

The common-law map now includes a focused source-inspected financial-auditor tranche under [Singapore sustainability reporting](../cases/singapore-sustainability-reporting/common-law-authorities.md): *Deloitte v Hin Leong* [2026] SGCA 33 and its cited *JSI Shipping* and *PlanAssure* decisions. It distinguishes a company's statutory-audit engagement, factual causation, contractual remoteness and contributory fault from any still-unverified investor right against a sustainability assurer. This is issue-based legal research and changes no ledger review state. Next case action: obtain an actual usable assurance-engagement scope and period-specific statutory text, and independently examine the evidence for possible investor standing before proposing new reviewed propositions. Do not create a generic insurer/assurer liability entry from financial-audit analogies. Coordinate structured case-record work with core development; independent human legal review remains the condition for a checked claim.

## 4 November 2026: third-party assurance-contract remedies and forum

The Singapore [authority map](../cases/singapore-sustainability-reporting/common-law-authorities.md) now distinguishes third-party contractual entitlement, remedies, defences, limitation and dispute forum, anchored in opened *VKC* [2021] SGCA 72 and *Low Jun Hong* [2026] SGHCR 11. The official 2020 Revised Edition of the Contracts (Rights of Third Parties) Act was visible in an indexed search record, but direct retrieval of the consolidated statute returned HTTP 403; this is **not** a completed full statutory check. Next case gate: obtain the applicable actual assurance contract, directly verify the current statute and any appeal from the Registrar's ruling, then assess how each clause affects an identified claimant. Preserve the two unreviewed ledger propositions; the source map creates no third-party ESG entitlement or actual remedy.

## 1 November 2026: interrupted output-write recovery

The ESG workbench now attempts to remove its planned output filenames if an
output write raises an exception, and removes its new directory only if empty.
A synthetic failure test writes partial data on the second file before raising
an error, verifies cleanup, and retries the complete ordinary workflow.
Previously this could leave a misleading partial workspace that blocked retry.
This is best-effort process-level cleanup, not a transactional filesystem or
a guarantee against abrupt termination and concurrent writers.

Next priority remains a permissioned independent first-use review, including
source navigation and whole-task effort. Preserve unreviewed legal claims and
record actual failure or usability evidence before adding further features.

## Foundations paper and Wiki publication

The owner-requested [whitepaper](../wiki/Whitepaper.md) explains first principles,
public-interest purpose and proposed progression. Next documentation action:
initialise the GitHub Wiki, let the bounded publisher run and verify the actual page.
This documentation work does not complete the independent report-pair evaluation,
live-model check or qualified legal review above. Keep the paper aligned with
observed capabilities and preserve disagreements and unsuccessful evaluations.

## 6 November 2026: limitation source gate for the Singapore case

The [Singapore authority map](../cases/singapore-sustainability-reporting/common-law-authorities.md) now distinguishes accrual of actionable damage, discovery of facts triggering the alternative statutory period, continuing consequences and truly new breaches. Opened *Lian Kok Hong* [2008] SGCA 30 and its identified subsequent appellate application in *IPP Financial Advisers* [2020] SGCA 47. The latter concerned an investor's negligent-misrepresentation claim and found it time-barred. These are historical judgments, not an ESG limitation opinion. Current consolidated Limitation Act s 24A direct retrieval failed (HTTP 403); do not infer that the historical statutory text is unchanged. Next case gate: inspect the period-matched current Act, any further appellate treatment and the actual pleaded cause, accrual facts and knowledge before proposing a deadline or human-checked legal proposition. Preserve the unchanged unreviewed SGX ledger and existing assurance-contract evidence gates.

## Release packaging verification

The release lane has added a reproducible isolated-wheel check to the CI
matrix. Its result is evaluated at each exact head; it must not be confused
with an authorised published release or independent first use. The separately
maintained source-tree experiments are deliberately excluded from the wheel.
The next release decision is to reconcile citation/distribution identity,
inspect the intended candidate archive and confirm the applicable rights and
user-facing scope before any formal release. Continue the independent-user
and qualified human legal-review gates in their respective lanes.
