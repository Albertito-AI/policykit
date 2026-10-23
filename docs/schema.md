# Evidence ledger schema 1.0

The ledger is UTF-8 JSON. Duplicate object keys and nonstandard `NaN` or `Infinity`
values are rejected. Unknown fields are errors so a misspelt field is not silently
ignored. Dates use `YYYY-MM-DD` and must be actual calendar dates.

## Root object

| Field | Type | Requirement |
| --- | --- | --- |
| `schema_version` | string | Required; exactly `1.0` |
| `title` | string | Required; non-empty |
| `description` | string | Optional |
| `sources` | array of source objects | Required; an empty array produces a warning |
| `claims` | array of claim objects | Required; an empty array produces a warning |

All source and claim identifiers share a single namespace. An identifier begins
with an ASCII letter, contains only ASCII letters, digits, `.`, `_` or `-`, and
has at most 80 characters. Use stable identifiers rather than renumbering entries
whenever their display order changes.

## Source object

| Field | Type | Requirement |
| --- | --- | --- |
| `id` | string | Required; unique across sources and claims |
| `title` | string | Required; non-empty |
| `url` | string | Required; absolute HTTP(S) URL, with no embedded credentials or whitespace |
| `source_type` | string | Required; `legislation`, `case`, `regulation`, `guidance`, `article`, `book`, `dataset` or `other` |
| `jurisdiction` | string | Required; use a meaningful scope such as `Singapore` or `Not jurisdiction-specific` |
| `version` | string | Optional, non-empty when present |
| `as_of` | date string | Optional; identifies the date of the material consulted |
| `accessed` | date string | Optional; records when the source was accessed |
| `notes` | string | Optional |

Omitting both `version` and `as_of` produces a warning. `as_of` does not certify
that a legal text was then in force, or that it is the latest version. Record
such conclusions separately with their evidence. A source not linked to a claim
also produces a warning. URLs are parsed but never visited.

## Claim object

| Field | Type | Requirement |
| --- | --- | --- |
| `id` | string | Required; unique across sources and claims |
| `text` | string | Required; a non-empty proposition |
| `review_status` | string | Required; `unreviewed`, `checked` or `contested` |
| `evidence` | array of evidence-link objects | Required |
| `review` | review object | Required for `checked`; optional otherwise |
| `notes` | string | Optional |

`checked` means that the entry's author declares a human review. It is not a
software verification outcome. The program cannot establish who performed a
review or whether it was competent or complete.

`unreviewed` and `contested` each produce a warning. An empty evidence array
produces a warning, or an error if the claim is marked `checked`. A checked claim
with only context or contradictory links produces a warning for the absence of
supporting or qualifying evidence.

## Evidence-link object

| Field | Type | Requirement |
| --- | --- | --- |
| `source_id` | string | Required; must match a source in the ledger |
| `pinpoint` | string | Required; an empty value warns, or errors for `checked` claims |
| `relation` | string | Required; `supports`, `qualifies`, `contradicts` or `context` |

The relation is the researcher's assessment of the source's relationship to the
proposition. The code does not infer it. Repeating an identical source, pinpoint
and relation within one proposition produces a warning.

## Review object

| Field | Type | Requirement |
| --- | --- | --- |
| `reviewer` | string | Required when a review object is supplied; non-empty |
| `date` | date string | Required when a review object is supplied |
| `note` | string | Optional, non-empty when present |
| `resolution` | string | Optional, non-empty when present |

For a checked claim that includes contradictory evidence, absence of a
`resolution` produces a warning. A resolution is a recorded explanation, not a
machine-approved answer to the conflict. A contested status keeps the conflict
visible regardless of whether a review object exists.

## Minimal structurally complete example

```json
{
  "schema_version": "1.0",
  "title": "A new evidence register",
  "sources": [],
  "claims": []
}
```

This blank register has no structural errors and has two warnings. It contains
no reviewed evidence. The `init` command creates this structure with an optional
description field.

