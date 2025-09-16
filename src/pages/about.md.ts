import type { APIRoute } from "astro";
// Use Vite's raw import to bundle the source at build time
import aboutSource from "./about.md?raw";

export const GET: APIRoute = async () => {
  return new Response(aboutSource, {
    headers: {
      "Content-Type": "text/plain; charset=utf-8",
      "Cache-Control": "public, max-age=0, s-maxage=3600",
    },
  });
};
