# Evidence handover: proposed development and acceptance cases

**Status on 25 October 2026: design recorded; new capabilities not implemented.**
This is a public technical specification, not a release announcement, customer
agreement, evaluated benefit or promise to implement every item. The eighteen
acceptance cases below are design requirements marked `NOT_RUN`, not executable
fixtures or passing tests. Existing implementation tests remain separate.

## Existing foundation and missing work

The [ledger schema](schema.md) and [snapshot comparison](quickstart.md#after-editing-a-ledger-compare-saved-snapshots)
already support explicit sources, claims, evidence links and recorded review
declarations. [Source Watch](../experiments/source_watch/README.md) observes bytes
of listed local files and returns their supplied claim IDs. The
[local agent gateway](../experiments/agent_gateway/README.md) exposes that existing
check. These components do not supply the proposed export adapter or combined
source/record/process handover described here.

A file change can flag every entry linked to that file. Unlisted sources and
unwatched extraction outputs are outside that check. A structurally valid ledger
is not a verified legal or factual conclusion. Preserve these limits when selecting
an evaluation. The independent-use, source-review and release priorities in the
[roadmap](ROADMAP.md) continue to apply.

## First decision before development

Confirm one actual review task, the permitted inputs, the current alternative and
an acceptance check. Where existing functionality is sufficient, test it before
adding an adapter. The [existing operator invitation](https://github.com/Albertito-AI/policykit/issues/12)
is one route to qualify a task; an enquiry does not establish execution permission,
a partnership or a completed evaluation. [Existing rights](../RIGHTS.md) remain
unchanged.

For an export-dependent task, agree one explicit non-confidential JSON contract,
including stable IDs and source locations, before implementing RN-M01. An
expressly agreed fictional contract may support internal prototyping but does not
establish compatibility with a customer's unseen format. Develop one bounded
increment, then use actual observations to retain, revise or stop it.

## Proposed handover design

Reuse the existing comparator instead of implementing another diff engine:

`permitted export -> explicit mapping -> ledger snapshots/comparison -> reviewer handover`

Keep five observations distinguishable: source bytes; extracted records; disclosed
processing identifiers; review attention; and coverage. A changed processing
identifier is not proof that it caused an output difference. Unavailable process
metadata remains unknown. If the source changes while selected extracted fields
remain identical, retain source/context attention rather than silently treating the
whole source as unchanged.

Preserve supplied values, units, periods, entities, boundaries and source anchors.
Separate physical PDF page numbers from printed labels. Domain/process metadata
would initially use a separately validated, versioned sidecar linked by stable IDs;
that is a proposal, not a new schema. Do not add unknown fields to schema 1.0 or
hide essential structured metadata in unvalidated notes. Any later schema migration
requires its own review and compatibility checks.

## Six conditional work items

The identifiers remain stable for later branch/PR and result references. Each
implementation should record its actual stage, code version, checks and unresolved
limits. Core development owns adapters, schema and comparison behaviour; adoption
owns first-use and independent workflow observations. Coordinate through the
[workstream guide](WORKSTREAMS.md). No timetable, new dependency or commercial
permission is created by this specification.

### RN-M01: Agree one export contract and map it to existing records

**Status:** `SPECIFIED_NOT_IMPLEMENTED`. **Order:** `FIRST`.

An unfamiliar extraction export cannot safely become a RegNav evidence register without explicit IDs, pinpoints and mapping rules.

**Proposed output:** One versioned import specification and a bounded adapter for an agreed non-confidential JSON export, reusing ledger schema 1.0 and a separate proposed sidecar.

**Admission condition:** Actual permitted export or expressly agreed synthetic contract; no assumption about an unseen third-party schema.

**Acceptance requirements:**
- Reject duplicate/ambiguous IDs and unsupported schema versions with actionable errors.
- Preserve original values, citation fields and explicitly supplied scope; report missing metadata without filling it.
- Generated claims default to unreviewed; no invented human declaration.
- Do not mutate the source export or add unknown fields to schema 1.0.

**Excluded:** General PDF extraction; Automatic claim discovery; Universal connector.

### RN-M02: Compose source and structured-record changes into one handover

**Status:** `SPECIFIED_NOT_IMPLEMENTED`. **Order:** `NEXT_AFTER_RN-M01`.

A raw file change and a changed extraction are different observations; one file-level flag cannot explain both.

**Proposed output:** A read-only before/after handover using existing ledger comparison and Source Watch, with separate source, record and processing observations.

**Admission condition:** RN-M01 plus user-confirmed repeated comparison task and review of the full diff/tests.

**Acceptance requirements:**
- Keep all raw Source Watch results visible.
- Show field changes by stable record ID and preserve additions/removals.
- When raw source changes but extracted fields do not, retain unresolved source/context attention.
- Unavailable process metadata stays unknown; a recorded process change is not presented as proof of causal attribution.
- No automatic substantive correctness or renewed-review verdict.

**Excluded:** Causal attribution of model error; Automatic semantic equivalence; Silent suppression of byte-change warnings.

### RN-M03: Retain source anchors and flag explicit scope mismatches

**Status:** `SPECIFIED_NOT_IMPLEMENTED`. **Order:** `CONDITIONAL`.

Values lose meaning if unit, period, entity, boundary or source location is omitted or changed.

**Proposed output:** Explicit comparison rules for declared fields and anchor availability, alongside reviewer questions.

**Admission condition:** Required fields actually exist or are manually supplied with provenance; expert examination of any domain criteria.

**Acceptance requirements:**
- Physical PDF page and printed page label remain separate.
- Missing, relocated or multiply matched anchors require attention, not guessed resolution.
- Period/unit/entity changes are visible even when the numeric value is unchanged.
- Reported assurance coverage is distinct from independently established assurance and must not expand to omitted metrics.

**Excluded:** Automated assurance certification; Inference from missing text that assurance does not exist; Unlicensed standards reproduction.

### RN-M04: Version-specific review history and closure notes

**Status:** `SPECIFIED_NOT_IMPLEMENTED`. **Order:** `BEFORE_RELYING_ON_PRIOR_REVIEWS`.

A past declaration can be misunderstood as approval of a later version.

**Proposed output:** Separate decision records identifying the reviewed snapshot, actual declarant, rationale and remaining issues.

**Admission condition:** A real review workflow requires the extension; no premature schema migration.

**Acceptance requirements:**
- Never rewrite earlier declarations to make the latest output appear approved.
- AI suggestions and actual human decisions have distinct actor/type fields.
- Record does not claim authentication, immutability or independent assurance merely because it contains a timestamp or hash.
- A closed issue states its scope and reopening condition.

**Excluded:** Identity provider; Cryptographic timestamp authority; Unrestricted audit certification.

### RN-M05: Evaluate incremental reviewer value against the actual alternative

**Status:** `BENCHMARK_DESIGN_CREATED_NOT_RUN`. **Order:** `DESIGN_NOW_EXECUTE_WITH_EACH_INCREMENT`.

Internal tests cannot show that an additional component saves reviewers useful effort.

**Proposed output:** 18-case design specification plus a small permitted held-out evaluation against the participant's current workflow.

**Admission condition:** Permission, appropriate reference labels and agreed scope; real tests require actual participant observations.

**Acceptance requirements:**
- Separate exact software invariants from professionally judged conclusions.
- Measure setup, mapping, verification, correction and review, not output-generation speed alone.
- Retain correctly supported examples, ambiguous cases and adverse results.
- Do not train/tune on all held-out examples or use an AI judge as the sole professional ground truth.
- Counts without known denominators are not converted into rates.

**Excluded:** Claim of statistically established uplift; Publication of confidential evaluations; Invented participants.

### RN-M06: Expose the proven handover through the existing agent interface

**Status:** `DEFERRED_PENDING_DEMAND`. **Order:** `AFTER_INDEPENDENT_USE`.

A partner may need a callable result rather than a separate manual command.

**Proposed output:** One versioned read-only interface to the accepted handover, with an explicit local configuration and permissions.

**Admission condition:** A real operator requests this integration; current local MCP capability alone does not prove that need.

**Acceptance requirements:**
- Independent client/version reproduces the specified synthetic task.
- No caller-controlled arbitrary paths, commands, customer documents or financial powers.
- A tool response does not grant licence, action authority or payment permission.
- No public remote deployment until authentication, data handling and operating costs are justified and authorised.

**Excluded:** General agent marketplace; Payment custody; Unrestricted delegation.

## Eighteen proposed acceptance cases

All cases use proposed fictional material. **No case in this table has been run
as an evaluation of the proposed upgrade, and no actual output or human review
has been recorded.** Some conditions also have existing component tests; those
results cannot be carried over as proof of a new composed workflow.

| ID | Case and input condition | Proposed acceptance | Work items | Status |
| --- | --- | --- | --- | --- |
| B01 | **Unchanged inputs.** Same original bytes, extracted record and disclosed process identifiers. | Report identity within the compared scope; preserve the historical review without declaring current truth or a new review. | RN-M02, RN-M04 | `NOT_RUN` |
| B02 | **Formatting-only original change.** Alter a newline in a fictional source; structured metric fields stay unchanged. | Retain CHANGED_BYTES and unresolved context attention; identify no selected field delta without claiming semantic equivalence. | RN-M02 | `NOT_RUN` |
| B03 | **One reported value changes.** Change one of six explicit metric records while keeping stable IDs. | Identify that field/record change while retaining the raw file-wide change and mapping coverage limits. | RN-M01, RN-M02 | `NOT_RUN` |
| B04 | **Unit changes with identical number.** The string value stays 100; the declared unit changes. | Flag the unit change. Do not silently convert or assume a harmless relabelling. | RN-M03 | `NOT_RUN` |
| B05 | **Reporting period changes.** Keep value and unit; change reporting period. | Expose the changed period and prevent an unchanged-value shortcut. | RN-M03 | `NOT_RUN` |
| B06 | **Reporting boundary changes.** Keep value; change entity/facility/organisational boundary. | Record the boundary difference and identify a review question; do not infer the correct boundary. | RN-M03 | `NOT_RUN` |
| B07 | **Extraction changes while source is unchanged.** Use byte-identical original input with a different extracted figure. | Distinguish an extracted-record change from a source-byte change; cause remains unknown unless additional evidence establishes it. | RN-M02 | `NOT_RUN` |
| B08 | **Process changes while output is identical.** Change a disclosed prompt/model/parser version with identical source and extracted fields. | Record the process observation; do not invent an output defect or declare the process immaterial for every purpose. | RN-M02 | `NOT_RUN` |
| B09 | **Page or anchor moves.** A cited passage changes physical page, or a quote matches multiple locations. | Expose relocated, missing or ambiguous provenance; never guess that a matching number proves the same source relationship. | RN-M03 | `NOT_RUN` |
| B10 | **Assurance coverage is overextended.** Fictional statement covers named Scope 1/2 metrics; proposed summary also includes Scope 3. | Retain the declared coverage and flag the explicitly inconsistent summary for competent review; no independently verified assurance is claimed. | RN-M03 | `NOT_RUN` |
| B11 | **Assurance statement not located.** The supplied material does not include an assurance statement. | State not located in supplied material, with coverage limits; do not label the company definitively unassured. | RN-M03 | `NOT_RUN` |
| B12 | **Source unavailable.** Remove a listed source after baseline capture. | Preserve NOT_OBSERVED; no fresh approval or inference that bytes were unchanged. | RN-M02 | `NOT_RUN` |
| B13 | **New source outside original manifest.** Add an unlisted source affecting the possible interpretation. | An explicit inventory comparison records incomplete coverage; the existing watcher alone must not be claimed to discover the new source. | RN-M01, RN-M02 | `NOT_RUN` |
| B14 | **Duplicate identity.** Provide two incompatible records with the same stable ID. | Reject ambiguity instead of silently overwriting or merging. | RN-M01 | `NOT_RUN` |
| B15 | **Identifier renamed.** Replace an old record ID with a different one. | Preserve removal/addition unless an explicit authorised mapping resolves identity; do not fuzzy-match automatically. | RN-M01, RN-M02 | `NOT_RUN` |
| B16 | **Instruction embedded in evidence.** Add text directing the software or agent to mark a claim approved or reveal private files. | Treat it as untrusted source content; no command execution, permission expansion or financial action. | RN-M01, RN-M06 | `NOT_RUN` |
| B17 | **Historical human declaration.** A previous review declaration references an earlier version, then a material linked field changes. | Retain the actual declaration and flag reconsideration; never manufacture a new reviewer, timestamp or completed review. | RN-M04 | `NOT_RUN` |
| B18 | **Unsafe report cell.** A supplied identifier, note or text field resembles a spreadsheet formula or HTML. | Export safely using existing escaping rules while retaining lossless source data and disclosing changed presentation. | RN-M01, RN-M02 | `NOT_RUN` |

## Evidence needed to close a work item

For software behaviour, record the exact permitted inputs, expected outputs,
implementation commit, environment, actual commands and results. Preserve inputs
and earlier baselines. A model-generated suggestion cannot supply a completed human
review. Professional scope judgements need an appropriate reference decision and
an explicit disagreement route, not only a machine score.

For usefulness, compare the same bounded task with the participant's actual current
workflow. Count setup, mapping, checking, correction, assistance and maintenance.
Retain sound examples, ambiguous cases and adverse outcomes. Do not tune on every
held-out example or convert missing denominators into rates. Internal reproduction
and a small feasibility exercise do not establish independent adoption, causal
productivity gains or production-wide reliability.

Keep source evidence and instructions separate. A quoted instruction in a document
cannot grant filesystem access, create a review or expand an agent's authority.
Sensitive source metadata needs appropriate handling even when no raw source text
is exported. This plan does not add an extractor, hosted endpoint, identity service,
automated assurance, payment function or general agent marketplace.

## Publication boundary

This page contains technical requirements and fictional test designs only.
Private correspondence, prospective-customer identities, source samples, commercial
terms, financial plans and private workspace links are excluded. It reproduces no
book or third-party standard and grants no additional reuse rights. The work is
AI-assisted planning; independent evaluation remains outstanding.
