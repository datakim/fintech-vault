import { defineAstroPaperConfig } from "./src/types/config";

export default defineAstroPaperConfig({
  site: {
    url: "https://fintech-vault.vercel.app",
    title: "Fintech Vault",
    description: "금융 AI, 데이터 사이언스, 그리고 LLM 응용에 대한 기록",
    author: "Elliot Kim (김태헌)",
    profile: "",
    ogImage: "default-og.jpg",
    lang: "ko",
    timezone: "Asia/Seoul",
    dir: "ltr",
  },
  posts: {
    perPage: 4,
    perIndex: 4,
    scheduledPostMargin: 15 * 60 * 1000,
  },
  features: {
    lightAndDarkMode: true,
    dynamicOgImage: true,
    showArchives: true,
    showBackButton: true,
    // 저장소 주소가 정해지면 enabled: true 로 바꾸고 url 을 채워주세요.
    editPost: {
      enabled: false,
    },
    search: "pagefind",
  },
  // GitHub만 활성화. URL은 추후 본인 저장소 주소로 채워주세요.
  // (이 v6 테마는 active 플래그가 없어 배열에 넣은 항목만 노출됩니다.)
  socials: [{ name: "github", url: "" }],
  shareLinks: [
    { name: "whatsapp", url: "https://wa.me/?text=" },
    { name: "facebook", url: "https://www.facebook.com/sharer.php?u=" },
    { name: "x",        url: "https://x.com/intent/post?url=" },
    { name: "telegram", url: "https://t.me/share/url?url=" },
    { name: "pinterest", url: "https://pinterest.com/pin/create/button/?url=" },
    { name: "mail",     url: "mailto:?subject=See%20this%20post&body=" },
  ],
});