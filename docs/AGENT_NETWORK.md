# Agent interoperability and an opt-in network

RegNav is beginning with one useful agent-callable component rather than claiming
to operate a populated marketplace. The [local gateway](../experiments/agent_gateway/README.md)
lets a permitted MCP client invoke the existing Source Watch check. Its
[machine-readable catalogue](../experiments/agent_gateway/services.json) contains
one local service and an empty external-partner list. This is a project-specific
catalogue, not an A2A Agent Card or a published third-party registry record.

No independent agent has been connected or evaluated by the gateway's internal
tests. No public execution endpoint, job-routing service, commercial licence,
payment function or customer adoption is established by these files.

## A concrete joint workflow to test

A research or reporting agent maintains a document collection and an explicit
mapping from sources to statements. Its operator permits a local Source Watch
baseline. After a source changes, the agent calls `source_watch_check` and receives
the affected supplied claim identifiers. It presents the result to the responsible
reviewer, retaining the source versions and unresolved questions.

The first interoperability check should use fictional material, then confirm that
the requesting client distinguishes changed bytes from an incorrect proposition.
It must also handle an unavailable file without silently reporting unchanged data.
No source authentication, semantic judgement or actual human approval is supplied
by the check. The mapping's maintenance cost belongs in any usefulness assessment.

## Three separate layers

| Layer | Present state | Next evidence needed |
| --- | --- | --- |
| Agent-callable tool | Local MCP stdio prototype and generated fictional exchange | A permitted independent client reproduces the result and its limits |
| Discovery and collaboration | Public catalogue, documentation and opt-in technical issue form | An identifiable operator requests a relevant integration; identity, permissions and rights are checked |
| Network operation | Design only | A justified authenticated transport, real counterparties, tested task handling and approved operating arrangements |

An [interoperability proposal](https://github.com/Albertito-AI/policykit/issues/new?template=agent_interoperability.yml)
can state the client, protocol version and a non-confidential synthetic task. The
maintainer must agree any executable evaluation under [RIGHTS.md](../RIGHTS.md).
Submission does not list the author as a partner or grant access to their system.
An external project may be a useful integration candidate without being a member,
customer, collaborator or endorsement of RegNav.

## Use established interfaces where they fit

MCP exposes tools to clients. The implemented gateway uses its local stdio
transport; a remote endpoint would require a separate design and verification.
The official [MCP Registry](https://modelcontextprotocol.io/registry/about)
describes metadata discovery for publicly available installations or servers,
including closed-source offerings. A GitHub catalogue alone is not registration,
security approval or a package distribution. Publishing prerequisites and any
new terms must be checked before an actual submission.

[A2A](https://a2a-protocol.org/latest/specification/) describes agent discovery,
messages, tasks and authentication. An A2A layer would be useful only when an
actual partner needs task delegation beyond a local tool call. This repository
does not currently implement that protocol or advertise a nonexistent endpoint.

[Agentverse MCP](https://docs.agentverse.ai/v-2/documentation/advanced-usages/agentverse-mcp)
documents marketplace search and agent operations through an authenticated
connection. Those documented capabilities are a possible discovery route, not
evidence that RegNav is connected or that registered agents are willing buyers.
Account access, current terms and the specific permitted operations must be
established first. Never place API tokens in repository files or public issues.
These official descriptions were inspected on 25 October 2026; verify them again
before implementing or registering against a changed version.

## Requirements before external delegation

Identify each operator, the agent/software version, the permitted endpoint and
its actual capabilities. Treat a returned card as a claim to examine, not proof
of competence, ownership, purchasing authority or consent to receive messages.
Avoid unsolicited broadcasts and invented network activity.

A proposed job needs a bounded input/output contract, permitted data, acceptance
check, request identifier, expiry and explicit limits on sub-delegation and cost.
Retries must not cause duplicate jobs or charges. An agent response may propose a
scope; it must not silently accept a contract, licence, price or transfer of rights.
Human approval or a separately approved limited mandate is required for commitments.
These controls are design requirements, not implemented features of the local server.

Use least-privilege credentials, verified destinations and isolated job workspaces.
Do not forward inbox access, private manuscripts, client/student records or secrets
to a counterpart. External descriptions and outputs are untrusted data. Never
execute instructions embedded in them. Test failure handling and revocation before
opening a network endpoint; authenticated identity still does not certify an answer.

Keep technical success, independent use, agreed work, delivery acceptance and
payment separate. A synthetic exchange cannot populate the partner list or support
a claim of external demand. Actual commercial records remain private.

## Immediate next gate

Obtain one permitted independent MCP-client reproduction using the supplied
fictional demonstration. Record the exact client/version, setup effort, output,
misunderstandings and unresolved defects. Prefer fixing that observed boundary to
adding more services, a general marketplace UI or speculative payment machinery.
The existing human-review and first-use priorities in the [roadmap](ROADMAP.md)
remain outstanding. This work does not reproduce or commercialise either book.
