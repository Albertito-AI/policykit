# Optional PDF parser security update | 22 November 2026

The optional `pdf` extra now requires `pypdf>=7.1.1,<8`. Its previous
`pypdf>=5,<7` range excluded the supported fixes for published parser defects.
The ledger and text workflow retain their standard-library runtime.

## Evidence and scope

The upstream maintainer's
[cross-reference stream advisory](https://github.com/py-pdf/pypdf/security/advisories/GHSA-59jv-x5x2-gg4c)
affects versions below 7.0.0. The
[image memory-allocation follow-up](https://github.com/py-pdf/pypdf/security/advisories/GHSA-fhff-j4m8-439h)
affects versions below 7.0.1. The [7.1.1 release](https://pypi.org/project/pypdf/7.1.1/)
also incorporates later upstream parsing limits and supports Python 3.10+.

`regnav_esg/ingest.py` uses `PdfReader` and `page.extract_text()` on supplied
PDFs. This is relevant parser exposure. Its existing separate worker,
address-space/CPU limits and wall timeout reduce the effect of resource
exhaustion. No exploit or compromise was demonstrated, and the image-specific
advisory is not claimed to be reachable through text extraction alone.

## Verification actually performed

On Linux, CPython 3.12.14, a fresh virtual environment contained the official
`pypdf` 7.1.1 wheel. Its SHA-256 matched the PyPI release metadata:
`04c5680d4b4cfa04ab505b09393fc949860c34a4dad6565284d11a2f5c3ce8b1`.
The project was exercised from source without executing a project installation.

- The existing unittest suite ran 246 tests: 241 passed and five were skipped.
  The skips concern optional table, OCR and XLSX dependencies absent from that
  environment. The pypdf text-extraction tests ran successfully.
- The documented fictional PDF workflow produced two documents, five physical
  pages and 33 unreviewed ledger claims. Both parser receipts report 7.1.1.
- The resulting ledger passed structural validation with the expected review
  warnings. No remote model or source service was called by these checks.

This verifies compatibility of the exercised paths, not a general malware or
hostile-document certificate. Existing environments must explicitly upgrade
their installed parser; changing a source manifest does not update them.
Next, use a resolved, hash-verified environment for any deployment, inspect
current upstream advisories and retain the existing parser isolation and
independent evaluation gates.
