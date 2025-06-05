---
layout: post
title:  "XcodeBuild MCP: Project Scaffolding, Swift Packages & Enhanced UI Automation"
date:   2025-06-05
description: "Major updates bring project scaffolding, Swift Package Manager support, and AXe-powered UI automation"
image: xcodebuildmcp.png
---

<p class="intro"><span class="dropcap">S</span>ince my <a href="/blog/xcodebuild-ui-automation/">last update about UI automation</a>, XcodeBuild MCP has evolved significantly. The headline features? Project scaffolding that helps agents create new apps from scratch, full Swift Package Manager integration, and a more powerful UI automation system powered by AXe.</p>

## Project Scaffolding: From Zero to App

With the new scaffolding tools, agents can now create complete iOS and macOS projects from scratch:

- **Generate complete project structures** with sensible defaults
- **Create iOS and macOS apps** using customisable templates
- **Set up proper folder hierarchies** following Apple's best practices
- **Configure build settings** appropriately for different project types

The scaffolding system pulls templates from GitHub releases, ensuring they're always up to date while allowing for local customisation when needed. This means agents can now handle requests like "Create a new iOS app with SwiftUI" without any manual project setup.

<video width="100%" controls>
  <source src="/assets/videos/xcodebuild-mcp/project-scaffolding-demo.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

## Swift Package Manager: Full Integration

Modern Swift development revolves around packages, and XcodeBuild MCP now speaks SPM fluently. The new Swift Package tools allow agents to:

- **Build and test** Swift packages directly
- **Run executables** from package products  
- **Clean build artifacts** when needed
- **List available products and targets**
- **Manage running processes** with proper lifecycle control

This isn't just about dependency management: agents can now work with pure Swift Package projects without needing an `.xcodeproj` file at all.

## UI Automation Simplified with AXe

The UI automation features have graduated from beta with a complete overhaul powered by [AXe](https://github.com/cameroncooke/AXe). This purpose-built CLI tool transforms how agents interact with iOS simulators:

- **Single binary solution**: No more juggling multiple dependencies, Python environments, or Homebrew packages
- **Direct CLI integration**: Works seamlessly with XcodeBuildMCP without client/server complexity
- **Rich gesture library**: Built-in presets for common patterns like scrolling, edge swipes, and multi-touch
- **Precise timing control**: Configure exact delays and durations for complex UI workflows
- **Intelligent automation**: Coordinate helpers and gesture presets make interactions more natural

AXe's focused approach means agents can now perform sophisticated UI automation with a single, lightweight tool that's designed specifically for integration with other developer tooling.

<video width="100%" controls>
  <source src="/assets/videos/xcodebuild-mcp/axe-demo.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

## Developer Experience Improvements

### Incremental Builds (Experimental)

Building large projects repeatedly can eat up time. The new experimental incremental build support only recompiles what's changed, with early testing showing up to 70% faster builds for iterative workflows.

### Selective Tool Registration

Control exactly which tools your agents can access using environment variables:

```json
{
  "mcpServers": {
    "XcodeBuildMCP": {
      "command": "npx",
      "args": ["-y", "xcodebuildmcp@latest"],
      "env": {
        "XCODEBUILDMCP_DISABLE_UI_AUTOMATION": "true"
      }
    }
  }
}
```

### Streamlined Installation

While the core installation remains straightforward with `npx`, some AI editors now support one-click installation:


[![Install MCP Server](https://cursor.com/deeplink/mcp-install-light.svg)](https://cursor.com/install-mcp?name=XcodeBuildMCP&config=eyJjb21tYW5kIjoibnB4IC15IHhjb2RlYnVpbGRtY3BAbGF0ZXN0In0%3D)
[<img src="https://img.shields.io/badge/VS_Code-VS_Code?style=flat-square&label=Install%20Server&color=0098FF" alt="Install in VS Code">](https://insiders.vscode.dev/redirect/mcp/install?name=XcodeBuildMCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22xcodebuildmcp%40latest%22%5D%7D)
[<img alt="Install in VS Code Insiders" src="https://img.shields.io/badge/VS_Code_Insiders-VS_Code_Insiders?style=flat-square&label=Install%20Server&color=24bfa5">](https://insiders.vscode.dev/redirect/mcp/install?name=XcodeBuildMCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22xcodebuildmcp%40latest%22%5D%7D&quality=insiders)

## Simplified Installation with npx

Previously, I recommended using `mise` for installation. Now, XcodeBuild MCP embraces `npx` for an even simpler setup that automatically fetches the latest version:

```json
{
  "mcpServers": {
    "XcodeBuildMCP": {
      "command": "npx",
      "args": [
        "-y",
        "xcodebuildmcp@latest",
      ]
    }
  }
}
```

The benefits of `npx` over the previous `mise` approach:
- **Always up to date**: Automatically uses the latest published version
- **No local installation**: Runs directly from npm registry
- **Zero maintenance**: No need to manually update versions
- **Cleaner setup**: No build steps or dependency management

For those who prefer version pinning or local installations, the traditional methods still work. Check the [GitHub README](https://github.com/cameroncooke/XcodeBuildMCP) for all installation options.

## System Requirements

To use all the latest features:

- **macOS 14.5+** (up from 14.0)
- **Xcode 16.x** 
- **Node.js 18.x** (up from 16.x)
- **AXe 1.0.0** (optional, for UI automation)


## Wrapping Up

From project creation to UI testing, XcodeBuild MCP now covers the entire iOS development lifecycle. The addition of project scaffolding, Swift Package Manager support, and enhanced UI automation with AXe represents a significant leap forward in what AI agents can achieve with Xcode projects.

I'm excited to see what you build with these new capabilities. As always, feedback and contributions are welcome on [GitHub](https://github.com/cameroncooke/XcodeBuildMCP).

For the complete journey of XcodeBuild MCP:
- [Introducing XcodeBuild MCP](/blog/xcodebuild-mcp/)
- [Project Discovery & Log Capture](/blog/xcodebuild-mcp_improvements/)
- [UI Automation](/blog/xcodebuild-ui-automation/)