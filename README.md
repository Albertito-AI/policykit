# RegNav Evidence Ledger

RegNav means Regulatory Navigator. This repository develops research tools for
examining the evidence behind legal propositions, beginning with the questions
raised by sustainability reporting and legal accountability in Asia.

Maintainer: **Albert Tan** · [Website](https://www.alberttansinhon.com/)
· [Research profile](https://research.rug.nl/en/persons/tan-sin-hon-albert-tan/)
· [ORCID](https://orcid.org/0009-0001-8996-7933)

**Status:** version 0.1 research prototype. See the
[roadmap](docs/ROADMAP.md), [progress record](docs/PROGRESS.md) and
[research standard](docs/RESEARCH_STANDARD.md). The
[project status](docs/project_status.md) records available materials and the
external evidence still needed.

An offline register connecting scholarly propositions to their sources, pinpoint
locations and recorded human review. It gives a legal researcher or editor a
repeatable way to see which propositions still need attention.

This is a working Python prototype. It checks the structure of the record and
exports an evidence matrix. A `checked` entry records a person's declaration that
they reviewed it. The software does not retrieve sources, compare quotations,
decide whether a source supports a proposition, determine current law, or certify
factual accuracy.

## Try it

Start with the [ten-minute guide](docs/quickstart.md) for step-by-step commands,
expected output and troubleshooting. It includes a paper route for readers
without Python and a [generated sample report](docs/sample_report.md).

Use Python 3.10 or newer. There are no third-party packages, API keys or network
calls. Run these commands from this directory:

```bash
python -m regnav_evidence validate examples/synthetic_ledger.json
python -m regnav_evidence report examples/synthetic_ledger.json --format markdown
python -m regnav_evidence report examples/synthetic_ledger.json --format csv --output evidence.csv
python -m regnav_evidence init my-ledger.json --title "My research evidence register"
```

The example intentionally contains one unreviewed proposition, one missing
pinpoint and one contested proposition. Its **three warnings are expected**.
All of its source texts and reviewer details are fictional training material;
the complete mock texts are in [training_sources.md](examples/training_sources.md).

For a machine-readable validation result:

```bash
python -m regnav_evidence validate my-ledger.json --json
python -m regnav_evidence validate my-ledger.json --strict
```

`validate` exits `0` when the structure has no errors, `1` for invalid input or
structural errors, and `2` when `--strict` is used and warnings remain. Normal
command-line usage errors also use exit `2`. Warnings may represent a legitimate
unresolved disagreement. A strict failure therefore identifies work for a human
reviewer; it is not a judgment that the research is wrong.

## Compare two saved versions

After saving an earlier snapshot of a ledger, use the new read-only comparison
command to identify changes that may make recorded reviews stale:

```bash
python -m regnav_evidence compare ledger-before.json ledger-after.json
python -m regnav_evidence compare ledger-before.json ledger-after.json --json
```

Both snapshots must be structurally valid. The tool distinguishes source-version,
proposition and evidence-link changes from access-date and review-declaration
edits. It flags previously reviewed propositions for **human reconsideration**
when their substantive record changes. It does not edit either ledger, check the
legal source, invalidate a declaration or certify renewed review. A successful
comparison exits `0`, even when substantive differences are reported; invalid
snapshots exit `1`. See the [comparison instructions](docs/quickstart.md#after-editing-a-ledger-compare-saved-snapshots).

## Source-file changes: a separate experiment

Does a changed source leave a statement in your report needing another look?
[Source Watch](experiments/source_watch/README.md) compares explicitly listed
local files with a saved baseline and identifies their linked claim IDs.
[Inspect the generated fictional example](experiments/source_watch/sample_report.json)
without installing anything or providing contact details. The
[evaluation guide](experiments/source_watch/README.md#consider-an-evaluation)
explains fit, limits and how to discuss a bounded pilot. This is an experiment,
not a production service or a determination that a legal claim is wrong.

## Record a proposition

1. Enter the exact source version or the date of the material consulted. Supply
   its title, URL, source type and jurisdiction.
2. State a proposition narrowly enough for its evidence to be examined.
3. Link the relevant sources and record a page, paragraph, provision or other
   reproducible pinpoint. Classify each link as `supports`, `qualifies`,
   `contradicts` or `context`.
4. Leave the proposition `unreviewed` until a person has examined the evidence.
   A `checked` declaration requires a reviewer, date, evidence link and pinpoint.
   Preserve significant disagreement using `contested`, or record how contrary
   evidence was addressed in `review.resolution`.
5. Run the validator and inspect the matrix. Correct the record and repeat the
   substantive review when a source or proposition changes.

See [the schema](docs/schema.md) for the complete field specification and
[the review method](docs/review_method.md) for a practical editorial workflow.

## Source-grounded worked case

The [Singapore sustainability reporting case](cases/singapore-sustainability-reporting/README.md)
records two narrow propositions about report timing and internal review under
SGX Mainboard rules, with four official source records and exact pinpoints.
It retains the provisions' qualifications and identifies the versions inspected
on 23 October 2026. Both propositions remain **unreviewed**. This AI-prepared
example does not assess an issuer, liability or remedies; independent human
review is outstanding. See the [case collection](cases/README.md) for scope.

## Teaching and evaluation

The [55-minute teaching exercise](teaching/README.md) uses the complete
fictional source packet to practise tracing a proposition to evidence,
identifying qualifications and disagreement, and explaining the limits of a
software report. It includes a learner handout, facilitator answer key,
descriptive assessment rubric and blank feedback form. A paper or spreadsheet
route requires no Python installation.

The [external usability protocol](docs/evaluation_protocol.md) defines five
tasks for an initial three-volunteer pilot. The materials are original,
AI-assisted and unevaluated. No participants have been tested or educational
benefits demonstrated in this release. See [RIGHTS.md](RIGHTS.md) before reuse.

## Outputs and file handling

Markdown reports contain an evidence matrix, a source register, human-review
declarations and outstanding warnings. The CSV is a flat matrix with one row per
evidence link. Claims without links retain a row. The JSON remains the complete,
lossless record; report views do not include every optional note or access date.

HTML and Markdown supplied as field text are escaped in Markdown reports. CSV
fields that could start a spreadsheet formula are prefixed with an apostrophe,
including formulas after whitespace or invisible control characters. This
deliberately changes those exported cell values. Keep the JSON for round trips.

`init` never overwrites an existing file. `report --output` also refuses an
existing file unless `--force` is supplied. Even with `--force`, it refuses to
overwrite the input ledger, including an existing hard link to that file.

## Development checks

Read [CONTRIBUTING.md](CONTRIBUTING.md) for bug reports, source-grounded case
proposals, documentation feedback and pull requests. The
[workstream guide](docs/WORKSTREAMS.md) coordinates maintenance, and the
[release criteria](docs/release_readiness.md) define the evidence needed for
a candidate decision.

```bash
python -m unittest discover -s tests -v
```

The suite exercises malformed input, duplicate identifiers and JSON keys,
invalid references, date and URL checks, review metadata, contradictory evidence,
CSV formula handling, Markdown escaping, command exit codes and file protection.

## Scope of this prototype

The core ledger supports one JSON schema and local command-line use. It has
no browser interface, authenticated multiuser workflow, automatic source
retrieval, source-change detection or persistent review history. It does not
validate a court citation format or generate an OSCOLA bibliography. A URL that
passes the structural check may still be unavailable, irrelevant or incorrect.

The design is intended for careful human review of research records. Independent
field testing and evaluation of its effect on review quality remain to be done.

## Intellectual context

The project grows from questions about the relationship between a statement,
its evidential basis and its legal consequences. Related scholarship includes
[sustainability reporting in Singapore and Thailand](https://research.rug.nl/en/publications/converging-standards-divergent-accountability-sustainability-repo/)
and [sustainability disclosure in China](https://research.rug.nl/en/publications/when-does-a-sustainability-report-count-as-securities-disclosure-/).
These papers provide context for the research direction. This prototype has
not been evaluated in those papers, and neither publication establishes its
effectiveness.

## Citation and rights

Use [CITATION.cff](CITATION.cff) to identify the software and cite the version
actually used. No DOI has yet been assigned. See [RIGHTS.md](RIGHTS.md) before
reuse; this public prototype is not currently supplied under an open-source
licence. Existing linked material retains its own rights status.

## Earlier starter packages

The original README linked these materials:

- [policykit-starter-v5.tar.gz](https://github.com/user-attachments/files/22344766/policykit-starter-v5.tar.gz)
- [policykit-extras-v1.zip](https://github.com/user-attachments/files/22344754/policykit-extras-v1.zip)

These links are retained for continuity. The archives are separate legacy
material, have not been reviewed as part of this prototype, and are not
dependencies of the evidence ledger.

