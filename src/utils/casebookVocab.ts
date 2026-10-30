/*
 * 사례집 분류 어휘. content.config.ts도 이 파일을 쓰므로 astro:content를 불러오지 않는다.
 */

export type CaseLang = "en" | "ko";

export const DOMAINS = [
  { id: "investment", en: "Investment", ko: "투자" },
  { id: "credit", en: "Credit risk", ko: "신용 리스크" },
  { id: "fraud", en: "Fraud risk", ko: "사기 리스크" },
  { id: "marketing", en: "Marketing", ko: "마케팅" },
  { id: "operations", en: "Operations", ko: "오퍼레이션" },
] as const;

export const METHODS = [
  { id: "gbdt", en: "GBDT", ko: "GBDT" },
  { id: "deep-learning", en: "Deep learning", ko: "딥러닝" },
  { id: "sequence-model", en: "Sequence models", ko: "시퀀스 모델" },
  { id: "transformer", en: "Transformers", ko: "트랜스포머" },
  { id: "foundation-model", en: "Foundation models", ko: "파운데이션 모델" },
  { id: "graph", en: "Graphs", ko: "그래프" },
  { id: "llm", en: "LLMs", ko: "LLM" },
  { id: "rag", en: "RAG", ko: "RAG" },
  { id: "agent", en: "Agents", ko: "에이전트" },
  { id: "embeddings", en: "Embeddings", ko: "임베딩" },
  { id: "anomaly-detection", en: "Anomaly detection", ko: "이상 탐지" },
  { id: "forecasting", en: "Forecasting", ko: "시계열 예측" },
  { id: "causal-uplift", en: "Causal & uplift", ko: "인과·업리프트" },
  { id: "bandit-rl", en: "Bandits & RL", ko: "밴딧·강화학습" },
  { id: "recommender", en: "Recommenders", ko: "추천" },
  { id: "document-ai", en: "Document AI", ko: "문서 AI" },
  { id: "nlp", en: "NLP", ko: "NLP" },
  { id: "explainability", en: "Explainability", ko: "설명 가능성" },
  { id: "real-time", en: "Real-time", ko: "실시간" },
  { id: "mlops", en: "MLOps", ko: "MLOps" },
  { id: "optimization", en: "Optimization", ko: "최적화" },
  { id: "speech", en: "Speech", ko: "음성" },
] as const;

export const REGIONS: Record<string, { en: string; ko: string }> = {
  US: { en: "United States", ko: "미국" },
  UK: { en: "United Kingdom", ko: "영국" },
  EU: { en: "Europe", ko: "유럽" },
  KR: { en: "Korea", ko: "한국" },
  JP: { en: "Japan", ko: "일본" },
  CN: { en: "China", ko: "중국" },
  SG: { en: "Southeast Asia", ko: "동남아" },
  ID: { en: "Indonesia", ko: "인도네시아" },
  IN: { en: "India", ko: "인도" },
  BR: { en: "Brazil", ko: "브라질" },
  LATAM: { en: "Latin America", ko: "중남미" },
  Global: { en: "Global", ko: "글로벌" },
};

export type DomainId = (typeof DOMAINS)[number]["id"];
export type MethodId = (typeof METHODS)[number]["id"];

export const DOMAIN_IDS = DOMAINS.map(d => d.id) as [DomainId, ...DomainId[]];
export const METHOD_IDS = METHODS.map(m => m.id) as [MethodId, ...MethodId[]];
