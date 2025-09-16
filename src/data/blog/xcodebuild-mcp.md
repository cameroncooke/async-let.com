---
title: Introducing XcodeBuild MCP
pubDatetime: 2025-03-31T00:00:00.000Z
ogImage: ./xcodebuild-mcp/xcodebuildmcp.png
tags:
  - Xcode
  - iOS
  - MCP
  - XcodeBuild MCP
description: A project I've been working on to make Xcode automation easier
---
![Introducing XcodeBuild MCP](./xcodebuild-mcp/xcodebuildmcp.png)
## What is XcodeBuild MCP?

XcodeBuild MCP is a Model Context Protocol (MCP) server I created to connect AI agents with Xcode projects. I wanted a standardised interface for programmatic interactions that would make my own development workflow smoother.

### What It Does

- **Xcode Project Management**: Handles build operations for macOS, iOS simulator, and device targets. You can list schemes and check build settings through a simple interface.
- **Simulator Management**: Makes it easy to control iOS simulators programmatically. Boot them up, open them, and deploy apps without manual steps.
- **App Utilities**: Extracts bundle identifiers and launches applications on simulators and macOS with minimal fuss.

### How do I get it?

You can get it from [GitHub](https://github.com/cameroncooke/XcodeBuildMCP).

### How do I use it?

Getting started is straightforward. You'll need Node.js (v16 or later), npm, and Xcode command-line tools installed on your machine. Then:

1. Clone the repository from GitHub
2. Install the dependencies with `npm install`
3. Build the project using `npm run build`

The beauty of it is that you don't need to run the server manually—MCP clients will handle this for you. If you're using Windsurf, Cursor, or Clude Desktop, simply edit or create a new MCP server configuration file pointing to your local build:

```json
{
  "mcpServers": {
    "XcodeBuildMCP": {
      "command": "node",
      "args": [
        "/path_to/XcodeBuildMCP/build/index.js"
      ]
    }
  }
}
```
Once configured, your AI assistant will have access to all the Xcode-related tools, allowing it to build projects, manage simulators, and run apps!

### Why I Built It

I grew frustrated watching AI agents struggle with outdated or incorrect command-line invocations when interacting with Xcode projects. This tool addresses this challenge by providing a set of specialised tools that AI can utilise for building and deploying to simulators and devices.

The superpower of this tool is how it enables AI agents to intelligently read build output and automatically correct issues without constant manual intervention.

I hope you find it as useful, and I'd love to hear your thoughts and feedback via my socials or raise an issue on GitHub if you have found a bug or just want to suggest an improvement.

### Update 14 April 2025

I've been working on a few improvements to XcodeBuild MCP since I wrote this article, read about the new project discovery and run-time log capture features [here](/posts/xcodebuild-mcp_improvements/).

### Update 28 April 2025

Read about the new UI automation and screenshot features [here](/posts/xcodebuild-ui-automation/).

### Update 5 June 2025

Major update! XcodeBuild MCP now includes project scaffolding, Swift Package Manager support, and enhanced UI automation with AXe. Read about these improvements [here](/posts/xcodebuild-mcp-scaffolding-spm/).
