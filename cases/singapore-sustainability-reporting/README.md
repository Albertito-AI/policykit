# Singapore sustainability reporting: a narrow evidence case

**AI-prepared example. Both propositions remain `unreviewed`. Independent human
review is outstanding.** No reviewer, maintainer endorsement or issuer-specific
compliance finding is asserted.

## Question and scope

How do the current SGX Mainboard provisions distinguish the timing of an annual
sustainability report, internal review of the reporting process and additional
external assurance?

The [ledger](ledger.json) contains two modest textual propositions, identified as
`sgx-mb-report-timing` and `sgx-mb-internal-review`. It uses real primary sources;
there is no fictional issuer, alleged breach or adjudicated dispute. The example
is limited to the versions SGX displayed as applicable from 1 January 2026,
consulted on **23 October 2026**. Applicability to a particular issuer, reporting
period, waiver or listing history has not been determined.

Climate-disclosure phasing, IFRS/ISSB requirements, Catalist rules, statutory
causes of action, liability, sanctions and remedies are outside this case.

## Primary-source register

All four materials below were opened on the issuing institution's rulebook site
during the AI preparation pass. The ledger retains their URLs, access date,
version observations and exact provision or page references.

| Ledger source | Official source and pinpoint | What was checked |
| --- | --- | --- |
| `sgx-mb-711a` | [Mainboard Rule 711A](https://rulebook.sgx.com/rulebook/711a), sole paragraph: ordinary timing clause and external-assurance alternative | The individual rule page displays a current version beginning 1 January 2026. |
| `sgx-mb-711b` | [Mainboard Rule 711B](https://rulebook.sgx.com/rulebook/711b), paragraph (3), first and second sentences | The same version label is displayed; the two sentences address different review mechanisms. |
| `sgx-mb-pn76` | [Practice Note 7.6](https://rulebook.sgx.com/rulebook/practice-note-76-sustainability-reporting-guide), paragraphs 6.1, 6.2 and 5.3 | The current version begins 1 January 2026. Relevant guidance qualifies timing and review scope. |
| `sgx-mb-amend-2026` | [2026 amendment document](https://rulebook.sgx.com/sites/default/files/net_file_store/Mainboard_Rules_-_Sustainability_Reporting_Enhancing_Consistency_and_Comparability_%282026%29.pdf), PDF page 1: effective-date heading and Rule 711A/711B blocks | The document linked from both rule pages expressly identifies amendments effective on 1 January 2026. |

### What source verification establishes

The direct rule pages, their version labels, the linked amendment document's
effective-date heading and the relevant guidance were read, rather than relying
on search snippets or secondary commentary. The clean current HTML supplies the
operative wording used in the ledger. The amendment PDF is a redline: extracted
deleted and inserted text must not be combined into a purported current rule.

This is a documented AI source-inspection pass, not independent human legal
verification. The effective date comes from SGX's labels and amendment heading;
it is distinct from the access date. A separate publication date has not been
established. The live URLs may change, and this case does not preserve a licensed
full-text snapshot or certify later changes. Its `as_of` metadata does not itself
prove that a provision applies to a particular report.

## Evidence relationships and limits

- **Timing:** Rule 711A supports the ordinary report-timing proposition and
  qualifies it with an assurance alternative. Practice Note 7.6 paragraph 6.1
  describes that alternative as transitional. Paragraph 6.2 adds a summary
  requirement if the sustainability report follows the annual report. These
  qualifications are retained, rather than presenting an unconditional deadline.
- **Review:** Rule 711B(3)'s first sentence supports the internal-review
  proposition. Its second sentence distinguishes additional independent external
  assurance. Practice Note 7.6 paragraph 5.3 qualifies how already assured aspects
  may be treated within a risk-based internal review. This does not determine
  duties arising from other instruments.
- **Version:** The amendment document is linked as `context` for the stated
  version, not as a separate legal conclusion about a particular issuer.

No contrary authority is recorded in this bounded pass. That does not establish
that none exists. An independent human reviewer should read each provision in
context, confirm the relevant version and reporting period, check any applicable
waiver or newly listed issuer treatment, and assess each relationship before
entering a review declaration. No completed human review has been recorded.

## Reproduce the structural checks

From the repository root:

```sh
python -m regnav_evidence validate cases/singapore-sustainability-reporting/ledger.json
python -m regnav_evidence report cases/singapore-sustainability-reporting/ledger.json --format markdown
```

These commands run offline and do not fetch or verify source URLs. The expected
review-gap warnings are deliberate: `unreviewed` must remain visible until a
human review actually occurs. The report is emitted to standard output; the
JSON remains the complete record, including source notes and access dates.

Local verification on 23 October 2026, using Python 3.12.14:

| Command | Actual result |
| --- | --- |
| `validate` (one run) | Exit 0; 0 errors; 2 `UNREVIEWED_CLAIM` warnings, one for each proposition |
| `report --format markdown` (one run) | Exit 0; matrix produced for 4 sources and 2 unreviewed propositions; both review warnings retained |

These results establish structural compatibility and report generation only.
They do not turn either proposition into a checked claim or verify its sources.

## Rights and attribution

The sources are issued by Singapore Exchange and remain subject to their own
terms. This example uses brief paraphrases and reproducible references; it does
not reproduce the rulebook. The existing [rights statement](../../RIGHTS.md)
continues to apply. No general reuse licence is added.
