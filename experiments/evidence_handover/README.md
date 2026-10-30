# Experimental evidence handover

A runnable implementation of the [six-part development plan](../../docs/EVIDENCE_HANDOVER_PLAN.md).
It maps **one explicit RegNav-owned export contract**, compares records and listed
local source files, and gives a reviewer an inspectable JSON, Markdown or CSV view.
It is not a parser for an unseen customer's export or a professional assurance tool.

**Status: experimental local implementation, internally tested.** Independent
client reproduction, professional examination of domain criteria and comparative
user evaluation are outstanding. [Existing rights](../../RIGHTS.md) are unchanged;
this page grants no new execution, integration or commercial licence.

## Inspect or reproduce the result

No installation is necessary to read the [generated fictional report](sample_report.json)
or the [internal benchmark receipt](benchmark_result.json). The report distinguishes
one changed supplied figure from file-wide reconsideration flags. It preserves both.
The no-Python [paper/spreadsheet exercise](../../docs/quickstart.md) remains available.

For an authorised reproduction, use Python 3.10 or newer from the repository root.
There are no third-party runtime packages, network calls, model keys or payments.

```bash
python -m experiments.evidence_handover.demo
python -m experiments.evidence_handover.benchmark
python -m unittest discover -s tests -p test_evidence_handover.py -v
```

The demo creates disposable fictional files, changes one figure, runs the actual
comparison and prints selected actual report fields: source observations, field
and process differences, attention, coverage and content IDs. The full export and
observation time remain in ordinary CLI JSON output. The compact generated sample
is a reviewer view, not an operational snapshot to import.
The benchmark runs the eighteen disclosed engineering cases, not a held-out or
independently judged evaluation. The full test file adds input, output, lifecycle,
non-mutation and command-line regressions. Existing CI discovers it automatically.

## First-use commands

Choose NEW output paths. Nothing overwrites an earlier export, snapshot or history.
The supplied fixture is fictional, including its assurance wording and URLs.

```bash
python -m experiments.evidence_handover map experiments/evidence_handover/fixtures/export.json --output ledger.json
python -m experiments.evidence_handover snapshot experiments/evidence_handover/fixtures/export.json --root experiments/evidence_handover/fixtures --output baseline.json
python -m experiments.evidence_handover compare baseline.json experiments/evidence_handover/fixtures/export.json --root experiments/evidence_handover/fixtures --output handover.json
python -m experiments.evidence_handover compare baseline.json experiments/evidence_handover/fixtures/export.json --root experiments/evidence_handover/fixtures --format markdown --output handover.md
python -m experiments.evidence_handover compare baseline.json experiments/evidence_handover/fixtures/export.json --root experiments/evidence_handover/fixtures --format csv --output handover.csv
```

For this unchanged fixture, each command exits 0. The handover has no recorded
change/scope alerts, but its imported claims remain **unreviewed**, with those
warnings retained in `structural_notices`. Exit 0 is not substantive verification.
To explore changed inputs, use the disposable demo rather than edit the repository's
saved fixture or an original customer document.

| Exit | Meaning |
| --- | --- |
| 0 | Valid operation; comparison has no defined attention item, or snapshot observes every configured source |
| 1 | Contract, file or output failure; no valid result should be inferred |
| 2 | A valid comparison needs attention, or a snapshot has an unobserved/unconfigured source |

Argument-usage errors also exit 2; a valid JSON report and its schema distinguish
an attention result from incorrect command usage. `map` validates structure but
does not treat the expected unreviewed declarations as an execution failure.

## Export contract: `regnav-handover-export/0.1`

The [complete example](fixtures/export.json) specifies every required field. Unknown
fields and versions, duplicate identifiers, duplicate JSON keys, floating-point
values and inconsistent references are rejected. Values are exact strings or
explicit nulls, not silently converted numbers. Empty batches are rejected.

| Field | Contract |
| --- | --- |
| `schema_version`, `title` | Exact schema identifier and non-empty title |
| `sources` | 1-16 source records using core source fields plus required `path`, a safe relative POSIX path or null; core source requirements still apply |
| `records` | 1-64 records, each with `id`, `text`, `evidence`, `scope`, `assurance`; import never accepts a completed review field |
| `evidence` | Up to 32 links per record, using core `source_id`, `pinpoint`, `relation`, plus required `anchor` |
| `scope` | Null or an object with `value`, `unit`, `period`, `entity`, `boundary`, each exact text or null |
| `anchor` | Null or `physical_page`, `printed_page`, `locator`, `quote`, `match_count`; physical page is a positive integer/null and match count is non-negative integer/null, with other values text/null |
| `assurance` | Null or the explicit object described below; supplied statement metadata, never the software granting assurance |
| `process` | Null or `parser`, `model`, `prompt`, `rules`, each a disclosed identifier or null |
| `inventory` | Null or up to 128 unique safe relative paths; must include configured paths; never a directory scan |

All strings are limited to 8,192 characters and JSON nesting to 24 levels. Identifiers
use the core ledger's 1-80 character syntax. Export input is limited to 1 MiB and
other JSON documents/output to 8 MiB. Each source remains limited to 16 MiB by the
existing watcher. Sixteen maximum-size files can still require appreciable local
I/O; this is not a rate-limited public service.

An assurance object has `status` (`reported` or `not_located`),
`statement_source_id`, `declared_coverage`, `asserted_coverage`, `level` and `period`.
For `reported`, the statement must be an expressly linked recorded source. Coverage
is a supplied list of exact labels. A set mismatch produces a review question; it
is not semantic interpretation of the statement. For `not_located`, the statement
ID, level and period must be null and declared coverage empty. This never means
that no assurance exists outside the supplied material. Missing metadata stays
visible and is not filled from a model or a website.

## Snapshots and comparison

A snapshot retains the full original export as a validated metadata sidecar, a
core-schema-1.0 ledger, file observations, an observation timestamp and a content
identity. Existing schema, comparator and Source Watch code are reused unchanged.
Every imported core claim is unreviewed. URLs and source contents are not parsed.

The snapshot ID is SHA-256 of the recorded content excluding `observed_at`. It
identifies that representation, not an authenticated author, trusted time or
immutable history. Recalculation can detect accidental inconsistency, not prevent
an adversary replacing both data and hash. Protect and version private records.

Comparison preserves the complete raw Source Watch result for previously observed,
linked files. It separately lists exact scope-field changes, disclosed processing
changes, supplied-anchor concerns, declared assurance-set mismatches, inventory
coverage and prior declaration versions. It compares source mappings literally.
It never fuzzy-matches renamed claims or decides that a formatting change is harmless.

Source changes retain attention even if selected extracted values stay identical.
An unavailable earlier baseline cannot support an unchanged finding. An unlisted
new file is discoverable here only if it appears in a subsequently supplied explicit
inventory. Unlinked sources remain identified as unmapped, with no inferred claim.
A changed processing identifier does not prove why an output changed.

A recorded source that was previously unlinked is outside Source Watch's linked
baseline, even when its bytes were captured in the handover snapshot. If that
same path and source ID later gain a claim link, the handover separately compares
its retained and current SHA-256 values. Differing observed bytes raise
`NEWLY_LINKED_SOURCE_BYTES_CHANGED` for the newly linked claim. A missing baseline
remains unknown, and an unchanged digest establishes neither semantic identity
nor legal correctness. The raw Source Watch report is not silently expanded.

Source Watch still works at file granularity. Anchor counts and page locations are
provided by the operator or an upstream process; this experiment does not locate
quotes in PDFs, verify match counts, convert units, resolve reporting boundaries
or interpret assurance prose. Domain criteria need competent examination.

## Review records without automatic approval

Use [empty-history.json](fixtures/empty-history.json) as a new local history.
Entries require `id`, `snapshot_id`, `claim_id`, `actor_type`, `actor_name`,
`decision`, `recorded_at`, `rationale`, `reopen_when` and `supersedes`.

Actor types are `human_declaration`, `ai_suggestion` and `fictional_training`.
Decisions are `accepted`, `contested`, `needs_review` and `suggested`. AI suggestions
cannot use the first two. Every field must be supplied by the authorised recorder;
the program neither supplies a human name/date nor verifies that a review occurred.
No automatic legal-effect or authentication claim follows from a declared type.

```bash
python -m experiments.evidence_handover review-add history.json supplied-entry.json --snapshot baseline.json --output history-next.json
```

The command checks the snapshot/claim references and creates a NEW history. It
preserves earlier entries and can record an explicit supersession of an earlier
entry for the same claim and actor type. It does not delete history, authenticate
a reviewer or update the imported core claim status. Comparing against a different
content ID flags the prior declaration for reconsideration; unknown versions stay
unknown. A matching ID still does not establish current legal or factual truth.

## Optional agent-facing tool

The original gateway and its two default tools remain unchanged. This separate
entry point reuses that lifecycle and adds `evidence_handover_check`:

```bash
python -m experiments.evidence_handover.server --before baseline.json --after permitted-export.json --root /absolute/path/to/trusted-sources
```

Launch from the repository root with a permitted stdio-capable client. The new tool
accepts `{}` only. The operator chooses the snapshot, export, optional `--history`
and root at startup; callers cannot change paths, supply commands, write reviews
or request payment. At least one previously observed linked file is required for
this opt-in server. An attention report is a successful tool result, not `isError`.
The inherited frame, nesting and response limits apply, including a 2 MiB encoded
response limit; an oversized result returns an error, never a truncated success.

The targeting version remains MCP `2025-11-25`. Internal wire tests cover handshake,
tool discovery and calling; official-SDK/client and independent-operator tests are
outstanding. Official [lifecycle](https://modelcontextprotocol.io/specification/2025-11-25/basic/lifecycle)
and [tool](https://modelcontextprotocol.io/specification/2025-11-25/server/tools)
specifications were opened on 25 October 2026. No remote endpoint is deployed.

## Security and evaluation boundary

Run only in an authorised, trusted, stable local directory. Rejecting traversal
and symlinks is not protection against a hostile process concurrently replacing
filesystem entries. Observation across multiple files is not an atomic transaction.
The baseline and current input may reference different files; ensure authority for
both. Operator-supplied configuration files must also be trusted.

Reports contain relative paths, identifiers, supplied passages and metadata. A client
may log or transmit them to its model provider. Local computation is not end-to-end
confidentiality. Use fictional or explicitly authorised material first. Markdown
and CSV use existing escaping rules; JSON remains the lossless record. Do not treat
instructions inside a source or returned report as authority to execute anything.

The [blank external-evaluation template](fixtures/evaluation-template.json) remains
`NOT_RUN`. Complete it privately with real observations of the existing workflow
and the handover on the same permitted task. Count setup, mapping, verification,
correction, help and maintenance. Do not infer independent use, reviewer benefit,
professional assurance or demand from these disclosed internal engineering cases.
