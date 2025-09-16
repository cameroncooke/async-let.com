---
title: 'Streamlining MCP distribution with npm, npx, and mise'
pubDatetime: 2025-04-09T00:00:00.000Z
ogImage: ./npm-npx-mise/packages.png
tags:
  - npm
  - npx
  - mise
  - Node.js
  - Distribution
description: 'How to use npm, npx, and mise to run Node.js packages without installation'
---
![Streamlining MCP distribution with npm, npx, and mise](./npm-npx-mise/packages.png)
Distributing developer tools can be a challenge. How do you make your tools accessible without requiring users to jump through complex installation hoops? I recently faced this exact problem with my  project [XcodeBuild MCP](/posts/xcodebuild-mcp/) and discovered an elegant solution thanks to a suggestion from [@pepicrft](https://twitter.com/pepicrft).

## npm package

The first suggestion was submitting the package to the NPM registry. This was a no-brainer really, NPM (Node Package Manager) is the standard package manager for JavaScript and Node.js, with millions of packages that developers use daily. By publishing XcodeBuildMCP to NPM, I've made it accessible to anyone with a simple command.

Publishing to NPM means:

1. The package is discoverable through the NPM registry
2. Users can install specific versions
3. Dependencies are automatically managed
4. Updates can be easily distributed

If you're curious about the process, publishing to NPM was straightforward:

```bash
npm login
npm publish
```
And just like that, XcodeBuildMCP became available to the wider Node.js ecosystem.

## mise and npx

While publishing to NPM solved the distribution problem, users could still encounter friction when installing XcodeBuildMCP as they would need to install Node if they didn't have it already, clone the repo, install then dependencies and build the project. 

There are a couple of issues with this, why should an end-user who most likely isn't a node developer need to worry about Node.js versions or installation? Ideally, users shouldn't need to worry about node just to use a tool occasionally.

### What is npx?

npx is a tool that comes bundled with npm. It lets you run a package without installing. For my XcodeBuildMCP server, this was perfect, users could run it without downloading the sources and building it themselves.

With npx, when someone wants to use my XcodeBuildMCP tool, they just run a simple command and npx handles downloading the package, running it, and then cleaning everything up afterward, nice.

It's as simple as:

```bash
npx xcodebuildmcp
```
While this is a great solution for running my server, it still requires the user to have Node.js installed and this is where mise comes to the rescue.

### What is mise?

mise is like a Swiss Army knife for developers that solves the "but it works on my machine" problem. Instead of struggling with different versions of Node, Python, or Ruby, mise lets you run any tool from any ecosystem without installing it permanently on your system.

Installing mise is simple:

```bash
brew install mise
```
Where mise really shined was its `x` command. This was the final piece of the puzzle for XcodeBuildMCP. With this approach, users don't even need to have Node.js installed at all! Mise handles everything, it downloads the right version of Node.js temporarily, runs my package, and cleans up afterward!

Running the command is simple:

```bash
mise x npm:xcodebuildmcp@latest
```
### Putting it all together

We can now use mise and npm together to run XcodeBuildMCP without needing to install Node.js, download sources or build the package.

Configuring an MCP client (like Cursor, Claude Desktop, or Windsurf) to use XcodeBuildMCP is now as simple as (assuming they have mise installed):

```json
{
  "mcpServers": {
    "XcodeBuildMCP": {
      "command": "mise",
      "args": [
        "x",
        "npm:xcodebuildmcp@latest",
        "--",
        "xcodebuildmcp"
      ]
    }
  }
}
```
## Wrapping Up

I'm really happy with how this all turned out for XcodeBuildMCP. What started as a simple suggestion from [@pepicrft](https://twitter.com/pepicrft) has made the tool so much easier for people to use. The original version required users to clone the repo, install dependencies, and build the project, now they can be up and running with only one dependency `mise`.

I've learned that distribution is just as important as the tool itself. You can build the most amazing tool in the world, but if people can't easily use it, what's the point?

Thanks again to [@pepicrft](https://twitter.com/pepicrft) for this excellent suggestion.
