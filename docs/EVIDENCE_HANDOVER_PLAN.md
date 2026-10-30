# Evidence handover: implementation and remaining evidence

**25 October 2026: an experimental local implementation now exists.** The maintainer
expressly authorised implementing the six recorded items for internal testing.
The [original specification](https://github.com/Albertito-AI/policykit/blob/30105eb8c08131528e66535bea20ef634a20a674/docs/EVIDENCE_HANDOVER_PLAN.md)
remains available as the pre-implementation baseline. Its acceptance requirements
are not silently replaced by claims of professional or commercial success.

Start with the [working experiment and input contract](../experiments/evidence_handover/README.md),
[generated fictional report](../experiments/evidence_handover/sample_report.json),
[benchmark receipt](../experiments/evidence_handover/benchmark_result.json) and
[executable tests](../tests/test_evidence_handover.py).

## Six work items: actual stage

| ID | Implemented for internal testing | Evidence still outstanding |
| --- | --- | --- |
| RN-M01 | Strict RegNav-owned JSON export contract; lossless sidecar, core-schema mapping and unreviewed imports | Compatibility with any independent operator's actual permitted export |
| RN-M02 | Existing ledger comparison composed with raw Source Watch results; separate record, source, process and inventory observations | Repeated independent comparison task and demonstrated whole-workflow usefulness |
| RN-M03 | Exact unit/period/entity/boundary deltas, supplied-anchor checks and declared assurance-set consistency | PDF anchor discovery, semantic judgement, professional validation and any automatic interpretation remain outside the implementation |
| RN-M04 | Version-specific supplied declarations; new-file history extension, explicit actor types, supersession and reconsideration flags | Authenticated reviewer identity and actual human review are not supplied by this software |
| RN-M05 | Eighteen disclosed synthetic engineering cases, a runnable benchmark and blank comparative evaluation template | Independent/held-out evaluation, expert reference decisions and productivity claims remain NOT_RUN/unsupported |
| RN-M06 | Opt-in local stdio wrapper reusing the existing MCP gateway and adding one operator-configured read-only tool | Official SDK/client checks, independent client reproduction and any remote deployment |

No general PDF extractor, unit converter, assurance engine, public network endpoint,
marketplace, payment service, new runtime dependency or additional licence is added.
The existing core ledger, schema, Source Watch and default agent gateway are unchanged.

## The eighteen design cases

Each row is implemented as the corresponding `test_Bnn_...` method. The current
[generated receipt](../experiments/evidence_handover/benchmark_result.json) records
actual outcomes and source-file hashes. A pass concerns the disclosed software
assertions below, not independent domain validation of the broader design criterion.

| Case | Tested assertion and important limit |
| --- | --- |
| B01 | Unchanged recorded inputs; no new review or truth finding |
| B02 | Cosmetic source edit retains file-level attention, without semantic-equivalence inference |
| B03 | One supplied value delta remains distinct from broader raw file flags |
| B04 | Unit change is exposed without automatic conversion |
| B05 | Period change is exposed despite an unchanged numeric value |
| B06 | Boundary change is exposed without deciding the right boundary |
| B07 | Extraction-record change stays distinct from source-byte change |
| B08 | Declared process-only change produces no invented output error or causal explanation |
| B09 | Supplied page changes/ambiguous match counts produce attention; no PDF matching is claimed |
| B10 | Explicit declared-versus-asserted coverage sets are checked; prose interpretation and professional reference validation remain outstanding |
| B11 | A not-located statement does not become a finding of no assurance |
| B12 | Missing listed source remains NOT_OBSERVED |
| B13 | A new path in a supplied inventory is identified as outside the watch; no automatic directory discovery |
| B14 | Duplicate record identity is rejected |
| B15 | Renamed IDs remain removal/addition without fuzzy matching |
| B16 | Embedded instructions remain inert data and cannot create a completed review |
| B17 | A labelled fictional historical declaration is preserved and flagged against changed content; no actual human review is claimed |
| B18 | Unsafe cells are escaped in views, with original text retained in JSON |

A later regression also covers a recorded but previously unlinked source becoming
linked after its local bytes changed. Its snapshot hash is compared with current
observed bytes without claiming the source was included in the original linked
Source Watch baseline. A missing original observation remains explicitly unknown.

Additional regressions test malformed inputs, limits, exclusive file creation,
snapshot consistency, declaration constraints, CLI exit codes and the local MCP
wire path. These tests use original fictional fixtures only. They do not reproduce
private correspondence, client records, manuscripts or third-party standards.

## Next step and continuing improvement

Use the existing simpler component when it already meets an authorised task.
For the new handover, obtain one permitted independent reproduction and inspect
one actual export before promising compatibility. Keep an explicit acceptance
condition and compare the complete work against the participant's current method.
Record setup, mapping, checking, help, correction and maintenance, including adverse
results. No rates without known denominators; no model score as the sole
professional ground truth.

For each substantive change: reproduce the defect or specify the accepted behaviour,
add the smallest meaningful regression, implement it on an isolated branch, run the
focused tests and benchmark, inspect the full diff, then verify applicable CI before
merge. Update the generated benchmark receipt when its source-file hashes change.
Run the existing full suite for material cross-component changes. Do not manufacture
commits, new features or passing evaluations to meet a cadence.

Core development owns implementation; adoption owns independent first-use evidence.
The [workstream guide](WORKSTREAMS.md), [research standard](RESEARCH_STANDARD.md),
[roadmap](ROADMAP.md) and [existing rights](../RIGHTS.md) remain controlling.
Independent evaluation, human source review, delivery, release and payment are
separate evidence states. This implementation makes no claim about those outcomes.
