---
title: 'Introducing MCPLI: Turn MCP servers into first class CLIs'
pubDatetime: 2025-09-04T00:00:00.000Z
ogImage: ./introducing-mcpli/mcpli.png
tags:
  - MCP
  - CLI
  - Tooling
  - Agents
description: >-
  Announcing MCPLI: a CLI that turns MCP servers into first class command line
  tools, boosts composability, and cuts token usage by up to 95%.
---
![Introducing MCPLI: Turn MCP servers into first class CLIs](./introducing-mcpli/mcpli.png)
The community has been actively debating MCP versus CLI workflows for agent tooling. Many developers have raised valid concerns about context bloat and attention dilution when clients eagerly load large tool schemas. Others appreciate the magical, fully empowered agent experience that MCP servers provide. This has created what feels like a false choice: accept context overhead for rich capabilities, or abandon MCP entirely for leaner CLI approaches. MCPLI exists to bridge that gap.

## Why I built it

In my earlier post on the debate I argued for choosing the right tool for your context rather than adopting a blanket position. See: [My Take on the MCP vs CLI Debate](/posts/my-take-on-the-mcp-verses-cli-debate/). I continue to defend MCP servers: they are valuable for interoperability between AI agents and external tools, and for building safe, stateful workflows. At the same time, I acknowledge that depending on the use case and client behaviour, they can contribute to context bloat and degraded performance through attention dilution.

### The problem

- **Context and attention**: Loading multiple servers with rich schemas can consume significant tokens before the assistant even begins reasoning. This reduces the headroom available for problem solving and increases the chances of distraction by irrelevant tool detail.
- **Composition versus state**: Pure CLI workflows are wonderfully composable and transparent, yet they lose the long‑lived state and guardrails that many MCP servers provide out of the box.

### The best of both worlds

If you are willing to forgo some ergonomics and explicitly instruct your agent how to interface with external tools, you can avoid loading large tool schemas while retaining a predictable interface. MCPLI turns any existing stdio MCP server into a first class, stateful CLI where tools map to CLI command primitives. You keep the protocol’s benefits (capabilities, state, safety) and gain the CLI’s strengths (composition, predictability, and easy piping).

### Related reading that shaped this work

The conversation has moved forward thanks to thoughtful critiques and experiments from others:

- Armin Ronacher on the cost of tool schemas and limited composition: [Tools: Code Is All You Need](https://lucumr.pocoo.org/2025/7/3/tools/)
- Peter Steinberger on agents being very good at calling CLIs: [Peekaboo 2.0](https://steipete.me/posts/2025/peekaboo-2-freeing-the-cli-from-its-mcp-shackles)

My experience building XcodeBuildMCP reinforced a further point: **state and safety matter**. Long‑lived, stateful operations with built‑in guardrails often separate robust workflows from fragile chains of ad‑hoc commands. MCPLI preserves that state via a persistent daemon while exposing a CLI surface optimised for agentic use.

## Research: token usage and reliability

I ran a controlled study of three assistant configurations to build and run an iOS Calculator app on an iPhone 16 Pro simulator. All three completed the task successfully. The difference was the token footprint required to get there.

- **MCP-only**: Total used 38,609 tokens
- **Comprehensive CLAUDE.md**: Total used 10,009 tokens
- **Curated CLAUDE.md**: Total used 1,865 tokens

**Key finding**: The curated approach used only 5% of the tokens compared to the MCP-only baseline, a reduction of up to 95.2%, while achieving the same outcome.

Breakdown from the study:

- **MCP-only**: Tool definitions 32,900, messages growth 5,709, total 38,609
- **Comprehensive CLAUDE.md**: Tool definitions 7,500, messages growth 2,509, total 10,009
- **Curated CLAUDE.md**: Tool definitions 156, messages growth 1,709, total 1,865

You can read the full report and see the data tables in the research repository.

## Watch the sessions

Each configuration was recorded. You can play the videos directly below or open them in your browser.

### MCP-only session

<video width="100%" controls>
  <source src="/assets/videos/mcpli-research/mcp-only-session.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

### Comprehensive CLAUDE.md session

<video width="100%" controls>
  <source src="/assets/videos/mcpli-research/comprehensive-session.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

### Curated CLAUDE.md session

<video width="100%" controls>
  <source src="/assets/videos/mcpli-research/curated-session.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

## What is MCPLI?

MCPLI turns any stdio-based MCP server into a first class CLI. You run tools as commands, discover parameters with `--help`, and compose results with your usual shell utilities. Under the hood, MCPLI maintains a persistent daemon so repeated calls reuse the same server instance, preserving state and speed.

### Key capabilities

- **Zero setup**: Point MCPLI at any stdio MCP server and run.
- **Natural syntax**: Tools become commands you can chain in the shell.
- **Persistent daemon**: Reuse the same server instance for stateful workflows.
- **Auto-generated help**: Discover tools and parameters with standard help output.
- **Clean output**: Friendly JSON by default, raw mode for debugging when needed.

### Composability in action

This MCP weather server outputs structured JSON that works seamlessly with standard shell tools:

```bash
# First, see the raw tool output
$ mcpli get-weather --location "San Francisco" -- node weather-server.js
{
  "location": "San Francisco, California, United States",
  "temperature": "63°F",
  "feels_like": "64°F",
  "humidity": "86%",
  "condition": "Partly cloudy"
}

# Extract specific data with jq
$ mcpli get-weather --location "San Francisco" -- node weather-server.js | jq -r '.temperature'
63°F

# Filter and process results
$ mcpli get-weather --location "London" -- node weather-server.js | jq '.condition' | grep -i cloudy
"Partly cloudy"

# Chain with other tools for formatted output
$ mcpli get-weather --location "NYC" -- node weather-server.js | jq -r '.temperature' | awk '{print "Current temp: " $1}'
Current temp: 67°F
```
MCPLI returns whatever the MCP server outputs - text, JSON, or other formats. In the weather server example above, the server happens to return JSON from an API, making it perfect for `jq` processing. This means you can integrate any MCP tool into existing shell scripts and automation workflows.

## Getting started

Keep it simple to begin with. Install, discover tools, and run a command. See the repository for full documentation and advanced features.

```bash
# Install globally
npm install -g mcpli

# Discover tools from an MCP server
mcpli --help -- <mcp-server-command> [args...]

# Run a tool
mcpli <tool> [options] -- <mcp-server-command> [args...]
```
## Learn more

- MCPLI on GitHub: [cameroncooke/mcpli](https://github.com/cameroncooke/mcpli)
- Research repository with raw data and artefacts: [cameroncooke/mcpli-context-research](https://github.com/cameroncooke/mcpli-context-research)

If you try MCPLI in your own workflows, I would love to hear how it goes and what you would like to see next.

## Closing

My stance on this debate remains unchanged from my earlier article: use what works for your context. MCP servers can deliver an almost magical experience where the agent is fully empowered to make its own decisions with state and guardrails, and that value should not be underestimated. Even though MCPs, including my XcodeBuildMCP, can use significant tokens, the benefits of a fully agentic workflow often justify that cost.

MCPLI simply offers those who prefer a leaner context footprint another option without abandoning the benefits of MCP entirely. It is not a replacement for MCP servers, but rather an additional tool in the toolkit for different use cases and preferences.
