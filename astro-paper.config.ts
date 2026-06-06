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
    // 검색엔진 사이트 검증 메타 태그 값(content 속성 값만 적습니다).
    // - Google: 이미 public/google105fb3fcb81b9d7f.html 파일로 인증된 상태라 비워둬도 됩니다.
    // - Naver:  https://searchadvisor.naver.com/ 에 사이트 등록 → "HTML 태그" 인증 선택 →
    //           <meta name="naver-site-verification" content="여기"> 의 "여기" 값만 붙여넣기.
    // - Bing:   https://www.bing.com/webmasters 에 등록 → "HTML 태그" 인증 →
    //           <meta name="msvalidate.01" content="여기"> 의 "여기" 값.
    naverVerification: "111197347ee238c010bcc0bf4751da62c4c1e194",
    bingVerification: "",
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
  // 배열에 넣은 항목만 노출됩니다 (이 v6 테마는 active 플래그가 없음).
  // GitHub URL은 추후 본인 저장소/프로필 주소로 채워주세요.
  socials: [
    { name: "github", url: "" },
    { name: "linkedin", url: "https://www.linkedin.com/in/datamanyo/" },
  ],
  shareLinks: [
    { name: "whatsapp", url: "https://wa.me/?text=" },
    { name: "facebook", url: "https://www.facebook.com/sharer.php?u=" },
    { name: "x",        url: "https://x.com/intent/post?url=" },
    { name: "telegram", url: "https://t.me/share/url?url=" },
    { name: "pinterest", url: "https://pinterest.com/pin/create/button/?url=" },
    { name: "mail",     url: "mailto:?subject=See%20this%20post&body=" },
  ],
});