# RegNav roadmap

## Purpose

Make the evidence and interpretive choices behind legal propositions easier to
inspect. Begin with legal accountability in sustainability reporting across
Asian jurisdictions. Build reusable methods before expanding coverage.

## Current component

Version 0.1 provides an offline evidence ledger, structural validation,
Markdown and CSV reports, read-only comparison of saved snapshots,
a synthetic worked example and regression tests.
The code has no external runtime dependency. A complete fictional teaching
exercise, external usability protocol, first-use guide and contribution routes
are available. A narrow Singapore case records two unreviewed propositions
against official primary sources. Real-world usefulness, educational benefit
and legal dataset quality still require evaluation. See the
[project status](project_status.md) for the evidence baseline.

## Completed safeguard: compare saved ledger versions

The read-only `compare` command identifies substantive changes to propositions,
evidence links and source records and flags potentially stale prior declarations.
Metadata-only access-date and review-declaration updates are distinguished.
Identifiers are matched literally; any renamed identifier is recorded as a
removal and addition. No reviewer is authenticated and no review status is
changed by the command. Further refinement should be driven by actual review
friction rather than speculative features.

## Evidence-export integrity

Markdown evidence reports should retain the literal wording of recorded
propositions and source titles, including GitHub-flavoured Markdown's
strikethrough delimiters (`~~`). A targeted exporter regression protects
these delimiters from being interpreted as deletions in the rendered report.
The JSON remains the authoritative record; exported formatting is not evidence
that any proposition is correct. Follow up on concrete user-reported rendering
problems rather than adding speculative export formats.

## Next work in priority order

1. **Obtain human review of the first worked case.** The
   [Singapore example](../cases/singapore-sustainability-reporting/README.md)
   now records two narrow propositions, inspected primary sources and exact
   pinpoints. Both remain unreviewed. A reviewer should examine the source
   versions, reporting-period limits and each evidence relationship before
   entering an actual declaration. Do not expand case volume ahead of this
   review or represent an AI inspection as completed human assessment.
2. **Run the first external usability pilot.** Use the prepared
   [protocol](evaluation_protocol.md) with three independent volunteers. Record
   task completion, assistance, misunderstandings and reproducible difficulties
   privately. Revise concrete defects and report bounded, anonymous results.
   Keep the answer key linked from the manual quickstart for post-task checking;
   do not supply it before observed responses, and record earlier exposure.
   The manual-first sequence is not a controlled comparison and cannot establish
   a productivity or learning benefit. Design any later comparative evaluation
   separately.
3. **Improve entry and review.** Choose a CSV import or an accessible browser
   editor only after observing where users struggle. Preserve offline access
   and the JSON record. Check import ambiguities and export fidelity.
4. **Extend the legal comparison.** Add the second jurisdiction when the first
   worked case is stable. Distinguish disclosure duties, supervision, liability,
   standing and remedies. Record disagreements rather than forcing equivalence.
5. **Prepare a citable release.** Follow the
   [release criteria](release_readiness.md), including rights, documentation,
   evaluation limits and outstanding defects. Use a stable version and an
   archival record if an appropriate connection and rights permit it. No DOI
   has yet been assigned.

## Proposed first twelve weeks

| Period | Intended outcome | Evidence needed |
| --- | --- | --- |
| Weeks 1 to 2 | Reliable ledger and record-change design | Passing relevant checks and reproducible example |
| Weeks 3 to 4 | Human review of the first narrow legal case | Actual review of source versions, pinpoints and documented limits |
| Weeks 5 to 8 | Usability pilot and targeted revision | Actual task observations and a correction record |
| Weeks 9 to 12 | Evaluated demonstration and release decision | Complete documentation, rights review and honest results |

These are planning targets, not delivery or adoption guarantees. Reorder the
work when actual defects, user feedback or source availability justify it.

## Other programmes

The [teaching exercise](../teaching/README.md) is a first, unevaluated resource
for legal education with AI. It examines how a written answer can be traced
to sources and revised when its claims exceed the evidence. The next teaching
action is to observe a small pilot using the prepared protocol, then revise
the instructions in response to actual difficulties. These materials are
separate from the coauthored ANSWERABLE book project. Sports governance can
supply later case studies once the core workflow is useful.

## Bounded technical experiment: source-file changes

On 24 October 2026 the maintainer requested a separate technology-product
experiment alongside the research programme. [Source Watch](../experiments/source_watch/README.md)
checks byte changes in explicitly listed local files and returns their linked
claim identifiers. It is isolated from the ledger schema and command interface.
A runnable fictional demo and generated report make the proposed behaviour
inspectable without receiving confidential material or paying for a hosted service.

The next gate is independent reproduction under an agreed permission and a
concrete recurring user need, not more speculative features. CONTRIBUTING.md
now distinguishes public synthetic bug reports from private Source Watch
rights, evaluation and commercial enquiries.
The root README now leads to the generated report and a short evaluation enquiry route. Record
actual enquiries and permissions separately from completed evaluations or paid
work. Record missing sources, false-positive friction,
requested integrations and the limits of any observation. Do not build a hosted
API, external-source crawler or new dependency merely to fill a schedule.
The existing human source-review and teaching-pilot priorities remain outstanding.
No subscription, commercial licence, production service or customer adoption is
established by this experiment. Preserve the existing rights statement.

## Public website link

The README now links to [Albert Tan's website](https://www.alberttansinhon.com/).
At the next public-link review, check that this canonical address still resolves.

## Agent interoperability: one bounded first connection

The maintainer requested this integration on 25 October 2026. The
[local MCP gateway](../experiments/agent_gateway/README.md) now makes the existing
Source Watch check callable by a permitted local client without granting caller
control of paths, shell commands or the baseline. The
[network proposal](AGENT_NETWORK.md) and technical issue form provide an opt-in
route; the catalogue records no external partners, public endpoint or payment.

The next gate is one independent, permissioned MCP-client reproduction with
fictional inputs and an actual recurring workflow to assess. Record client and
protocol versions, setup effort, output interpretation and unresolved defects.
A public registry entry requires its own packaging, namespace, rights and
verification steps. External delegation needs separate authentication and task
controls. Do not describe the local prototype as a deployed marketplace or
substitute simulated exchanges for partners or customers. Existing human source
review and teaching-pilot priorities remain unchanged.

The root README now links directly to the gateway, generated exchange, catalogue
and existing pilot invitation. Use that route to qualify one operator's actual
task and agree the necessary permissions before an independent test. Record a
reply, a completed evaluation and a paid agreement separately; do not count this
navigation improvement as external use or a new participant.

## Proposed evidence-handover improvements

The [evidence-handover development plan](EVIDENCE_HANDOVER_PLAN.md) records six
conditional work items and eighteen proposed acceptance cases. They are specified,
not implemented; the cases are `NOT_RUN`. This links the proposed export mapping,
source/record/process comparison, scope checks, review history, evaluation and
later agent integration without advertising them as existing capabilities.

The next action is to qualify one permitted task and inspect the actual inputs.
Use the existing tools first where they already meet that need. For a justified
export adapter, agree one versioned format and acceptance check before implementing
RN-M01. Core development owns the implementation and adoption owns independent
workflow observations. Preserve current human source-review and usability
priorities, offline use, existing rights and truthful review declarations.
