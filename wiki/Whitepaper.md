<!-- atlas-whitepaper:managed:v1 -->

# RegNav: from published assertions to accountable reasons

## Abstract

RegNav is a local research prototype for connecting sustainability disclosures and legal propositions to inspectable evidence. It combines a structural evidence ledger with a document-oriented ESG workbench, while reserving substantive interpretation for reviewers. This paper defines those boundaries, follows a fictional source disagreement through the ledger, and separates implementation evidence from proposed evaluation. The contribution is an explicit record of claims, qualifications, sources and review declarations that can be inspected and revised. Independent usability, legal accuracy, learning benefit and improved environmental decisions remain unestablished.

## The central argument

A disclosure is useful only if a reader can understand what is asserted, locate its basis, recognise its qualifications and identify the decisions that remain open. RegNav treats those links as working research objects. Its thesis is that accountability improves when the path from document to proposition to judgement becomes inspectable, revisable and portable.

The project starts with sustainability reporting and legal accountability, but the underlying problem is broader: institutions often possess documents without a reliable record of how those documents justify a decision. RegNav aims to reduce that gap. It does not turn a collection of citations into verified law or a collection of environmental numbers into proven performance.

This whitepaper was prepared for Albert Tan Sin Hon with AI assistance on 2 November 2026 and revised against the source identified below on 15 November 2026. It is an original design synthesis, not an independently reviewed scholarly article or an issuer-specific legal assessment. Future directions below are proposals, subject to the project's existing rights and evaluation gates.

## First principles: traceability is necessary and insufficient

The first principle is proposition-level reasoning. A broad conclusion should be decomposed into claims narrow enough to examine. Each claim should identify its jurisdiction, relevant time, source version, location and qualifications where applicable. Evidence may support, qualify, contradict or contextualise it. Contrary evidence is part of the record rather than a nuisance to remove.

The second principle is separation of observations. Finding a quotation establishes a location in retained text. It does not establish authenticity, substantive support or legal effect. Computing an emissions inventory establishes arithmetic under supplied factors and units. It does not establish that activity data are complete or that the chosen factors are appropriate. A `checked` entry records a person's declared review; it does not authenticate the reviewer or prove the judgement sound.

The third principle is revision without amnesia. A later source, restatement or change in interpretation should not erase what was previously asserted and why. Comparing saved records makes the dependency of earlier review visible. Good institutional memory includes reasons for correction, unresolved disagreement and the limits of the evidence.

## Definitions and the public contract

| Object | Operational meaning | Boundary |
| --- | --- | --- |
| Proposition | An authored claim with an identity and review status | The programme does not derive its truth |
| Evidence link | An entered source ID, pinpoint and relation such as `supports` or `contradicts` | A valid relation field need not be a justified interpretation |
| Source anchor | A location and quotation in retained extracted text | Finding text does not establish authenticity or support |
| Review declaration | Supplied reviewer, date and status | It is not authenticated professional approval |
| Snapshot comparison | A report of differences between saved records | It does not itself retain history or reset old review statuses |

The ledger and workbench have different responsibilities. The ledger validator checks recorded structure; it does not retrieve source text or verify a quotation. The ESG layer performs separate extraction and anchoring operations. Reading their outputs together must not silently transfer one layer's capability to the other. The [research method](https://github.com/Albertito-AI/policykit/blob/465249eb48be348f87e2ef613d047403ecd14118/docs/review_method.md) and [public/private boundary](https://github.com/Albertito-AI/policykit/blob/465249eb48be348f87e2ef613d047403ecd14118/PUBLIC_PRIVATE_BOUNDARY.md) define the researcher's remaining duties and excluded material.

## Fundamental logic of the workbench

The public workflow has two connected layers. The evidence ledger represents propositions, sources, evidence links and review declarations in portable records. It validates structure, generates readable matrices and compares snapshots. The ESG workbench ingests documents, retains page text and source fingerprints, extracts candidates and exports records for human review.

Physical PDF pages, exact quotations, offsets and parser information make an extraction inspectable. Incomplete extraction remains an explicit state. Optional model assistance receives selected context and returns structured candidates; unsupported quotation or literal-field outputs can be rejected. Protocol tests do not substitute for a live-model evaluation or an independent accuracy study.

Calculation, materiality screening and action planning use explicitly supplied inputs. Keeping financial and impact perspectives separate avoids hiding different questions inside one score. A standards reference is a located record, not proof that its requirements apply to a particular entity. The workflow should show the supplied rubric and assumptions alongside its result.

## Worked example: structural success with unresolved substance

The [synthetic ledger](https://github.com/Albertito-AI/policykit/blob/465249eb48be348f87e2ef613d047403ecd14118/examples/synthetic_ledger.json) contains three propositions, two source records and four evidence links. Its fictional draft A gives a five-working-day response requirement at A.3; draft B gives ten working days at B.2. `CLAIM-timing` retains one supporting and one contradictory link and remains contested. The exercise supplies no rule choosing which draft governs. The tool reports the authored disagreement; it does not discover or resolve it from the source text.

A second proposition, `CLAIM-remedy`, asserts a further review procedure that the complete fictional packet does not state. It remains unreviewed and has an empty pinpoint. Normal validation reports zero structural errors and three warnings: `UNREVIEWED_CLAIM`, `MISSING_PINPOINT` and `CONTESTED_CLAIM`. These are the [documented reference results](https://github.com/Albertito-AI/policykit/blob/465249eb48be348f87e2ef613d047403ecd14118/docs/evaluation_protocol.md), not an assertion that the material is substantively correct.

The counterexample is deliberate: entering any non-empty location can satisfy a field requirement without making that passage support the proposition. Likewise, adding an explanation to a resolution field can satisfy a structural condition without resolving a legal disagreement. Review must examine relevance and reasoning. Changing `checked` by automation would misrepresent work that only the named person can declare.

### Reproduction and claim-to-evidence map

From an exact checkout of `465249eb48be348f87e2ef613d047403ecd14118`, use Python 3.10 or newer:

```sh
python -m regnav_evidence validate examples/synthetic_ledger.json
python -m regnav_evidence report examples/synthetic_ledger.json --format markdown
python -m regnav_evidence validate examples/synthetic_ledger.json --strict
python -m unittest discover -s tests -v
```

Normal validation returns exit 0 despite the three warnings; strict validation returns exit 2 for the same fixture. Read the complete fictional packet linked by the [learner handout](https://github.com/Albertito-AI/policykit/blob/465249eb48be348f87e2ef613d047403ecd14118/teaching/learner_handout.md) before interpreting the matrix. Retain command output, environment, commit, fixture version and any failures or skips. These instructions do not claim a fresh execution during this documentation review.

| Claim | Source evidence | Interpretation limit |
| --- | --- | --- |
| Structural validity is distinct from truth | [Validator notice and rules](https://github.com/Albertito-AI/policykit/blob/465249eb48be348f87e2ef613d047403ecd14118/regnav_evidence/validation.py); [tests](https://github.com/Albertito-AI/policykit/blob/465249eb48be348f87e2ef613d047403ecd14118/tests/test_validation.py) | Tests exercise structure, not the legal interpretation of arbitrary sources |
| Saved ledger differences can be inspected | [Comparison implementation](https://github.com/Albertito-AI/policykit/blob/465249eb48be348f87e2ef613d047403ecd14118/regnav_evidence/changes.py) | The caller must retain snapshots and reconsider review |
| Extraction candidates retain text anchors | [Extraction implementation](https://github.com/Albertito-AI/policykit/blob/465249eb48be348f87e2ef613d047403ecd14118/regnav_esg/extract.py) | Anchor checks are weaker than substantive support; live-model quality requires separate evidence |
| A volunteer task protocol exists | [Evaluation protocol](https://github.com/Albertito-AI/policykit/blob/465249eb48be348f87e2ef613d047403ecd14118/docs/evaluation_protocol.md) | A written procedure is not evidence that volunteers participated |
| Public and private capabilities differ | [README](https://github.com/Albertito-AI/policykit/blob/465249eb48be348f87e2ef613d047403ecd14118/README.md) and [boundary policy](https://github.com/Albertito-AI/policykit/blob/465249eb48be348f87e2ef613d047403ecd14118/PUBLIC_PRIVATE_BOUNDARY.md) | Private extension capabilities are not installed by the public package |

## Why comparability is a substantive question

Consider the fictional report sequence in the repository: a prior figure of 100, a current figure of 110, and a later statement restating the prior figure to 120. The simple calculation against 100 is a 10% increase. Against a justified restated baseline of 120 it is approximately an 8.33% decrease. Neither direction alone establishes environmental improvement.

The analyst must ask whether the entity, boundary, method, unit, period and factors are comparable, and why a restatement occurred. A precise percentage can conceal a category error. The public extraction layer helps locate the relevant statements. A separately maintained private research extension represents additional comparability and applicability checks; it is not included in the public installation. This distinction protects both users and the integrity of the public project's claims.

An assurance statement raises a similar issue. Coverage of one metric at one facility cannot silently become assurance over an entire report. The ideal evidence model should retain scope and exceptions at the same granularity as the claim being reviewed.

## Aim and hope: accountable sustainability decisions

The immediate aim is a usable local research workflow that makes source checking less fragmented. The larger hope is that researchers, reporting teams, educators and civil-society organisations can ask better questions of institutional claims, even with limited resources.

The pathway to public benefit is concrete: locate the passage; expose a mismatch or missing qualification; obtain appropriate review; correct the claim or decision; retain the explanation. Each step can fail. Better software alone cannot ensure disclosure quality, competent enforcement, remedies or institutional willingness to respond.

RegNav should therefore resist becoming a decorative compliance dashboard. The value lies in making uncertainty and responsibility legible. People affected by an environmental claim should be able to understand its basis and challenge a missing premise, rather than receive a score whose construction they cannot inspect.

## Ideal progression

| Stage | Desired result | Advancement gate |
| --- | --- | --- |
| Dependable local work | Faithful records, exports and recovery | Reproduction, source-anchor checks and meaningful regressions |
| Independent usefulness | A new reviewer completes a permitted report-pair task | Observed setup, errors, abstentions and whole-task effort |
| Evaluated research cases | Narrow propositions with qualified source review | Actual reviewers, exact versions, qualifications and retained dissent |
| Wider coverage | Additional jurisdictions, languages and document structures | Local expertise, licensed sources and explicit coverage gaps |
| Accountable operation | Controlled collaboration and maintained evidence dependencies | Authenticated roles, confidentiality, recovery and institutional responsibility |

The wishlist includes accessible source navigation; faithful multilingual extraction; more dependable table and OCR handling; versioned factors; clearer correction histories; carefully mapped case-law relationships; and interoperability with other evidence systems. The priority remains observed user difficulty. A wider corpus without reliable source selection and review could make the project less trustworthy.

## Related methods and questions for evaluation

The W3C [PROV-DM Recommendation, 30 April 2013](https://www.w3.org/TR/2013/REC-prov-dm-20130430/), particularly its overview and entities/activities/agents concepts, provides a useful comparison for recording how an information object was produced and by whom. RegNav's claim-to-source links add an authored evidential interpretation for this workflow. They should not be confused with a provenance standard's interchange contract. No PROV conformance, export implementation or priority claim is made here.

Within the project, [Research Standard](https://github.com/Albertito-AI/policykit/blob/465249eb48be348f87e2ef613d047403ecd14118/docs/RESEARCH_STANDARD.md) requires source identity, time, pinpoints, contrary authority and correction history. The [teaching materials](https://github.com/Albertito-AI/policykit/blob/465249eb48be348f87e2ef613d047403ecd14118/teaching/learner_handout.md) translate those requirements into inspectable tasks. These are project methods, not independent scholarly validation of their effectiveness. Future comparative research should document why a structured ledger improves a particular task relative to an ordinary annotated document or spreadsheet, including the additional setup cost.

The existing small volunteer protocol gives completion codes, time allowances, reference results, assistance recording and stopping decisions. It explicitly recognises convenience sampling and practice effects from using the same packet manually before software tasks. Any later claim of causal benefit needs comparable independent tasks, an appropriate comparison procedure, a defined sampling plan and treatment of failed setup. It must not reuse descriptive pilot timings as a controlled effect estimate.

### Teaching application

Ask a learner to reconstruct the two conflicting deadline passages, explain the unsupported further-review claim and identify the status of the fictional reviewer. Then give an apparently complete but irrelevant pinpoint and ask what validation can establish. Assess source identity, location, qualification, contrary evidence and residual uncertainty separately. Require a revised narrow proposition with reasons; do not reward a confident `checked` label alone. The exercise can assess an answer on this packet, but a claim of general learning improvement requires separate evaluation.

## Measuring improvement rather than activity

A report-pair evaluation should use independently checked reference data and measure anchor accuracy, supported-field coverage, extraction failures, abstentions and reviewer effort. It should include changed boundaries, restatements, partial assurance, contradictory passages and difficult tables. Record the cost of preparing inputs and correcting outputs, not only the speed of generation.

Legal evaluation is a separate exercise. Structural validity, successful parsing and a well-formed citation do not establish current authority or a justified legal inference. Human review must actually occur before it is recorded. Educational evaluation should test whether learners better distinguish evidence from interpretation, without treating a manual-first practice sequence as a controlled causal study.

Failure conditions include persistent false confidence, inaccessible review interfaces, hidden private dependencies and burdens that exceed the value of the record. A responsible project narrows or revises its claims when evidence demands it. Its ideal endpoint is a durable practice of accountable reasoning, with software serving that practice.

## Inspected foundation and boundaries

Source reviewed for this revision: [`465249eb48be348f87e2ef613d047403ecd14118`](https://github.com/Albertito-AI/policykit/tree/465249eb48be348f87e2ef613d047403ecd14118). Source and test assertions were inspected without a fresh runtime or participant evaluation. Sources: [README](https://github.com/Albertito-AI/policykit/blob/465249eb48be348f87e2ef613d047403ecd14118/README.md), [roadmap](https://github.com/Albertito-AI/policykit/blob/465249eb48be348f87e2ef613d047403ecd14118/docs/ROADMAP.md), [progress](https://github.com/Albertito-AI/policykit/blob/465249eb48be348f87e2ef613d047403ecd14118/docs/PROGRESS.md) and [workstreams](https://github.com/Albertito-AI/policykit/blob/465249eb48be348f87e2ef613d047403ecd14118/docs/WORKSTREAMS.md). Public source visibility grants no general open-source or commercial reuse licence. Private research material, participant data and client records remain outside the public project. This paper changes no review declaration or legal conclusion.
