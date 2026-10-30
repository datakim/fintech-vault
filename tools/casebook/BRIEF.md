# Fintech ML casebook: collection brief

We are building a "casebook" page for a fintech/AI blog (financialailab.com): a curated database of what
fintech companies have published about the ML/AI systems they actually run. Readers are data scientists
and ML engineers in finance. Every entry links to the company's own post.

## What to collect

First-party posts from a company's own engineering blog, tech blog, research blog or official Medium
publication (also official newsroom posts IF they describe a model in technical terms: what it is,
what data, what result). Published **between 2024-10-01 and 2026-10-30**.

The post must describe an ML/AI system the company built, runs in production, or seriously piloted,
in one of these five domains:

| domain key   | covers |
|--------------|--------|
| `investment` | trading, market prediction, portfolio/robo-advice, research assistants for investors or advisors, crypto market/trading models |
| `credit`     | underwriting, default/PD models, credit limits, loan pricing, collections and delinquency, cash-flow underwriting, BNPL risk |
| `fraud`      | payment/card/transaction fraud, account takeover, scams, identity/document fraud, AML / transaction monitoring, sanctions screening, merchant risk, disputes/chargebacks |
| `marketing`  | personalization, recommendation, CRM/notification targeting, churn, LTV, uplift/promotions, acquisition, in-app search/ranking, user segmentation |
| `operations` | customer support (chatbots, agent assist), document processing, back-office automation, internal LLM assistants/agents for staff, compliance review workflows, forecasting for ops (cash, liquidity, volume), payment authorization/routing optimization, reconciliation |

Skip: generic ML platform/infra posts that are not tied to one of these domains, hiring posts, event
listings, pure software engineering, vague "AI strategy" posts with no system described, press releases
with no technical content, third-party news coverage (only first-party sources count).

## Verification rules (strict)

- Find candidates with web search and by browsing the blog's index/tag pages.
- **Open every URL you record** (WebFetch) and confirm: it loads, the title, the publication date, and
  that the content matches. Never write a URL from memory or guess a slug.
- If the publication date can't be confirmed, or it falls outside the window, skip the post.
- Facts in `note_*` and `metric` must come from the post itself. Do not add numbers that are not in it.
- Quality over quantity, but do aim for coverage: for each assigned company, check its blog for the
  whole window, not just the first search hit.

## Output

Write a JSON array to the output path given in your task. One object per post:

```json
{
  "id": "stripe-payments-foundation-model",
  "company": "Stripe",
  "region": "US",
  "title": "Exact original title of the post",
  "url": "https://...",
  "date": "2025-05-07",
  "lang": "en",
  "domain": "fraud",
  "methods": ["foundation-model", "transformer", "real-time"],
  "problem_en": "Card-testing and fraud detection",
  "problem_ko": "카드 테스팅·사기 탐지",
  "note_en": "One sentence, at most 30 words: what they built and the most concrete detail the post gives (data scale, latency, metric).",
  "note_ko": "같은 내용을 한국어 평서체(~다)로 한 문장.",
  "metric": "optional: one headline number exactly as stated in the post, with what it measures (e.g. 'card-testing detection rate 59% → 97%'). Omit the key if the post gives none."
}
```

- `id`: kebab-case, `<company>-<topic>`, unique.
- `region`: one of `US`, `UK`, `EU`, `KR`, `JP`, `CN`, `SG`, `IN`, `ID`, `BR`, `LATAM`, `Global`.
- `lang`: language of the post (`en`, `ko`, `ja`, `zh`, `pt`, `es`).
- `domain`: exactly one key from the table above (the primary one).
- `methods`: 1–4 keys from this fixed vocabulary only:
  `gbdt`, `deep-learning`, `sequence-model`, `transformer`, `foundation-model`, `graph`, `llm`, `rag`,
  `agent`, `embeddings`, `anomaly-detection`, `forecasting`, `causal-uplift`, `bandit-rl`,
  `recommender`, `document-ai`, `nlp`, `explainability`, `real-time`, `mlops`, `optimization`, `speech`.
- Korean text uses plain declarative style (~다), no 합니다체, no em dashes. English text: no em dashes.
- Write the file with valid JSON (UTF-8). Validate it with `python3 -m json.tool <path>` before finishing.

## Final reply

Reply briefly: the output path, number of entries, count per domain, and any companies where you found
nothing in the window or could not access the blog. Do not paste the entries into the reply.
