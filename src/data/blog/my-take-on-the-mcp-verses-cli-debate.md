---
title: My Take on the MCP vs CLI Debate
pubDatetime: 2025-07-05T00:00:00.000Z
ogImage: ./my-take-on-the-mcp-verses-cli-debate/mcp-vs-cli.png
tags:
  - MCP
  - CLI
  - Agents
  - Opinion
description: >-
  Personal thoughts on the growing CLI movement and why I still see value in
  MCPs for certain use cases
---
![My Take on the MCP vs CLI Debate](./my-take-on-the-mcp-verses-cli-debate/mcp-vs-cli.png)
When I first started building my XcodeBuildMCP server, it was simply to solve my own frustrations with getting AI agents to work reliably with Xcode projects. What I did not expect was how much it would teach me about the broader questions around AI agent tooling.

The response has been incredible: over 1900 stars on GitHub (at time of writing) and countless messages from developers using it as their first experience with Swift development. Meanwhile, the community has been actively discussing the benefits of MCP servers versus using CLI tools directly - a debate that my experience building and maintaining an MCP server has given me some perspective on.


## Table of contents

There has been some interesting discussion lately about the best approaches for AI agent tooling. A growing number of developers are advocating for CLIs over the Model Context Protocol (MCP), citing performance, simplicity, and reliability concerns. Having built and used both approaches extensively, I wanted to share what I have learned from this experience.

## TL;DR

CLIs work well for expert developers who want control and transparency, while MCPs excel at complex workflows, safety constraints, and lowering barriers for less experienced users. Context management varies by implementation - MCPs can both consume and save context. Not all clients have shell access, limiting CLI-only approaches.

**My take:** There's no universal answer. Choose the right tool for your context rather than adopting a blanket approach.


## Understanding the Debate

To understand this discussion, it helps to know what we are comparing. The Model Context Protocol (MCP) is an open-source protocol (originally developed by Anthropic) for connecting AI assistants to external tools and data sources. MCP servers expose specific capabilities (accessing databases,  accessing and managing external resources as well calling external tools) through a standardised interface that AI agents can discover and use automatically.

The alternative approach involves using traditional Command-Line Interface (CLI) tools. Instead of purpose-built MCP servers, developers guide AI agents to use existing command-line utilities like `git`, `npm`, `docker`, or custom scripts. The AI generates and executes shell commands to accomplish tasks.

The debate centres on which approach is more effective for agentic AI workflows. Should we build specialised MCP servers that encapsulate domain expertise, or should we rely on the vast ecosystem of existing CLI tools that developers already know and trust?

## Where I Agree with the CLI Proponents

When I read Armin Ronacher's analysis, it was genuinely thought-provoking. He makes several compelling points that I largely agree with. Performance is a real concern. As Armin Ronacher demonstrates in his analysis, MCP ["suffers from two major flaws"](https://lucumr.pocoo.org/2025/7/3/tools/): it is not truly composable and it "demands too much context". His experiment showing that the GitHub CLI (`gh`) "consumed far less context and got to the result quicker than the GitHub MCP" is hard to argue with.

The debugging issue is also spot-on. When a CLI command fails, you can see exactly what went wrong. When an MCP call fails, it can be "incredibly hard to debug" as Armin Ronacher notes. This opacity is genuinely frustrating.

However, I believe many of these debugging issues can be solved with better tooling - it is one of the areas I am actively focusing on. I have built an MCP server called [Reloaderoo](https://github.com/cameroncooke/reloaderoo) that allows AI agents to create a proxy to your in-development MCP server with an added restart tool. This lets agents work on server sources and restart them autonomously without requiring users to close their client software for a new server instance. I am also working on an inspection mode that will turn it into a debugging tool, allowing agents to inspect an MCP server's resources, tools, and prompts and test them via simple tool calls. This should greatly reduce the debugging problems that Armin mentions.

Peter Steinberger's point that ["agents are really, really good at calling CLIs"](https://steipete.me/posts/2025/peekaboo-2-freeing-the-cli-from-its-mcp-shackles) resonates with my experience too. For many straightforward tasks, asking an AI to generate a shell script or run a few commands is often the most efficient approach.

These are not frivolous complaints. They come from experienced developers who have genuinely tried both approaches and found CLIs more practical for their use cases.

## Where I See Things Differently

While I agree with many of the criticisms, my experience building an MCP server has shown me some areas where I think the picture is more nuanced.

### The "Context Bloat" of CLIs is a Hidden Cost

The idea that CLIs are entirely context-free is not quite accurate. For an agent to use any non-trivial CLI *reliably*, you must provide it with some context. Peter Steinberger admits this himself in his post about his CLI tool, Peekaboo; for an agent to use it, the user must add a note in their project's `CLAUDE.md` or instructions that "peekaboo is available for screenshots".

But let me be honest here: a single line like "peekaboo is available" is definitely lighter than loading an entire MCP server. The context cost really depends on the specific MCP server, the number of tools it exposes, the complexity of tool descriptions, and how well the client manages context. This varies considerably between clients and implementations, and I believe this can improve over time.

> I think much of the context bloat issue comes down to client implementation rather than the protocol itself.

CLI proponents are absolutely right to be frustrated with clients that load every available tool. However, I have found that clients like VSCode, which allow project-level configuration, solve this problem quite elegantly. The issue may be less about MCP and more about the current state of the tooling ecosystem.

### Redefining Composition: The Power of Curated Workflows

Armin Ronacher is absolutely correct that MCP "is not truly composable" in the classic Unix-pipe sense. I will concede this point entirely. However, I have found that for complex domains, there is value in a different kind of composition: **pre-composed, expert-designed workflows**.

This insight came from my own frustration with CLI-based approaches. I was seeing issues with tool calling and the agent's ability to construct correct and up-to-date CLI calls for Apple tools. The AI would often make incorrect assumptions about command syntax or use outdated approaches. I created the MCP server to solve these reliability issues by providing a curated, domain-specific interface.

My XcodeBuildMCP, for example, has a single `buildAndRun` tool that encapsulates dozens of steps an iOS developer would typically take. While an AI could potentially string together raw CLI calls to achieve the same result, in practice I have found this approach to be more reliable. The expert knowledge is baked into the tool itself, rather than requiring the AI to reinvent the workflow each time.

### Different Tools for Different Contexts

Peter Steinberger is right that "agents are really, really good at calling CLIs". For simple, stateless tasks, I completely agree. However, I have found that for more complex operations, there are some interesting trade-offs to consider.

**Purpose-Built for Agents:** CLI tools are designed for human users and therefore have a broader scope and more general-purpose interfaces. MCP servers can be specifically designed for AI agent workflows, optimising for the kinds of operations and data that agents commonly need.

**Data Exchange:** A CLI outputs raw text that often requires parsing and interpretation. My MCP server, for example, parses thousands of lines of Xcode build output and returns a clean, structured object: `{"errors": [...], "warnings": [...]}`. This preprocessing saves the agent from having to parse complex output formats and, importantly, prevents the raw CLI output from bloating the context window with irrelevant information.

**Workflow Integration:** MCPs can encapsulate entire workflows that would require multiple CLI calls and coordination. Rather than an agent having to orchestrate several commands and handle edge cases, the MCP server can provide a single, reliable operation that handles the complexity internally.

**Stateful Operations:** One of the most significant advantages is that MCP servers are long-running and stateful. In XcodeBuildMCP, I use this extensively: managing running processes that can be stopped and started on demand, capturing logs into memory rather than expensive I/O operations, and maintaining context between operations. A CLI-based solution would need to rely on file I/O and process coordination, which is both slower and more complex to manage reliably.

**Client Independence:** An important consideration that often gets overlooked is that not all MCP clients have built-in shell access. While most coding editors do provide shell tools, it is not a requirement of the MCP specification. This means that CLI-based approaches may simply not be available in some client environments, whereas MCP servers can work universally across any compliant client. It is worth noting that most proponents of CLI approaches are discussing this in the context of coding environments specifically, but we cannot dismiss MCP servers broadly without considering the wider range of potential client environments.

A CLI is a tool designed for a human in a shell. An MCP is a protocol designed for an AI agent in a client.

### Safety and Guardrails: The Hidden Risk

> One aspect that is often overlooked in this debate is safety. Giving an AI agent unrestricted access to your shell can be genuinely dangerous.

I learned this the hard way when I first started experimenting with AI agents. I watched an agent run commands that wiped out uncommitted changes because it thought a `git reset --hard` was the fastest way to clean up a failed build. That experience shaped how I designed XcodeBuildMCP: I wanted it to be impossible for an agent to accidentally destroy someone's work.

An agent might run destructive git commands, attempt to modify system permissions when it gets stuck, or try to edit system configuration files. These are not theoretical risks. They are real possibilities when an AI has broad CLI access.

CLI tools are generally designed for interactive human use and therefore tend to be more abstract and powerful. This flexibility becomes a liability when an AI agent is trying to achieve a specific goal and chooses the most direct path, even if it is clearly the wrong option.

A well-designed MCP server, by contrast, is domain-specific and curated. It can include built-in guardrails, validation, and safety constraints that prevent dangerous operations while still achieving the intended workflow. My XcodeBuildMCP, for example, cannot accidentally destroy your project or modify system settings—it is constrained to safe build and development operations.

With CLIs, you might need to create extensive rules files specifying "do not use these commands" or "do not do that." With MCPs, the safety constraints are built into the tool itself by design.

## Real-World Impact: Why It Matters

The success of XcodeBuildMCP genuinely surprised me. I built it to solve my own frustrations with getting AI agents to work reliably with Xcode projects. The fact that it has helped thousands of developers (many taking their first steps into iOS development) tells me there is something valuable here that goes beyond the technical arguments.

> What strikes me most is how it has lowered the barrier to entry for non-app developers to try building apps, prototypes, or Swift concepts.

When people tell me they built their first Swift app using an AI agent and my MCP server, that feels different from someone running a clever shell script. It feels like we lowered a barrier that existed before.

Many people have told me it helped them learn iOS development in a way that felt approachable and immediate. I do not think this same impact would have occurred with a CLI-based approach. The success was not just about the technical capabilities, but about providing a dedicated, workflow-based tool that people could discover and use without needing to understand the underlying complexity of Xcode's build system.

## The Broader Picture: Protocol Capabilities and Use Cases

It is worth stepping back to consider what we are really comparing. CLIs are fundamentally command-line tools designed for human use, whereas MCPs are designed specifically for agentic tooling. The MCP protocol supports much more than just tool execution: it includes resources, prompts, completions, sampling, and roots. Most clients do not support these broader features yet, but VSCode is an example of a client that supports the entire protocol, which opens up possibilities that would be near impossible with CLI tools alone.

Features like sampling and prompts would be extremely difficult to implement effectively through CLI interfaces without additional effort on the part of the user. I think MCPs still need time to mature, and dismissing them entirely because current implementations have issues seems short-sighted.

The reality is that not all MCPs are created equal. Some, like the GitHub MCP, genuinely do not add much value over the well-established CLI tool (`gh`), which is already likely baked into most models' training data. In such cases, the MCP does indeed just pollute context without benefit.

However, there are thousands of MCPs with varying levels of value. The debate is often narrowly focused on coding, but agentic AI will be used in every domain. An agent booking travel or managing inventory will not use CLIs. It will use tools exposed via a standardised protocol—exactly what MCP provides.

## There Is No Right Answer

Building XcodeBuildMCP has been a journey of discovery. I started with assumptions about what developers needed, learned from real usage patterns, and adjusted course multiple times. What I have learned is that there is no universal right answer here.

> After considering both sides of this debate, I have come to believe there is no universal right or wrong approach here.

Some developers will always prefer the control and transparency of CLIs. They want to see exactly what commands are running and have the flexibility to modify them. That approach works brilliantly for many use cases, and I completely understand why experienced developers gravitate towards it.

But I have also seen something else: developers who were intimidated by iOS development suddenly building apps because the complexity was hidden behind a well-designed MCP server. Watching someone create their first Swift application with the help of an AI agent - that convinced me we are onto something valuable.

Advanced users will likely use a combination of strategies anyway. They will craft elegant CLI workflows, write custom scripts, and maintain detailed rules files to guide their AI agents. They have the expertise to verify generated code and prefer the transparency that CLIs provide.

For junior developers, users new to software engineering, or those working in unfamiliar domains, MCPs may offer a more approachable path. The barrier-lowering effect I have observed with my XcodeBuildMCP (where non-iOS developers can suddenly build Swift applications) suggests that MCPs can democratise access to complex toolchains in ways that raw CLIs cannot.

CLI proponents have raised important points about performance and complexity that the MCP community should take seriously. Equally, the MCP ecosystem continues to evolve and address these concerns.

The real win is not one approach defeating the other. It is having both options available, allowing developers to choose what works best for their expertise level, workflow, and comfort zone.

<h4>References</h4>

Ronacher, Armin. "Tools: Code Is All You Need." *Lucumr.pocoo.org*, 3 July 2025. [https://lucumr.pocoo.org/2025/7/3/tools/](https://lucumr.pocoo.org/2025/7/3/tools/)

Steinberger, Peter. "Peekaboo 2.0 – Free the CLI from its MCP shackles." *Steipete.me*, 2 July 2025. [https://steipete.me/posts/2025/peekaboo-2-freeing-the-cli-from-its-mcp-shackles](https://steipete.me/posts/2025/peekaboo-2-freeing-the-cli-from-its-mcp-shackles)

Odendahl, Manuel. "MCPs are Boring (or: Why we are losing the Sparkle of LLMs)." *YouTube*, uploaded by AI Engineer, 2025. [https://www.youtube.com/watch?v=J3oJqan2Gv8](https://www.youtube.com/watch?v=J3oJqan2Gv8)
