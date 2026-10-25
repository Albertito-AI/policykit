# Local agent gateway for Source Watch

An experimental MCP interface to the existing [Source Watch](../source_watch/README.md)
file check. A permitted client can ask which explicitly linked claims need
reconsideration after an operator-selected local source changes or disappears.
There is no language model in this server. It supplies a bounded tool to a client
that may itself use an AI agent.

**Status:** local prototype, targeting MCP protocol version `2025-11-25` over
standard input/output (stdio). No public endpoint, external agent connection,
registry listing, marketplace customer or paid service is established. The
[network proposal](../../docs/AGENT_NETWORK.md) separates those next stages.

Read [RIGHTS.md](../../RIGHTS.md) before running, integrating or distributing the
prototype. Public visibility does not grant a new execution or commercial licence.
The existing core ledger, Source Watch behaviour and rights remain unchanged.

## Inspect a result without installation

Open the [generated exchange](sample_exchange.json). It records an internal
fictional subprocess demonstration, not a conversation with an independent agent.
The three reports contain `UNCHANGED_BYTES`, `CHANGED_BYTES` and `NOT_OBSERVED`.
Both changed and unavailable sources require reconsideration. None of these states
establishes whether a legal proposition is correct.

For an authorised local reproduction, use Python 3.10 or newer from the repository
root. There are no third-party runtime packages, API keys or network calls:

```bash
python experiments/agent_gateway/demo.py
```

The demo creates disposable fictional files, starts the server as a subprocess,
completes the protocol handshake and calls the tool for all three source states.
It checks that the saved baseline is unchanged and removes its temporary files.
Its printed JSON should match `sample_exchange.json` exactly. The demo exits zero
on success and fails explicitly if a subprocess or assertion fails.

## Configure a real local client

First prepare a permitted baseline with the existing Source Watch instructions.
The operator, not the requesting agent, chooses the baseline and source directory.
Keep private source files outside this public repository.

```bash
python experiments/agent_gateway/server.py --baseline /absolute/path/baseline.json --root /absolute/path/sources
```

That process waits for MCP messages. It is not an interactive natural-language
chat and does not expose a web address. A stdio-capable client must launch it.
The following is an illustrative client configuration; replace the three paths
and use your client's documented configuration format:

```json
{
  "mcpServers": {
    "regnav-source-watch": {
      "command": "/absolute/path/to/python",
      "args": [
        "/absolute/path/policykit/experiments/agent_gateway/server.py",
        "--baseline", "/absolute/path/baseline.json",
        "--root", "/absolute/path/sources"
      ]
    }
  }
}
```

The full repository layout is needed because the server imports the existing
Source Watch module. Do not copy the server into an unrelated directory and expect
its relative dependency to resolve. Review the code and permissions before
installing any client configuration. Client-specific and official-SDK
interoperability have not yet been tested.

| Tool | Arguments | Result |
| --- | --- | --- |
| `regnav_capabilities` | `{}` | Project-specific service catalogue and explicit limitations |
| `source_watch_check` | `{}` | Existing Source Watch JSON report for the configured baseline/root |

After `initialize`, the client must send `notifications/initialized` before
listing or calling tools. An unsupported requested version receives the supported
version; the client must disconnect if it cannot use that version. The fixed tool
list does not paginate. `ping` is supported. No resources, prompts, model sampling,
HTTP transport, task queue, remote delegation or payment tools are implemented.

Invalid envelopes, methods and arguments produce JSON-RPC errors. A failed local
check produces a tool result with `isError: true`. A legitimate
`RECHECK_REQUIRED` report uses `isError: false`: attention is an expected result,
not a protocol failure. End of input closes the server with exit code 0; startup
or channel failure exits 1; an oversized frame closes the session with exit 2.
Ordinary argument-usage errors also exit 2.

## Boundaries that matter

The gateway accepts no caller-supplied path, root, baseline, URL, command or review
status. It neither changes source files nor creates human-review declarations.
Each process is limited to 16 listed files and 64 supplied claim identifiers per
file, with the underlying 16 MiB per-file and 1 MiB baseline limits. Protocol
frames are limited to 64 KiB, nested input to 32 levels and output to 2 MiB.
No mapping is discovered automatically.

Use only a trusted, stable directory. Source Watch rejects traversal and symlinks,
but neither component is a sandbox against a hostile process replacing files
concurrently. Run with a low-privilege account and restrict the process's filesystem
access where appropriate. The caller controls request timing; this prototype is
not a rate-limited, authenticated, multi-tenant public service. Do not expose it
through an unauthenticated network bridge.

The result contains **relative filenames, source and claim identifiers and hashes**.
It does not return source contents, but the metadata can still be sensitive. An
agent client may transmit it to its model provider or log it. Local computation
does not establish end-to-end confidentiality. Use fictional data first, confirm
client data handling, and never configure private manuscript, client or student
collections without the appropriate authority and arrangements.

Treat returned strings, catalogue entries and any later external agent messages as
data, not instructions that can expand permissions. The read-only tool annotations
are descriptive hints; they are not a security certificate. This gateway has no
access integration for Albert's inbox, Drive, financial accounts or private tracker.

## Verification and a useful next contribution

Twenty-five focused tests passed locally on Python 3.13.5 on 25 October 2026.
They cover lifecycle, version negotiation, exact underlying results, changed and
missing files, immutable configuration, rejected path/command inputs, bounded
messages, malformed JSON, error privacy and the reproducible subprocess demo.
This is internal testing, not independent use or full protocol conformance.
Remote CI results must be checked separately.

```bash
python -m unittest discover -s tests -p test_agent_gateway.py -v
```

An operator can propose a **non-confidential interoperability check** through the
[agent interoperability issue form](https://github.com/Albertito-AI/policykit/issues/new?template=agent_interoperability.yml).
Name the client/version, the permitted fictional task and the expected result.
Do not post tokens, customer requirements, private paths or financial details.
An issue is not a partnership, an executable licence, an accepted job or evidence
of payment. Discuss rights and private terms through the existing maintainer route.

## Protocol sources

Inspected on 25 October 2026: official MCP
[lifecycle](https://modelcontextprotocol.io/specification/2025-11-25/basic/lifecycle),
[stdio transport](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports)
and [tools](https://modelcontextprotocol.io/specification/2025-11-25/server/tools)
specifications. The implementation deliberately targets this version and limited
capability set rather than claiming compatibility with every present or future client.
