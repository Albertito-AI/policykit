# Your first ten minutes with RegNav

Follow one fictional proposition from its source to an evidence matrix, then
export a CSV you can inspect in a spreadsheet. You will see what the prototype
checks and what still requires a person's judgment.

**Choose your route:** use the CLI route below if Python 3.10 or newer is already
available. Otherwise, go directly to the [paper route](#no-python-paper-route).
The timings are suggested, not measured completion times. Installing Python is
outside this ten-minute walkthrough.

All example sources, propositions, dates and reviewers are fictional. The
`example.org` addresses are placeholders, not sources to visit. RegNav works
offline using the Python standard library; no package installation, account,
API key or model access is required after obtaining the repository. See the
[rights statement](../RIGHTS.md) before reuse. This guide adds no licence.

## Minutes 0 to 2: open the example

If you do not have the repository locally, use **Code > Download ZIP** on its
[GitHub page](https://github.com/Albertito-AI/policykit), then extract it. Open a
terminal in the extracted repository folder. It should contain `README.md`,
`regnav_evidence/` and `examples/`. Run all commands below from that folder.

Check your interpreter:

```bash
python --version
```

The version must be 3.10 or newer. If your installation uses `python3` or
`py -3`, use that in place of `python` throughout.

Open the [complete fictional sources](../examples/training_sources.md). Read
A.2, A.3 and B.2. Then inspect [the example ledger](../examples/synthetic_ledger.json).
It records three propositions against two sources. You do not need to edit it.

## Minutes 2 to 4: run the structural check

```bash
python -m regnav_evidence validate examples/synthetic_ledger.json
```

The command begins with a notice explaining that these are structural checks.
It reports the following three warnings and ends with exactly:

```text
Structural checks: 0 error(s), 3 warning(s).
```

| Expected warning | What to inspect in this fixture |
| --- | --- |
| `UNREVIEWED_CLAIM` | `CLAIM-remedy` has no completed human-review declaration. |
| `MISSING_PINPOINT` | That claim's link to `SRC-draft-b` has an empty pinpoint. |
| `CONTESTED_CLAIM` | `CLAIM-timing` retains a disagreement between the two drafts. |

Now run the same check in strict mode:

```bash
python -m regnav_evidence validate examples/synthetic_ledger.json --strict
```

The displayed findings are the same. The exit status changes from **0 to 2**
because warnings remain. This is the intended result; keep the distributed
fixture unchanged.

| Exit status | Meaning for `validate` |
| --- | --- |
| `0` | No structural errors. Ordinary validation can still report warnings. |
| `1` | The input cannot be read or parsed, or structural errors were found. |
| `2` | In strict mode, warnings remain and there are no structural errors. An invalid command or option can also produce `2`; read the message. |

A successful exit does not establish that a proposition is supported, that
current law has been identified, or that a real person completed a review.

## Minutes 4 to 7: inspect and export the matrix

Display the Markdown report:

```bash
python -m regnav_evidence report examples/synthetic_ledger.json --format markdown
```

The [generated sample report](sample_report.md) shows the same report in a
readable page. There are **three propositions and four evidence rows**:
`CLAIM-timing` has two links, one to A.3 and one to B.2.

Create a CSV using a filename that does not already exist:

```bash
python -m regnav_evidence report examples/synthetic_ledger.json --format csv --output quickstart-evidence.csv
```

Expected result: `Wrote quickstart-evidence.csv.` and exit status `0`. A notice
about the three warnings is expected too. The file appears in the current
folder and contains a header plus four evidence rows. Open it in a spreadsheet;
choose UTF-8 and a comma delimiter if prompted.

The report command writes notices to standard error and the report to standard
output, or to the file specified by `--output`. A warning notice alone does not
mean export failed. The JSON remains the complete record; report views omit
some optional notes and access information. CSV export also prefixes text that
could be interpreted as a spreadsheet formula, so it is not a lossless copy of
every JSON field.

## Minutes 7 to 10: answer three concrete questions

Inspect the report alongside the source packet. Write one sentence for each:

1. **Logging:** which paragraph supports `CLAIM-logging`, and what does it say
   happens before review?
2. **Timing:** what differs between A.3 and B.2? Does anything in the supplied
   packet establish which draft governs?
3. **Further review:** can you find a passage supporting `CLAIM-remedy`? Would
   filling its blank pinpoint with an unrelated paragraph supply support?

You have finished this route when you have the exported CSV and three short
answers identifying a supported sequence, an unresolved difference and a gap
in the evidence. These are your observations, not evaluation results collected
by the project. The exercise supplies no rule selecting a governing draft and
no passage establishing further review.

The fixture's `checked` label is a declaration by a **fictional reviewer**.
Do not copy that identity into a real record. Only a person who actually performs
a review should record their own declaration and its limits. RegNav does not
read sources, compare quotations or decide whether a recorded relation is right.

## After editing a ledger: compare saved snapshots

Keep the earlier valid JSON ledger as a separate file, for example
`ledger-before.json`. After editing its working copy, compare them:

```bash
python -m regnav_evidence compare ledger-before.json my-ledger.json
python -m regnav_evidence compare ledger-before.json my-ledger.json --json
```

Both files must pass the structural validator. The comparison reports added,
removed and modified sources and propositions, changes to evidence links and
review declarations, and which **previously checked or contested** propositions
may need renewed human attention. It does not change either input file.
The exit code is 0 when the comparison succeeds, including when differences
exist, and 1 if either snapshot cannot be read or is structurally invalid.

A change to a source's version, URL, title, jurisdiction, source type, legal
reference date or interpretive notes is conservatively treated as material.
A change only to its `accessed` date is metadata-only. Editing proposition
text, links or notes is material; changing only the reviewer declaration is
reported separately. Reordering sources, propositions or evidence links is not
a substantive change. If an identifier changes, RegNav shows one removal and
one addition. It does not guess that they denote the same record.

A **RECONSIDER PRIOR REVIEW** marker is a prompt for a person to inspect the
changed materials and decide what the previous declaration still supports.
It neither removes that declaration nor performs a fresh review. A new
`checked` value remains only the person's own declaration. This comparison
checks records and never fetches the underlying legal sources.

## No-Python paper route

You can do the same source-reading task without installing or running anything.
Open the links in a browser, or print the pages beforehand.

| Suggested time | Action | Output |
| --- | --- | --- |
| Minutes 0 to 2 | Read the five paragraphs in the [source packet](../examples/training_sources.md). | Identify the two fictional drafts. |
| Minutes 2 to 5 | Read the evidence matrix and three notices in the [sample report](sample_report.md). | Locate the logging, timing and further-review entries. |
| Minutes 5 to 9 | Answer the three questions above on paper. Record the source label and pinpoint beside each answer. | Three reasoned notes, including unresolved points. |
| Minutes 9 to 10 | Explain why four evidence rows represent three propositions, and why `checked` is not legal verification. | A short account of the report's limits. |

This route lets you inspect a generated report; it does not claim that you ran
the validator or exported a file. The [learner handout](../teaching/learner_handout.md)
contains the sources, a fuller table and a paragraph-revision exercise for a
longer session. The materials are an unevaluated teaching prototype.

## If a command does not work

| What you see | What to do |
| --- | --- |
| `python` is not found, or the version is older than 3.10 | Check an installed `python3` or `py -3` interpreter with `--version`, and substitute it consistently. Use the paper route if no suitable interpreter is available. |
| `No module named regnav_evidence` | Open the terminal in the repository folder containing `regnav_evidence/` and `examples/`. Run the documented `python -m regnav_evidence ...` command there. |
| `error: Cannot read ledger` followed by a file or path error | Confirm that the ZIP was extracted and `examples/synthetic_ledger.json` exists relative to your terminal's current folder. |
| `error: cannot write report` and `File exists` | Use an unused name such as `quickstart-evidence-2.csv`. The command intentionally refuses to replace an existing file without `--force`; no force option is needed for this route. |
| Strict validation exits `2` with the three listed warnings | This is the expected fixture result. Inspect the notices rather than changing review statuses merely to make them disappear. |
| `unrecognized arguments: --strict` after a `report` command | `--strict` belongs to `validate`. Run the strict validation command above separately, then the report command. |
| The matrix has an empty pinpoint and a repeated claim ID | The blank belongs to `CLAIM-remedy`. The repeated `CLAIM-timing` has two evidence links. Both are deliberate features of this fixture. |

If your output differs, retain the command, Python version and exact error
message. Check that you are using the unchanged bundled fixture. A report of a
reproducible problem should use this fictional material, not private research,
student records or client information.

## Next step

For your own bounded research question, read the [review method](review_method.md)
and [schema](schema.md) before creating entries. Keep the source version and
pinpoint, distinguish support from context, and leave review declarations
accurate. Independent usefulness and educational benefit remain to be evaluated.
