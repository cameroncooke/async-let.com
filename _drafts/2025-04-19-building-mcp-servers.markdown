---
layout: post
title:  "Building MCP Servers"
date:   2025-04-19
description: "Learnings from building an MCP server"
---

<p class="intro"><span class="dropcap">B</span>uilding an MCP server seems straitforward enough but is actually tricker than expected. This article covers some of the learnings from building my XcodeBuild MCP server.</p>

## A short introduction to MCP servers

If you're new to MCP servers then they are essentially applications that can run either locally on your machine or via the internet on a web server or cloud hosting service and which expose their capabilities via a standardised interface that conforms to the Model Context Protocol (MCP) standard. MCP was created by Anthropic the company by the extreamly popular Clude AI assistant and the Sonnet 3.7 LLM which has proven to be a favouite of many developers.

At a basic level most MCP servers expose "tools" via a standardised `tools/list` end-point. The MCP client can then call the tools via the `tools/call` end-point providing the necessary parameters. The beauty of this is that the client doesn't need to know anything about the server or the tools it provides, it just needs to know how to call them.

## Building an MCP server

### Background

If you're not interested in why I build my own MCP server feel free to skip this section, if not then read on.

As an iOS developer I was keen to jump on the AI bandwagon, I grew increasinly frustraied by the lack of support for native Apple platform development from the major AI vendors. Everyone was raving about Cursor and Windsurf so naturally I wanted to join in the fun. So I installed Cursor and the official Swift VSCode extension but this was too limiting, I still had to jump back to Xcode for building, running, testing etc. Cursor was just an editor and I wanted the full IDE experience. Luckily I discovered the rather odly named extension Sweetpad by Yevhenii Hyzyla, this bridged most of the gaps between Xcode and Cursor and added build, run, debug and testing capabilities. While this was a decent solution for working on Xcode projects, the extension was limited to the IDE and not available to the AI agent capability.

#### Vibe Coding enters the room

As editors like Cursor, Windsurf and more recently Github Copilot amoung others added agenteic AI capabilities I stated to watch in envy endless "vibe coding" demos where entire web applications (albit basic MVPs) were built in one-shot and iterated on by the AI agent with very little input from a human. I quickly explored "vibe coding" existing and new iOS projects, most agents in popular IDEs can issue shell commands and therefore in theory build and run iOS projects, in my experience this was very hit or miss. Often the agent would halusionate or call outdated commands and the overall experience was rather frustraing. It was at this point I decided I would attmept to solve this problem by building my own MCP server.

### XcodeBuild MCP

