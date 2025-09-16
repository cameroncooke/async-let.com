# Async Let — Blog

Personal blog by Cameron Cooke. Articles on Swift, iOS, AI‑assisted development, and indie projects.

## Contents

- Tech stack and structure
- Local development
- Writing posts and images
- Tags
- Embeds (YouTube, Tweets, etc.)
- Deployment
- Credits

## Tech stack and structure

- Framework: Astro
- Theme: AstroPaper (no local theme changes)
- Styles: Tailwind CSS
- Search: Pagefind
- Content: Markdown/MDX under `src/data/blog`

Key paths

- Posts: `src/data/blog/*.md` (or `.mdx` when using embeds/components)
- Per‑post images: `src/data/blog/<slug>/...` (refer to them relatively, e.g. `![](./<slug>/image.png)`)
- Videos and other static files: `public/assets/videos/...`
- Site config: `src/config.ts` (title, author, website, timezone)
- Social links: `src/constants.ts`

## Local development

```bash
npm install
npm run dev
# open http://localhost:4321
```

Production build and preview

```bash
npm run build
npm run preview
```

## Writing posts and images

- Create a new file in `src/data/blog/` named after the slug, e.g. `my-post.md`.
- Frontmatter fields used here: `title`, `description`, `pubDatetime` (Date), optional `modDatetime`, `tags`, `ogImage` (relative path to a local image).
- Header image: place the image next to the post (e.g. `src/data/blog/my-post/header.png`) and reference at the top of the Markdown with `![](./my-post/header.png)`. Keep `ogImage: ./my-post/header.png` in frontmatter for social previews.
- Table of contents: add a heading `## Table of contents` in your post to inject a TOC automatically.

## Tags

- Use Title Case for words (`Swift`, `Testing`), keep acronyms uppercase (`MCP`, `CLI`, `SPM`).
- Reuse existing tags for consistency (see `/tags`). The theme slugifies tags for URLs automatically.

## Embeds

This site is configured with `astro-embed` and MDX.

- Use MDX when you need embeds: rename your post to `.mdx`.
- You can either use components or auto‑embeds for supported links.

Examples (MDX):

```mdx
---
title: "My Post with Embeds"
---

import { YouTube, Tweet } from 'astro-embed';

<YouTube id="dQw4w9WgXcQ" />

<Tweet id="20" />

# Or paste supported links on their own line for auto‑embed
https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

No theme files were modified for embeds; only `astro.config.ts` was configured to include `embeds()` and `mdx()` integrations.

## Deployment

The site builds to `dist/` (static output). Deploy to any static host (Cloudflare Pages, Netlify, Vercel, GitHub Pages, etc.). Update `SITE.website` in `src/config.ts` to your final domain before deploying.

## Credits

- Theme: AstroPaper by Sat Naing — https://github.com/satnaing/astro-paper
- Thank you to the original theme author and contributors.
