import type { APIRoute } from "astro";
import { getCollection } from "astro:content";
import { getPath } from "@/utils/getPath";

export async function getStaticPaths() {
  const posts = await getCollection("blog", ({ data }) => !data.draft);
  return posts.map(post => ({
    params: { slug: getPath(post.id, post.filePath, false) },
    props: { body: post.body },
  }));
}

export const GET: APIRoute = async ({ props }) => {
  const body = (props as { body: string }).body;
  return new Response(body, {
    headers: {
      "Content-Type": "text/plain; charset=utf-8",
      // Cache raw markdown for a short period; adjust as desired
      "Cache-Control": "public, max-age=0, s-maxage=3600",
    },
  });
};

