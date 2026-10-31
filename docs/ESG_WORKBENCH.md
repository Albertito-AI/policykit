# ESG workbench

The workbench extends RegNav from a supplied-record ledger to a runnable local
document and sustainability-data workflow. Its outputs remain candidates for
review. The original `regnav_evidence` schema and behaviour are unchanged.

## Capability status

| Function | Implemented behaviour | Practical boundary |
| --- | --- | --- |
| PDF ingestion | Actual page text extraction, source-byte SHA-256, parser version, text hashes and physical page numbers | Optional pypdf or pdftotext; difficult layouts can lose reading order |
| Scanned PDFs | Explicit local English OCR through pdftoppm and Tesseract | At most 20 empty pages; recognition needs inspection; mixed text/image pages can remain incomplete |
| Tables | Optional pdfplumber candidate cells, row/column positions and page bounding boxes | Tables are heuristic detections, not verified semantic metric records |
| Markdown | Page-labelled source text and candidate tables | Preserves extracted text; does not reproduce visual PDF layout |
| Extraction | Configurable keywords and regex patterns, captured literal fields and page-cited source passages | Ten illustrative default fields; neither exhaustive nor independently accuracy-tested |
| Summary | Ranked verbatim ESG-related passages with source locations | Extractive selection, not comprehensive analysis |
| Retrieval | Local BM25 page ranking and exact excerpts | Lexical retrieval; no claim of semantic completeness |
| Model-assisted extraction | Opt-in Responses API adapter, selected-page retrieval, strict JSON contract, exact quotations and literal field-presence checks | Needs credentials, model selection and explicit network opt-in; live provider/accuracy evaluation outstanding |
| Activity collection | Strict CSV/TSV and optional XLSX import with explicit column mapping | Decimal/date conventions are explicit; no hosted multiuser entry system |
| Emissions | Decimal arithmetic at 50-digit precision, supplied versioned factors, compatible unit conversions and entity/facility rollups | Factor selection, completeness, appropriateness and inventory boundary remain operator responsibilities |
| Materiality | Separate financial and impact screening under supplied rubrics, scores, reasons and evidence | No universal threshold, automatic legal applicability or professional materiality conclusion |
| Standards references | Exact framework/version/code lookup in supplied source records | Registry is not an authorised standards corpus; references are not independently verified |
| Action planning | Supplied gaps and templates become proposed actions with owners, deadlines, criteria and optional budget ranges | Missing facts remain missing; no invented budgets, success or execution |
| Evidence handover | Original-schema ledger export with candidate context links and unreviewed status | Requires original source URLs; no invented source URLs or human review |
| Review view | Offline HTML with candidate filters and source-page links; JSON, CSV and Markdown exports | Read-only view; no authenticated collaboration, hosted service or production assurance |

These capabilities do not establish parity with any commercial platform's
accuracy, coverage, deployment, security, integrations or professional services.

## Installation

Python 3.10 or newer is required. From a permitted checkout:

```bash
python -m pip install '.[pdf,tables,excel]'
```

The extras are optional: `pdf` supplies pypdf, `tables` supplies pdfplumber and
`excel` supplies openpyxl. Text/Markdown and the original ledger have no external
Python runtime dependencies. `pdftotext` is an alternative system PDF parser.
OCR requires separately installed `pdftoppm` and `tesseract` with English data.
No installation command changes the project's rights or grants a reuse licence.

## Reproduce the fictional document demonstration

Run from the repository root, using directories that do not already exist:

```bash
python examples/esg/make_demo.py demo-input
python -m regnav_esg run demo-input/fictional_2024.pdf demo-input/fictional_2025.pdf --output demo-output --source-url https://example.org/fictional-2024 --source-url https://example.org/fictional-2025 --jurisdiction FICTIONAL
python -m regnav_evidence validate demo-output/ledger.json --json
```

Open `demo-output/report.html`. It contains original fictional data, clearly
identified as such. The example URLs are explicitly fictional and are never
fetched. Actual use requires the original source URLs. Omitting `--source-url`
produces the workspace without a core-ledger export.

Outputs:

- `documents.json`: exact extracted page texts, source hashes and parser records.
- `extractions.json`: field rules, candidate passages, captured values and locations.
- `source-N.md`: page-preserving Markdown, with candidate tables when requested.
- `candidates.csv`: spreadsheet-safe view; JSON retains the complete record.
- `assessments.json`: explicitly supplied arithmetic/screening/planning results.
- `report.html`: offline readable view with source navigation.
- `ledger.json`: original-schema unreviewed context records, when original URLs are supplied.

Every candidate citation is checked against the corresponding retained page text
and source identity before report or ledger export. Exact locations do not prove
that a passage supports a proposed inference or that the source is true. Physical
PDF page numbers are distinct from form-feed segments in text files; printed
page labels are not inferred.

## Individual document commands

```bash
python -m regnav_esg ingest report.pdf --output document.json
python -m regnav_esg ingest report.pdf --tables --output document-with-tables.json
python -m regnav_esg ingest scan.pdf --ocr --output ocr-document.json
python -m regnav_esg markdown document.json --output report.md
python -m regnav_esg extract document.json --output candidates.json
python -m regnav_esg search document.json 'Scope 1 emissions assurance'
python -m regnav_esg locate document.json 'Exact quotation' --page 12
```

`locate --normalise-whitespace` reports a separate normalised match and retains
the original quotation and character offsets. Multiple matches remain ambiguous.
The parser records fallback when `auto` uses pdftotext after a pypdf failure.
Scan-only and empty-text inputs produce explicit incomplete states, never a
successful empty extraction. `ingest` exits 2 for those incomplete states;
downstream extraction refuses them.

Default extraction is intentionally transparent. Custom `--config` JSON contains
`name`, `version` and `fields`; each field has a unique `id`, `label`, `category`,
`keywords` and/or `patterns`. Named regex groups become `captured_fields` only
when they occur within the cited match. Full surrounding sentence context is
retained where possible. Candidate limits and truncated passages are explicit.
Non-discovery under a rule does not establish absence from the source.

## Optional retrieval and model extraction

Set the API key in `REGNAV_MODEL_API_KEY` using the operator's normal secret
management, then explicitly choose a model:

```bash
python -m regnav_esg model-extract document.json --model YOUR_CONFIGURED_MODEL --query 'Scope 1 Scope 2 emissions assurance' --allow-network --output model-candidates.json
```

This sends selected page text to the configured HTTPS provider. Without
`--allow-network`, the adapter makes no request. The default endpoint is the
OpenAI Responses API; `--endpoint` accepts an explicitly chosen compatible HTTPS
endpoint. Redirects are rejected so credentials are not forwarded to a new host.
No provider tools are enabled. Documents are framed as untrusted data, not
instructions, and `store` is set to false in the request. Provider retention and
account policy remain governed by that provider; this flag is not a guarantee
about all forms of retention.

The adapter records model, prompt version/hash, selected pages, context hash and
source hash. It rejects absent, wrong-page and ambiguous quotations, and
non-null numeric/unit/period fields that are not literally present in the cited
passage. Presence is not semantic entailment: accepted items remain unreviewed
and `claim_support_verified` remains false. The adapter's mocked protocol and
rejection tests are not a live model evaluation. No API key is bundled.

Context is bounded rather than silently truncated. Large documents require a
focused query or explicitly divided work. Retrieved subsets are recorded and
must not be represented as whole-document coverage.

## Operational data and calculations

```bash
python -m regnav_esg import-activities examples/esg/activities.csv --output imported-activities.json
python -m regnav_esg inventory examples/esg/inventory.json --output inventory-result.json
python -m regnav_esg materiality examples/esg/materiality.json --output materiality-result.json
python -m regnav_esg plan examples/esg/plan.json --output action-plan.json
python -m regnav_esg standard examples/esg/standards.json 'Fictional Disclosure Framework' 'v1' 'METRIC-01'
```

The complete JSON examples define the input contracts. All factors, rubrics,
standards and budgets in those examples are fictional, not production defaults.
For tabular imports, a mapping is `{canonical_field: exact_column_header}`.
Dates use `YYYY-MM-DD`; decimal strings use a dot without thousands separators.
An explicit mapping permits deliberate exclusion of unrelated columns. Formula
cells and ambiguous spreadsheet decimals or dates are rejected. The formula-like
text check also rejects leading `=`, `+`, `-` or `@` concealed by whitespace
or Unicode format/control characters, including inside text-formatted XLSX
cells. It does not execute formulas, normalise source text or certify how
external spreadsheet programs will interpret every input. XLSX with multiple
sheets requires `--sheet`; TSV requires `--delimiter` with a literal tab.

Emissions calculations preserve the original activity and factor records,
version, validity interval, source URL and pinpoint. Scope 2 location-based and
market-based results remain separate. Biogenic CO2 remains outside scope CO2e
totals. The result includes activity counts per bucket: a zero subtotal with no
activity observations is not a measured zero. Empty inventories are rejected.
Missing source references for individual activity inputs are reported explicitly.
A factor citation does not authenticate the underlying meter reading.

Materiality thresholds and aggregation are caller-selected, with separate
financial and impact decisions. A weighted average is a configurable screening
choice, not a claim that GRI, IFRS or another framework mandates that formula.
Missing evidence, rationale or scores remains insufficient information.
Threshold decisions use exact rational arithmetic; a rounded display score
cannot move a topic across its threshold. Exact fractions and display-rounding
indicators are retained.

Action budgets are supplied estimates, aggregated by currency without exchange
rate assumptions. Missing owners, deadlines or criteria produce draft actions;
an overdue action is not proof of a legal breach or failed performance.

An optional `run --assessment assessment.json` accepts an object with
`inventory`, `materiality` and/or `action_plan` keys using those same contracts.
Results appear in the workspace without inventing analysis inputs from the PDF.

## Limits and evaluation

Current input limits include 25 MiB per document, 500 pages, five million
extracted characters and sixteen documents per workspace. PDF workers have
timeouts; POSIX workers additionally have memory/CPU/output limits. OCR is
limited to twenty empty pages. Default field extraction retains at most twenty
candidates per field; its lower-level API permits up to fifty. CSV import is
bounded to 100,000 rows. These limits are implementation choices, not tested
production capacity guarantees. Supplying the same source bytes twice, including
through different paths, is rejected before workspace creation: duplicate source
identities would give the HTML view ambiguous page-link targets. Submit each
source once; different versions must have distinct recorded source identities.

The remaining evaluation work is a permissioned held-out corpus with independently
checked page anchors, metrics, tables, OCR errors, missing disclosures, scopes
and interpretations. Measure field precision/recall, coverage, review time,
abstentions and disagreement separately. Regression tests and one real-PDF
execution do not establish these accuracy or business-performance results.

No authenticated multiuser database, hosted portal, customer integration,
emissions-factor subscription, complete standards corpus, full multilingual OCR,
professional service operation or independently validated legal rule collection
is included. Use the existing evidence-handover experiment for its separately
documented supplied-record contract; an actual external system still needs an
agreed adapter and interoperability test.

## Source and implementation references

- [pypdf extraction documentation](https://pypdf.readthedocs.io/en/stable/user/extract-text.html): extraction and OCR limitations.
- [pdfplumber](https://github.com/jsvine/pdfplumber): candidate table detection and coordinates.
- [OpenAI Responses API](https://developers.openai.com/api/reference/resources/responses/methods/create): optional provider contract.
- [Original RegNav schema](schema.md): evidence records and human-review declarations.
- [Rights and reuse](../RIGHTS.md): permission and third-party rights boundaries.
