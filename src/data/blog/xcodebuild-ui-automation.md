---
title: 'XcodeBuild MCP: UI Automation is here!'
pubDatetime: 2025-04-28T00:00:00.000Z
ogImage: ./xcodebuild-ui-automation/xcodebuildmcp.png
tags:
  - iOS
  - UI Automation
  - Xcode
  - Agents
description: Taking agent-driven iOS development to the next level with UI Automation
---
![XcodeBuild MCP: UI Automation is here!](./xcodebuild-ui-automation/xcodebuildmcp.png)
What if AI agents could not only build your iOS apps, but also interact with them just like a real user? With the latest release of XcodeBuild MCP (v1.3.0), that's now a reality. I'm excited to introduce a suite of UI automation features in beta

## UI Automation: The Game-Changer

Until now, AI agents could build and launch your app in a simulator, but once running, they were essentially "blind" unable to see the UI, tap buttons, or check that everything worked as intended.

But that's all changed. With the new UI automation tools, agents can:

- **Tap** UI elements at specific coordinates
- **Swipe** to navigate your app
- **Long press** for contextual menus
- **Type text** into fields
- **Capture screenshots** to verify appearance
- **Analyse the accessibility hierarchy** to identify UI elements

These features close the loop, allowing agents to autonomously build, run, test, and verify iOS applications without human intervention.

## Screenshot Tool in Action

The new screenshot capability is particularly powerful. It allows agents to capture the current state of your app's UI and use that information to make informed decisions about what to do next.

![Using Cursor to build, install, and launch an app on the iOS simulator while capturing logs and screenshots at run-time.](https://github.com/user-attachments/assets/17300a18-f47a-428a-aad3-dc094859c1b2)

In the example above, you can see how an agent can build an app, run it in the simulator, and capture both logs and screenshots to provide comprehensive feedback.

## Getting Started with UI Automation

To enable these features, you'll need to install Facebook's idb_companion, which acts as a bridge between XcodeBuild MCP and the iOS simulator. It provides the underlying automation capabilities, allowing agents to interact with your app’s UI just like a person would.

```bash
brew tap facebook/fb
brew install idb-companion
```
Once installed, configure your MCP client to use version 1.3.0 or later of XcodeBuild MCP:

```json
{
  "mcpServers": {
    "XcodeBuildMCP": {
      "command": "mise",
      "args": [
        "x",
        "npm:xcodebuildmcp@1.3.0",
        "--",
        "xcodebuildmcp"
      ]
    }
  }
}
```
> **Note:** These UI automation features are currently in beta. While they're already incredibly useful, you might spot the odd rough edge. If you do, please report it in the [issue tracker](https://github.com/cameroncooke/XcodeBuildMCP/issues).

## Wrapping Up

The addition of UI automation and screenshot capabilities to XcodeBuild MCP represents a significant step forward in agent-driven iOS development. By enabling agents to interact with your app just like a human would, we're removing yet another barrier to truly autonomous development workflows.

I would love to hear your thoughts and feedback via my socials or raise an issue on GitHub if you have found a bug or just want to suggest an improvement.

If you want to read my original post for a full background on what XcodeBuild MCP is or how to get started, check it out [here](/blog/xcodebuild-mcp/) or if you just want to try it out, you can get it from [GitHub](https://github.com/cameroncooke/XcodeBuildMCP).
