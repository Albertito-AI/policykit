<!-- atlas-whitepaper:managed:v1 -->

# RegNav: from published assertions to accountable reasons

## The central argument

A disclosure is useful only if a reader can understand what is asserted, locate its basis, recognise its qualifications and identify the decisions that remain open. RegNav treats those links as working research objects. Its thesis is that accountability improves when the path from document to proposition to judgement becomes inspectable, revisable and portable.

The project starts with sustainability reporting and legal accountability, but the underlying problem is broader: institutions often possess documents without a reliable record of how those documents justify a decision. RegNav aims to reduce that gap. It does not turn a collection of citations into verified law or a collection of environmental numbers into proven performance.

This whitepaper was prepared for Albert Tan Sin Hon with AI assistance on 2 November 2026. It is an original design synthesis, not an independently reviewed scholarly article or an issuer-specific legal assessment. Future directions below are proposals, subject to the project's existing rights and evaluation gates.

## First principles: traceability is necessary and insufficient

The first principle is proposition-level reasoning. A broad conclusion should be decomposed into claims narrow enough to examine. Each claim should identify its jurisdiction, relevant time, source version, location and qualifications where applicable. Evidence may support, qualify, contradict or contextualise it. Contrary evidence is part of the record rather than a nuisance to remove.

The second principle is separation of observations. Finding a quotation establishes a location in retained text. It does not establish authenticity, substantive support or legal effect. Computing an emissions inventory establishes arithmetic under supplied factors and units. It does not establish that activity data are complete or that the chosen factors are appropriate. A `checked` entry records a person's declared review; it does not authenticate the reviewer or prove the judgement sound.

The third principle is revision without amnesia. A later source, restatement or change in interpretation should not erase what was previously asserted and why. Comparing saved records makes the dependency of earlier review visible. Good institutional memory includes reasons for correction, unresolved disagreement and the limits of the evidence.

## Fundamental logic of the workbench

The public workflow has two connected layers. The evidence ledger represents propositions, sources, evidence links and review declarations in portable records. It validates structure, generates readable matrices and compares snapshots. The ESG workbench ingests documents, retains page text and source fingerprints, extracts candidates and exports records for human review.

Physical PDF pages, exact quotations, offsets and parser information make an extraction inspectable. Incomplete extraction remains an explicit state. Optional model assistance receives selected context and returns structured candidates; unsupported quotation or literal-field outputs can be rejected. Protocol tests do not substitute for a live-model evaluation or an independent accuracy study.

Calculation, materiality screening and action planning use explicitly supplied inputs. Keeping financial and impact perspectives separate avoids hiding different questions inside one score. A standards reference is a located record, not proof that its requirements apply to a particular entity. The workflow should show the supplied rubric and assumptions alongside its result.

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

## Measuring improvement rather than activity

A report-pair evaluation should use independently checked reference data and measure anchor accuracy, supported-field coverage, extraction failures, abstentions and reviewer effort. It should include changed boundaries, restatements, partial assurance, contradictory passages and difficult tables. Record the cost of preparing inputs and correcting outputs, not only the speed of generation.

Legal evaluation is a separate exercise. Structural validity, successful parsing and a well-formed citation do not establish current authority or a justified legal inference. Human review must actually occur before it is recorded. Educational evaluation should test whether learners better distinguish evidence from interpretation, without treating a manual-first practice sequence as a controlled causal study.

Failure conditions include persistent false confidence, inaccessible review interfaces, hidden private dependencies and burdens that exceed the value of the record. A responsible project narrows or revises its claims when evidence demands it. Its ideal endpoint is a durable practice of accountable reasoning, with software serving that practice.

## Inspected foundation and boundaries

Baseline: [`3fa5c46ebfcbce3639e66884167984543f0a7600`](https://github.com/Albertito-AI/policykit/tree/3fa5c46ebfcbce3639e66884167984543f0a7600). Sources: [README](https://github.com/Albertito-AI/policykit/blob/3fa5c46ebfcbce3639e66884167984543f0a7600/README.md), [roadmap](https://github.com/Albertito-AI/policykit/blob/3fa5c46ebfcbce3639e66884167984543f0a7600/docs/ROADMAP.md), [progress](https://github.com/Albertito-AI/policykit/blob/3fa5c46ebfcbce3639e66884167984543f0a7600/docs/PROGRESS.md) and [workstreams](https://github.com/Albertito-AI/policykit/blob/3fa5c46ebfcbce3639e66884167984543f0a7600/docs/WORKSTREAMS.md). Public source visibility grants no general open-source or commercial reuse licence. Private research material, participant data and client records remain outside the public project. This paper changes no review declaration or legal conclusion.
