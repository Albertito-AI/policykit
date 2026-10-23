**Fictional sample report.** The generated section below is the unedited Markdown
output of the existing CLI for the bundled training ledger. All source texts,
propositions, dates, reviewer identities and `example.org` links in it are
fictional. It contains no actual law or observations from an external pilot.

Use the [ten-minute quickstart](quickstart.md) to follow the example, and read
[the complete source packet](../examples/training_sources.md) alongside the
matrix. The output identifies structural and recorded review gaps. It does not
establish legal truth, source relevance or the quality of a human review.

To reproduce the generated section, run from the repository root:

```bash
python -m regnav_evidence report examples/synthetic_ledger.json --format markdown
```

Generated on 23 October 2026 with Python 3.12.14. The report exits `0`; the
notice about three warnings is written separately to standard error. It is not
part of the generated Markdown below. Normal validation exits `0`; validation
with `--strict` exits `2` for this unchanged fixture.

The [rights statement](../RIGHTS.md) remains applicable. This page adds no reuse
licence and makes no claim of independent evaluation.

---

<!-- BEGIN GENERATED REPORT -->
# Synthetic training example: recording an internal review procedure

Structural checks only. Review status is a user-declared human assessment; this software does not verify sources, quotations, legal validity or factual truth.

All source texts, propositions, dates and reviewer details in this file are fictional training fixtures. They express no actual law. The example.org URLs are illustrative and are never fetched. See training\_sources.md for the complete mock texts.

Sources: 2. Propositions: 3.
User-declared statuses: 1 unreviewed, 1 checked, 1 contested.

## Evidence matrix

| Claim ID | Proposition | User-declared review | Source ID | Pinpoint | Relation |
| --- | --- | --- | --- | --- | --- |
| CLAIM-logging | Draft A states that requests are entered in a log before review. | checked | SRC-draft-a | A.2 | supports |
| CLAIM-remedy | The drafts provide a further review procedure after an initial decision. | unreviewed | SRC-draft-b |  | context |
| CLAIM-timing | The draft procedure specifies a response within five working days. | contested | SRC-draft-a | A.3 | supports |
| CLAIM-timing | The draft procedure specifies a response within five working days. | contested | SRC-draft-b | B.2 | contradicts |

## Source register

| Source ID | Title | Type | Jurisdiction | Version / as of | URL |
| --- | --- | --- | --- | --- | --- |
| SRC-draft-a | Synthetic internal procedure, draft A (training fixture) | other | Fictional training setting | Draft A / 2025-01-01 | https://example.org/regnav-training/draft-a |
| SRC-draft-b | Synthetic internal procedure, draft B (training fixture) | other | Fictional training setting | Draft B / 2025-01-01 | https://example.org/regnav-training/draft-b |

## Human-review declarations

| Claim ID | Reviewer | Review date | Treatment of contrary evidence |
| --- | --- | --- | --- |
| CLAIM-logging | Synthetic reviewer (training fixture) | 2025-01-02 |  |
| CLAIM-remedy |  |  |  |
| CLAIM-timing | Synthetic reviewer (training fixture) | 2025-01-02 |  |

## Outstanding structural and review notices

- UNREVIEWED\_CLAIM ($.claims\[1\]): No completed human review is declared for this proposition.
- MISSING\_PINPOINT ($.claims\[1\].evidence\[0\].pinpoint): Identify a page, paragraph, provision, section or other reproducible location.
- CONTESTED\_CLAIM ($.claims\[2\]): This proposition is recorded as contested; retain the disagreement in any summary.

The ledger's JSON is the authoritative record. This matrix is a view of its recorded entries.
<!-- END GENERATED REPORT -->
