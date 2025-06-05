# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Development
- **Start development server**: `bundle exec jekyll serve -w` (serves locally on port 4000 with auto-reload)
- **Install dependencies**: `bundle install` (required after cloning or when Gemfile changes)

### Deployment
- Deployment is automatic via GitHub Actions when pushing to the main branch
- GitHub Pages builds and deploys the site using the `jekyll-gh-pages.yml` workflow

## Blog Post Conventions

### Creating New Posts
1. Create file in `_posts/` with format: `YYYY-MM-DD-title-slug.markdown`
2. Required front matter:
```yaml
---
layout: post
title: "Post Title"
date: YYYY-MM-DD
description: "SEO-friendly description"
image: filename.png  # Optional, stored in /assets/img/
---
```

### Content Formatting
- First paragraph uses dropcap: `<p class="intro"><span class="dropcap">F</span>irst letter capitalized...</p>`
- Use UK English spelling
- Avoid em-dashes, use colons instead
- Links in HTML blocks must use `<a href="">` tags, not Markdown `[text](url)`
- Images: Store in `/assets/img/`
- Videos: Store in `/assets/videos/` organized by topic (e.g., `/assets/videos/xcodebuild-mcp/`)

### Writing Style & Tone

Maintain a knowledgeable, clear, and engaging human writing style suitable for an expert developer sharing knowledge, opinions, and project updates. 

**Core Principles:**
- **Human, not AI-clichéd**: Use natural language with varied sentence structure. Avoid overly formal constructions and AI-esque phrasing
- **No contractions**: Use "do not" instead of "don't", "it is" instead of "it's" for clarity and appropriate formality
- **Active voice**: Prefer active over passive voice where appropriate
- **Personal perspective**: Use "I" when sharing experiences or decisions (e.g., "I grew frustrated...", "I wanted...")

**Technical Writing:**
- **Clarity first**: Explain concepts directly and concisely, assuming fellow developers but not necessarily AI/MCP experts
- **Practical focus**: Frame explanations from a developer-centric perspective, relating back to building applications
- **Real benefits**: Focus on actual problems solved rather than theoretical concepts
- **Avoid hyperbole**: Do not oversell features or claim things were "highly requested" without evidence

**Engagement:**
- **Conversational but professional**: Address readers directly ("you", "let us discuss") while maintaining expertise
- **Measured enthusiasm**: Avoid excessive hype or overly casual language
- **Informative titles**: Use engaging section headers (e.g., "Making Models Device-Friendly" vs just "Quantization")
- **Community-oriented**: Encourage feedback via GitHub issues and social media

**Swift/iOS Context:**
- Frame concepts for Apple platform developers
- Use Swift/iOS terminology appropriately
- Include practical examples relevant to iOS/macOS development

### Linking Between Posts
- Use relative URLs: `/blog/post-slug/`
- Update related posts when creating new articles in a series

## Architecture

### Key Directories
- `_posts/`: Blog posts in Markdown
- `_scripts/`: Python script for auto-tweeting posts
- `assets/`: Images, videos, CSS, and JavaScript
- `_layouts/`: Post and default templates
- `_includes/`: Reusable components

### Automation
- **Twitter Integration**: Daily cron job (`tweet_new_post.yml`) automatically tweets new posts
- **Tweeted Links Log**: `_scripts/tweeted_links.log` tracks posted content (auto-committed)

### Theme Customization
- Based on "Long Haul" Jekyll theme
- Comments use Gisqus (GitHub-based) instead of Disqus
- Dark mode support via CSS media queries
- Custom navigation includes featured project link

## Important Notes
- Site URL: www.async-let.com
- When updating post filenames, update all internal links
- Run lint/typecheck commands if modifying Ruby/Python scripts
- Verify videos play correctly after embedding