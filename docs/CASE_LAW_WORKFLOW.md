# Landmark and key case repository: vision and workflow rationale

**Direction recorded: 29 October 2026.** This is the canonical guide for the
case-law collection's purpose, selection decisions and development priorities.
It records the maintainer's agreed direction, prepared with AI assistance.
Implementation and evidence of completed work belong in the
[roadmap](ROADMAP.md) and [progress record](PROGRESS.md).

**Our ambition is to build the world's most useful and trustworthy landmark
and key case repository.** We will pursue that ambition through traceable
sources, careful legal analysis, explicit coverage and demonstrated usefulness.
Any claim about comparative quality must be supported by an appropriate
evaluation. This document records an ambition and a working method.

## 1. The purpose of the collection

Help a researcher, teacher or practitioner answer a connected set of questions:
What happened? What did the court decide? Which legal proposition does the
decision support? Why does that proposition matter? What limits it? How has it
been treated? Under what facts, jurisdiction and time period might it apply?

The central design decision is to connect **judgments, individual propositions,
later treatment, applicable instruments and reasoned applications**. Each
connection needs an inspectable source or an explicit statement that it is an
editorial inference. Users should be able to move from a concise explanation
back to the relevant primary passage and see the unresolved questions.

Growth is useful when it closes an identified coverage gap, improves an
existing analysis, corrects a source or helps someone complete a research task.
A scheduled run can therefore produce a correction, a documented gap or no
change. Record counts alone do not establish research value.

## 2. A decision guide when we are uncertain

| Question | Working decision |
| --- | --- |
| Does this case answer a defined research question or change our understanding of an existing proposition? | Record the reason for inclusion. Keep an unexplained discovery as a candidate. |
| Can we inspect the primary passage and identify the decision, opinion and source version? | Preserve the exact pinpoint and context. If the passage is unavailable, disclose the gap and withhold an asserted holding. |
| Did the court decide this point, assume it, reserve it or discuss it incidentally? | Record that distinction before turning the passage into a proposition. |
| What qualifications, contrary authorities, legislation or procedural limits could change the analysis? | Include them with the supporting authority and identify the scope of the search. |
| Do we know which forum, period and material facts the proposed application concerns? | Record missing inputs as unknown and keep the conclusion conditional. |
| Has a person actually reviewed the proposition and its source basis? | Preserve the actual review state and scope. AI preparation and software checks cannot create a human review declaration. |
| Will this change make the resource more useful, accurate or easier to inspect? | Prefer the smallest change that resolves the observed need. Record the next unresolved question. |

When the evidence is insufficient, the useful result is a precise account of
what is missing and what would resolve it. A reliable collection must make
uncertainty usable.

## 3. The knowledge model we intend to build

The following are **design requirements for future structured records**. They
do not introduce new fields into the current ledger or assert that these
capabilities have been implemented. Core development owns schema and command
changes under the [workstream guide](WORKSTREAMS.md).

| Record | Information to preserve | Reason |
| --- | --- | --- |
| Judgment and opinion | Stable identifier, case name, neutral and report citations, court, jurisdiction, decision date, procedural stage, disposition, appeal history, separate majority/concurrence/dissent, original language, source URL and version | Keep related proceedings, parallel citations and distinct opinions identifiable. |
| Material facts and issues | Facts material to the reasoning, questions before the court, relief sought and procedural assumptions | Make the factual and procedural limits of a proposition visible. |
| Proposition or principle | A narrow statement, linked opinion and exact pinpoint, reasoning, conditions, exceptions, and whether it is decided, assumed, reserved, obiter, dissent, a party submission or editorial synthesis | Allow each proposition within a judgment to have its own meaning, qualifications and history. |
| Treatment relationship | Later decision or instrument, source and target proposition, direction and type of treatment, pinpoint, date, forum and review basis | Explain how a particular proposition has been followed, distinguished, limited, questioned or displaced. |
| Applicable instrument | Statute, rule or other instrument, provision, version, commencement, transitional rules and relevant period | Connect case analysis to the legal text applicable to the question being asked. |
| Application analysis | Issue, governing forum and time, proposed rule, element-by-element facts and evidence, competing arguments, exceptions, uncertainty and conditional conclusion | Show how a principle is applied and which missing facts could change the result. |
| Provenance and review | Source retrieval and inspection dates, permitted snapshot/hash where available, extraction or translation method, author/AI contribution, reviewer and review scope, correction history and known gaps | Let users inspect how the record was produced and what has actually been checked. |

Keep source availability, last successful retrieval, last substantive legal
review and treatment-search coverage separate. A working URL or an unchanged
file does not establish the present legal status of a proposition.

Authority is assessed for the particular proposition, forum, legal system and
date. A single whole-case label is too coarse when different passages have
different treatment histories. The local legal tradition determines which
precedential distinctions apply.

## 4. How we select landmark and key cases

Use explicit editorial categories, allowing more than one category with a
reason. These are repository selection labels, rather than court-issued
certifications or a universal hierarchy.

| Category | Reason to include |
| --- | --- |
| Foundational | Establishes an important framework or starting point for the selected issue. |
| Leading | Supplies a central authority for a defined issue in the relevant jurisdiction. |
| Clarifying | Resolves an ambiguity, explains an element or revisits earlier language. |
| Limiting or contrary | Restricts a proposition, supplies a competing approach or reveals an exception. |
| Important application | Shows how a principle operates under materially different facts or procedural conditions. |
| Emerging candidate | May become significant but still requires assessment, appeal checks or fuller context. |

Citation counts, reading lists and secondary commentary can help discovery.
Selection still requires inspection of the decision and an explanation of its
legal significance. A source being frequently cited does not explain whether
the citation supports, distinguishes or criticises the relevant proposition.

Define coverage by **jurisdiction, courts, issues, period, languages, sources
and review date**. Publish the known gaps and unavailable sources. Expand from
the existing Singapore accountability questions in bounded tranches; include
comparative authorities for a stated analytical purpose. Avoid calling a
collection exhaustive without a defined universe and evidence of coverage.

## 5. The recurring workflow

1. **Choose the next useful question.** Start from the current collection,
   unresolved gaps, corrections and actual user needs. Specify the intended
   jurisdiction, period and acceptance criteria before selecting cases.
2. **Discover and identify candidates.** Prefer official judicial sources and
   permitted legal-data services. Resolve duplicate citations while preserving
   distinct judgments, proceedings and opinions. Keep discovery metadata
   distinguishable from inspected source content.
3. **Inspect sources and permissions.** Read the relevant primary text in
   context, confirm identity and pinpoints, and record the allowed uses of the
   source. Retain only permitted material and publish it only to the extent
   authorised.
4. **Prepare narrow analysis.** Record the facts, issues, reasoning and
   propositions. Separate the court's reasoning from editorial synthesis.
   Check linked legislation, contrary authorities, appeals and later treatment
   within an explicitly recorded search scope.
5. **Check and review.** Run relevant structural and citation checks; inspect
   source-to-proposition support and qualifications. Keep technical validation,
   AI source inspection and a person's substantive review separately recorded.
6. **Publish at the evidenced review stage.** Release useful candidate or
   AI-prepared material with its status and limits prominent. A human-reviewed
   label requires the actual review and its recorded scope. Provide source
   links, practical research uses, coverage limits and a correction route.
7. **Maintain the dependencies.** Revisit affected propositions, applications
   and reading guides when new decisions, legislation, corrections or changed
   sources are discovered. Preserve earlier versions and explain substantive
   changes. A failed retrieval must retain the last successful observation and
   expose the failed attempt.

For each bounded update, record the question addressed, sources actually
inspected, material change, verification performed, unresolved limitations and
one next action. The existing progress record and Git history provide the
audit trail; avoid competing trackers that can drift apart.

## 6. Automation and substantive review

Automation should assist permitted discovery, metadata normalisation, duplicate
candidate detection, source receipts, draft extraction, link checks, change
alerts and a prioritised review queue. Preserve the source and method behind
each generated suggestion. Sampling and rate limits should be explicit, with
failed or partial runs visible.

Legal significance, the scope of a holding, treatment classification and
application require contextual assessment. Model-generated interpretations
remain identifiable as AI-prepared until an appropriate person reviews them.
A confidence score, passing test or second AI review cannot substitute for
that person's work. In the existing ledger, `checked` records a person's
declared review; it does not authenticate the reviewer or certify correctness.
Follow the [research standard](RESEARCH_STANDARD.md) and
[review method](review_method.md).

The intended dependency system should flag affected records for reconsideration
when their basis changes. Preserve the historical review declaration, its
version and scope, alongside the new recheck need. Presently, the ledger's
`compare` command flags differences between supplied snapshots without changing
review declarations, and Source Watch checks explicitly listed local files.
Neither supplies an automatic global legal-treatment monitor. See the
[current component description](ROADMAP.md#current-components).

## 7. Turning principles into reasoned applications

An application record should identify the question and governing law, state
each relevant element or condition, connect material facts to evidence, assess
qualifications and competing arguments, and explain a conditional conclusion.
Claimant capacity, procedure, causation, defences, limitation and remedies need
their own analysis when relevant to the issue.

For each factual element, use explicit analytical states such as **supported,
contradicted, disputed or unknown**, with reasons and sources. Keep uncertainty
about facts separate from uncertainty about the applicable law. These are
proposed application-layer states, not replacements for the existing ledger's
evidence-link types or review-status values.

A missing fact should produce a targeted research or evidence question. For
example, a clearly fictional exercise may identify an applicable duty framework
while the claimant's reliance, caused loss or available remedy remains unknown.
Label teaching assumptions as fictional and retain all conditions that prevent
a conclusion. A broad legal principle alone cannot determine a real dispute.

## 8. Global scope and responsible source access

Expand through jurisdiction-specific coverage plans and appropriate local
expertise. Preserve court structures, legal traditions and the role of
legislation in each system. Common-law terminology should be used where it
fits; other systems require their own account of a decision's authority.
Cross-jurisdiction comparison needs an explicit question and explanation of
the differences that matter.

Retain original-language source references. Identify official, professional
and machine translations separately, and surface wording that still requires
original-language review. An English summary cannot silently become the
authoritative text.

For each proposed data source, record permission for retrieval, retention,
computational analysis and republication separately. Check applicable terms,
API conditions, attribution, reporting restrictions, redactions and correction
or withdrawal requirements before scaling ingestion. Public access to a page
does not settle every reuse question. Use an approved interface or obtain the
necessary permission when required. The existing [rights statement](../RIGHTS.md)
continues to govern this repository; third-party materials retain their terms.

## 9. Current position and the next development steps

At the date of this record, the collection includes the
[Singapore sustainability-reporting case](../cases/singapore-sustainability-reporting/README.md)
and its [common law authority map](../cases/singapore-sustainability-reporting/common-law-authorities.md).
The original case ledger has two unreviewed propositions. The authority map
contains AI-prepared source analysis, sampled subsequent treatment and recorded
gaps. Independent human legal review remains outstanding.

The structured case/proposition/treatment model, global coverage interface,
automated treatment maintenance and application models described here are
development directions. Their completion must be supported by implementation
and verification records.

The next bounded sequence is:

1. **Specify and trial a small structured tranche from the existing authority
   map.** Agree the contract with core development. Preserve original sources,
   pinpoints, qualifications, stable identifiers and AI-prepared review states.
   Include a coverage/gap record and demonstrate that one judgment can support
   several separately qualified propositions.
2. **Connect treatment and instruments.** Model a limited, inspected set of
   later decisions and period-specific provisions, including an unresolved or
   limiting relationship. Test how an affected proposition is identified for
   reconsideration without inventing or overwriting a person's review.
3. **Develop useful applications and navigation.** Begin with selected
   negligence, misrepresentation, standing and remedy questions as appropriate
   to the source base. Use clearly fictional examples or expressly permitted
   materials, and make missing elements and competing arguments visible.
4. **Evaluate and expand from evidence.** Obtain actual qualified review and
   observe whether users can locate the authority, recognise its limits and
   explain an application. Use the findings to choose the next tranche and
   jurisdiction. Record permission, participants and results accurately.

Legal evidence cases owns source curation and legal research records. Core
development owns schema, validation and software behaviour. Adoption work owns
the usable entry route and observed friction. The
[Research Lab](https://albertito-ai.github.io/Albertito-AI/lab/#library) can expose
selected records and reading paths while linking back to this canonical case
collection. Coordinate through the existing workstreams and maintenance
cadences; this guide creates no additional scheduler or parallel ingestion job.

## 10. How we judge progress and keep this guide useful

Evaluate a defined tranche with disclosed denominators and review methods:

- **Traceability:** can a reader reproduce the source and pinpoint for each
  published proposition?
- **Analytical quality:** how often does independent review find an unsupported
  holding, missing qualification or misclassified treatment?
- **Coverage:** which declared issues, courts, periods and languages are covered,
  and which important gaps remain?
- **Currency:** when were the source, treatment search and substantive review
  last completed, and which known changes still await attention?
- **Usefulness:** can users find the controlling or relevant authority,
  distinguish its limits and complete the intended research task?
- **Maintenance:** how quickly are evidenced corrections assessed and affected
  records brought back for review, given available capacity?

Report actual observations and limitations. Establish baselines before claiming
an accuracy, time-saving or educational improvement. An increase in entries,
scheduled runs or GitHub activity is an operational measure only.

Consult this guide when selecting case work, proposing automation, expanding
coverage or making a public capability claim. Revise it when source constraints,
legal review or observed use justify a change. Record the reason and consequences
in the same reviewed change, preserve earlier decisions in Git history, and
update the roadmap's next action. The continuing test is whether a user can
understand, inspect and responsibly use the knowledge we publish.
