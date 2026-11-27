# Targets and stakeholder disclosure in Singapore and Thailand

**Historical comparison for the financial year ending 31 December 2023.** Four propositions compare the wording of three primary sources. They were prepared with AI assistance and await independent human review.

**Teaching this case?** Give participants the [blank comparison worksheet](worksheet.md) before showing them the worked comparison below.

If a sustainability report omits targets, what would each instrument ask the reader to look for? The Singapore rule directs attention to the issuer's explanation of an exclusion. The Thai form asks about organisational objectives if the company has any. A missing number alone cannot answer either question. [SGX Mainboard Rule 711B(1)(c) and (2)](https://rulebook.sgx.com/node/6528/revisions/26623/view) · [Thai Form 56-1 One Report, section 3.1, p. 11](https://publish.sec.or.th/nrs/9731s.pdf#page=11)

[Open the evidence ledger](ledger.json) · [Download the evidence rows as CSV](evidence.csv)

[Compare these observations with the 2025 reporting year](https://github.com/Albertito-AI/sg-th-disclosure-data). The two-year dataset tracks the target provisions and the change in numbering of the Singapore stakeholder guidance.

## Compare the provisions

| Question | Singapore, SGX Mainboard | Thailand, ordinary Form 56-1 One Report |
| --- | --- | --- |
| Which targets appear in the report? | Rule 711B(1)(c) lists targets as a primary component. Under (2), an issuer excluding it must explain the omission, its alternative and its reasons. Practice Note 7.6, para 4.1(d), recommends targets for each identified material ESG factor for the forthcoming year. | Section 3.1 asks the company to disclose organisational sustainability objectives, **if any**, aligned with its short-term or long-term business strategy, or both. |
| What should the report say about stakeholders? | Practice Note 7.6, para 3.6, recommends reporting **material outcomes of engagement**. | Section 3.2.2 directs the company to identify key internal and external stakeholder groups connected to its value chain and summarise their expectations. It then recommends describing how the company responds. |

## How to repeat the comparison

1. Open the three instruments below. Before opening the ledger, write down the document type, actor, object of disclosure, operative wording and any qualification for each jurisdiction and question.
2. Record the page or paragraph that supports each observation. Give separate entries to the exchange rule and the guide when both address a question. In the Thai text, look for the conditional phrase **ถ้ามี** in section 3.1 and the change from **ให้** to **ควร** in section 3.2.2.
3. Compare your entries with the four claim IDs in the ledger. If you would code a clause differently, record the claim ID, your reading, the conflicting wording and the pinpoint. A second person's account can then be compared with the first.

The coding unit is the instruction in its document. A **directive** instructs the issuer to make a disclosure. A **recommendation** uses an expression such as *should*. A **qualification** narrows the scope of an instruction or specifies how an omission must be handled. A single provision can contain all three elements. These labels describe the language of the passage. A finding on breach, sanction or remedy would require additional authority and issuer-specific facts.

| Instrument | Version and pinpoint |
| --- | --- |
| [SGX Mainboard Rule 711B](https://rulebook.sgx.com/node/6528/revisions/26623/view) | Archived version for 1 January 2022 to 31 December 2024, paras (1)(c) and (2). The second sentence of (2) addresses the separate climate component for specified industries. |
| [SGX Mainboard Practice Note 7.6](https://rulebook.sgx.com/node/6532/revisions/26630/view) | Same archived period. Paragraph 1.1 explains the guide's role. Read paras 3.6 and 4.1(d) for engagement and targets. |
| [Thai Form 56-1 One Report](https://publish.sec.or.th/nrs/9731s.pdf#page=11) | Official Thai form attached to Notification Tor Jor. 7/2566. The cover is dated 25 April 2023 and identifies financial years ending 31 December 2023 onwards. Sections 3.1 and 3.2.2 are on printed p. 11. The English wording here is a working translation. |

All source links were checked on 27 November 2026. The chosen SGX archive and Thai form preserve the wording examined for the 2023 comparison. Later revisions and issuer filings fall outside this exercise.

## Reproduce or cite an observation

Run these commands from the repository root. Each CSV row links one claim to one source passage, so a claim can span several rows. The JSON preserves the full record, including qualifications, source versions and notes.

```bash
python -m regnav_evidence validate cases/singapore-thailand-disclosure-2023/ledger.json
python -m regnav_evidence report cases/singapore-thailand-disclosure-2023/ledger.json --format csv
```

For a legal proposition, cite the instrument, version and pinpoint in the source table. To credit this comparison, cite *RegNav, Targets and stakeholder disclosure in Singapore and Thailand*, the claim ID and a permanent link to the revision you used. Open the ledger on GitHub and press **y** to obtain its commit-specific URL. Reuse terms are set out in the [repository rights statement](../../RIGHTS.md).

Albert Tan's article examines how reporting obligations lead to different questions about supervision, liability and remedies. Read it alongside this exercise for the broader comparative argument. [*Converging Standards, Divergent Accountability*, University of Groningen research portal](https://research.rug.nl/en/publications/converging-standards-divergent-accountability-sustainability-repo/)
