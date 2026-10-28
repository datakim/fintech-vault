import type { APIRoute } from "astro";
import { getCollection, type CollectionEntry } from "astro:content";
import { getKnowledgeGraph } from "@/utils/knowledgeGraph";
import { renderPostOgImage } from "@/utils/ogImage";
import config from "@/config";

export async function getStaticPaths() {
  if (!config.features.dynamicOgImage) {
    return [];
  }

  const posts = await getCollection(
    "en",
    ({ data }) => !data.draft && !data.ogImage
  );
  return posts.map(post => ({
    params: { slug: post.id },
    props: post,
  }));
}

export const GET: APIRoute = async ({ props, url }) => {
  if (!config.features.dynamicOgImage) {
    return new Response(null, { status: 404, statusText: "Not found" });
  }

  const post = props as CollectionEntry<"en">;
  const png = await renderPostOgImage(
    { id: post.id, ...post.data },
    await getKnowledgeGraph("en"),
    "en",
    url
  );

  return new Response(new Uint8Array(png), {
    headers: { "Content-Type": "image/png" },
  });
};
