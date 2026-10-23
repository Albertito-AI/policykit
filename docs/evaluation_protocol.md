# Three-volunteer observational usability pilot

**Status:** proposed procedure with no participant results. This protocol was
developed with AI assistance. It is an unevaluated pilot of the research
prototype, not a statistical study of legal accuracy or an assessment of
students. Read the [research standard](RESEARCH_STANDARD.md).

## Question and scope

Can three external volunteers use the supplied instructions to run the tool,
read its report, identify the intended review gaps and describe a problem in
a reproducible way? Record where each task succeeds independently, requires
help or remains blocked. Observe the manual evidence task as well, so that
software behaviour is not confused with reading and interpretation.

Use only [the synthetic ledger](../examples/synthetic_ledger.json) and
[its complete fictional sources](../examples/training_sources.md). The
source texts, propositions, dates and reviewer details are invented. They
must not be replaced with private, client or student material in this pilot.
There is no live legal dataset to evaluate.

## Participants and practical preparation

Invite three willing adults who did not write the software or these materials.
Record broad prior command-line and evidence-ledger experience without names
or institutional identifiers. Aim to include differing levels of command-line
experience if feasible; record the actual sample instead of claiming that
it represents legal researchers generally.

Use participant codes `V01`, `V02` and `V03`. Explain that participation is
voluntary, that they may stop and that the observation concerns the tool and
instructions rather than their competence. Obtain agreement to anonymous
written notes. No audio or screen recording is required. Determine any
applicable institutional requirements before using this activity as formal
participant research or collecting additional personal information.

Allow about 40 minutes per volunteer, plus five minutes for optional feedback.
Copy [the blank feedback form](../teaching/feedback_template.md) to a private
local working file. Do not commit completed forms. Record the software version,
commit identifier if available, Python version, operating system, fixture
version or digest and any differences from this procedure.

Provide the repository files and README. A CLI attempt requires Python 3.10
or newer; no third-party packages, API keys or network access are required to
run the commands. Record any preparation or installation help separately from
task completion. Have the handout's report snapshot available as a fallback
so a setup failure does not prevent observing later reading tasks.

Do not give the answer key, expected warning names or later scoring criteria
to the volunteer before the task. Reading the ordinary README is allowed;
this tests the documented workflow. If the volunteer has already seen the
teaching exercise, record that exposure and its possible effect.

## Observation procedure

Read each task prompt as written. Ask the volunteer to describe what they are
doing if comfortable. Start timing when the prompt has been read. Within the
allowance, avoid giving a substantive answer. If help is requested or progress
stops, record the exact help and mark the task assisted. At the allowance,
record any incomplete task as blocked, then offer the fallback or explanation
needed to continue. Do not silently exclude a failed installation.

Completion codes are `I` for independent, `H` for completed after help, `B`
for blocked or incomplete and `N` for not attempted. Record the actual answer
as well as the code. Time is descriptive, including any help given; it is not
a measured productivity gain.

| Task | Volunteer prompt and allowance | Observer criterion |
| --- | --- | --- |
| T1: manual source record | "Read the fictional source packet. On paper or in a spreadsheet, record what each draft says about the response deadline, with a pinpoint. State whether these materials let you choose which draft governs." Allow 6 minutes. | Identifies A.3 as five working days and B.2 as ten working days; records that no governing rule is supplied. Preserve the actual response even if incomplete. |
| T2: run and export | "Using the README, validate the synthetic ledger and display a Markdown report. Explain whether you obtained a report and what the validation result means." Allow 10 minutes, including the documented commands. | Runs normal validation and report successfully, distinguishes zero structural errors from three warnings, and locates the report. If setup is blocked, record it and use the printed snapshot for later tasks. A fallback does not count as running the tool. |
| T3: read the report | "Find the proposition with no completed review declaration, its missing source location, and the proposition recorded as contested. Explain why one proposition appears on two evidence rows." Allow 6 minutes. | Finds `CLAIM-remedy`, its missing pinpoint, and `CLAIM-timing`; explains the two source links. Locating a warning alone does not establish substantive review. |
| T4: identify the evidence gaps | "Check the report against the complete fictional sources. Is a further review procedure stated? Can adding any non-empty pinpoint establish it? Explain the timing disagreement and what the checked entry tells you." Allow 8 minutes. | Finds no stated further review in A.1 to A.3 or B.1 to B.2; rejects an irrelevant pinpoint as evidence; preserves the timing discrepancy; recognises `checked` as a declaration and the supplied reviewer as fictional. Record these four observations separately. |
| T5: report a problem | "Use the local feedback form to describe one difficulty or defect you actually encountered, with steps another person could follow. If none occurred, say so and describe the tasks you attempted; you may offer a labelled clarity suggestion." Allow 5 minutes. | Gives actual steps, input, expected and observed behaviour, and relevant environment details without private information. If no problem occurred, an honest bounded statement is complete; inventing a defect is not required. |

Reserve about five minutes for introduction and transitions. The optional final
five minutes asks which instruction should change first and whether the report
suggested more certainty than the sources justified.

## Reference results for the observer

The fixture's expected normal validation result is zero errors, three warnings
and exit `0`. The warnings are `UNREVIEWED_CLAIM` at `$.claims[1]`,
`MISSING_PINPOINT` at `$.claims[1].evidence[0].pinpoint` and `CONTESTED_CLAIM`
at `$.claims[2]`. With `--strict`, the same fixture exits `2`; that optional
command is not required for T2.

The report contains two source records, three propositions and four evidence
rows. `CLAIM-timing` has a supporting link to A.3 and a contradictory link to
B.2. The contradiction concerns the stated deadlines, not whether responding
on day five could satisfy a ten-day limit. Neither source supplies a governing
choice or a further review procedure. The report reflects entered relations;
the software does not derive those conclusions from the source text.

Use the [facilitator answer key](../teaching/facilitator_guide.md) when
interpreting a reasoned alternative answer. Do not mark a different wording
as a failure when it preserves the source and its scope.

## Record and decide

Prepare a small internal table with one row per volunteer and task. Record
completion code, elapsed time, help given, observed difficulty and proposed
correction. For T4, retain separate observations about further review,
pinpoint relevance, conflicting drafts and the review declaration. Report
counts such as "two of three volunteers completed T2 without help" only
after those events occurred. Give the denominator and describe non-completion.

Before the sessions, adopt these provisional product decisions:

- Any reproducible blocker in validation or report generation should be
  investigated before offering further unsupported demonstrations.
- If two volunteers need the same instruction explained, revise that instruction
  and test the specific change with a subsequent volunteer. Preserve the original
  observations and version the revised materials.
- If anyone interprets `checked` or zero structural errors as proof of legal
  truth, inspect the wording and presentation before extending the pilot.
  Record whether the misunderstanding persisted after the explicit explanation.
- A follow-up round is warranted when a concrete correction needs checking.
  Three successful sessions alone do not justify a claim of general usability,
  legal accuracy, educational benefit or commercial demand.

Keep observations separate from hypotheses about causes. If public reporting is
useful, prepare an anonymous summary of tasks, counts, failures, deviations and
changes made. Public issues should contain only the fictional input and
sanitised reproduction steps. Do not upload completed participant forms,
private notes, student data or identifying screenshots. Publish no quotation
without the participant's agreement.

## Limits of interpretation

This is a small convenience sample using a very short fictional packet. It
can reveal specific obstacles and misunderstandings. It cannot estimate a
population accuracy rate, demonstrate learning gains, establish legal
correctness or show willingness to pay.

T1 gives a manual record before the software tasks, using the same materials.
That ordering introduces familiarity and practice effects. Task times and
outcomes must not be presented as a controlled comparison or as evidence
that the software is faster or more accurate. A later benefit study would
need comparable independent tasks, an appropriate comparison procedure and
a defined sampling and analysis plan.

No completed human review should be generated by a model during the pilot.
Keep the fixture unchanged. If a volunteer separately creates a working
ledger, only that person may declare review they actually performed, and the
record must state the limited fictional scope. Passing software tests or
completing this protocol does not authenticate that declaration.
