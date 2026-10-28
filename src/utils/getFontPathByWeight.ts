import type { FontData } from "astro:assets";

export function getFontPathByWeight(
  fonts: FontData[],
  weight: number,
  options?: {
    style?: "normal" | "italic";
    format?: string;
  }
): string | undefined {
  const style = options?.style ?? "normal";
  const format = options?.format ?? "truetype";

  // 형식마다 항목이 따로 생기므로(woff2, ttf …) 맞는 항목을 모두 훑는다.
  return fonts
    .filter(font => font.weight === String(weight) && font.style === style)
    .flatMap(font => font.src)
    .find(file => file.format === format)?.url;
}
