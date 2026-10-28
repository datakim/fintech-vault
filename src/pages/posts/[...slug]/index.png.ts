import type { APIRoute } from "astro";
import { getCollection, type CollectionEntry } from "astro:content";
import { getPostSlug } from "@/utils/getPostPaths";
import { getKnowledgeGraph } from "@/utils/knowledgeGraph";
import { renderPostOgImage } from "@/utils/ogImage";
import config from "@/config";

export async function getStaticPaths() {
  if (!config.features.dynamicOgImage) {
    return [];
  }

  const posts = await getCollection("posts").then(p =>
    p.filter(({ data }) => !data.draft && !data.ogImage)
  );

  return posts.map(post => ({
    params: { slug: getPostSlug(post.id, post.filePath) },
    props: post,
  }));
}

export const GET: APIRoute = async ({ props, url }) => {
  if (!config.features.dynamicOgImage) {
    return new Response(null, { status: 404, statusText: "Not found" });
  }

  const post = props as CollectionEntry<"posts">;
  const png = await renderPostOgImage(
    {
      id: getPostSlug(post.id, post.filePath).replace(/^\//, ""),
      ...post.data,
    },
    await getKnowledgeGraph("ko"),
    "ko",
    url
  );

  return new Response(new Uint8Array(png), {
    headers: { "Content-Type": "image/png" },
  });
};
