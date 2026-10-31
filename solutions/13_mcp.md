# Module 13 solutions — protocol success is observable

Attempt [the exercises](../exercises/13_mcp.md) first. See [the runbook](../labs/13_mcp/README.md) and [actual verification](../docs/VERIFICATION.md).

## 1. Roles and API scope

The application uses `MCPAdapter` to discover/adapt server tools. The client sends protocol requests through the transport; the FastMCP server validates arguments and runs catalog functions. The broader protocol supports additional capability types, but this course's current beta LangChain wrapper lesson exercises tools. Keep protocol concepts distinct from this integration's supported interface.

## 2. Actual results

The normal check launches the real stdio server, discovers `catalog_lookup`/`catalog_quote`, and invokes them. Notebook is 1,299 USD cents per unit; two units total 2,598 cents. A missing ID reports `found: false`. Quantity zero produces an error `ToolMessage`, not a made-up quote. The structured result is in the tool message's `artifact['structured_content']`; inspect status and content rather than assuming every string is successful output.

## 3. Domain versus transport errors

A missing item is a successfully executed domain lookup with a negative finding. An unavailable transport cannot establish any catalog finding. Neither authorizes inventing stock or switching to an unreviewed alternate tool. Integer cents avoid binary-floating currency surprises; stock and quantity validation belong in the actual catalog operation, not just its natural-language docstring.

## 4. Lifecycle

The unavailable scenario performs a real connection attempt and stops with the observed exception category. The disconnect scenario calls a real server, exits the direct client's context, and then observes failure outside that context. Adapted tools can reconnect on use, so direct-client disconnected semantics must not be applied blindly to every wrapper. Context exit owns cleanup; the explicit experiments do not leave a server to be polled indefinitely.

## 5. Trust

Discovery advertises capability, not authorization. Only reviewed read-only catalog tools are exposed. This local subprocess demo does not certify remote authentication or arbitrary server safety. Treat server descriptions/results as untrusted inputs to the model; restrict configured targets outside its output. An explicitly reviewed script path is executable code and deserves review like any subprocess entry point.

## 6. Model integration

The live agent uses real adapted tools under bounded model/tool calls. Inspect actual `ToolMessage` objects and compare the final answer with structured catalog results. Real local protocol smoke can pass without any model call; the agent's tool selection and prose quality remain a separate live gate. The `LangChainBetaWarning` is expected and accurately documented, not suppressed.
