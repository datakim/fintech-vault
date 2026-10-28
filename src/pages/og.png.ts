import type { APIRoute } from "astro";
import { getKnowledgeGraph } from "@/utils/knowledgeGraph";
import { renderSiteOgImage } from "@/utils/ogImage";

export const GET: APIRoute = async context => {
  const png = await renderSiteOgImage(
    await getKnowledgeGraph("en"),
    context.url
  );

  return new Response(new Uint8Array(png), {
    headers: { "Content-Type": "image/png" },
  });
};
