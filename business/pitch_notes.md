# ShopScope — Presenter notes and defense Q&A

**12–14 minutes.** Follow slide titles in the generated deck; slide numbers may change between builds. All numerical evidence must match the deck's evidence ID.

## Opening: problem and market (2:30)
- **See the market. Sell smarter.** Imagine sourcing a diaper product: is the asking price competitive and does it cover costs? ShopScope turns fragmented listings into explainable pricing decisions.
- **A small seller faces a big decision.** Raw pack prices are misleading when quantities, sizes and variants differ. A competitive price can be unprofitable after fees. This customer pain is a hypothesis to test.
- **A growing market. A tougher game.** Metric via VCCI reports 429.7 trillion VND in four-platform GMV in 2025, up 34.75%, while active seller counts fell 7.43%. These statistics do not establish the cause of seller exits.
- **Start with one customer and one decision.** Our beachhead is small Vietnamese mother-and-baby retailers: identify truly comparable products, benchmark prices and protect margin.
- **Six markets; one historical snapshot.** 24,896 observations, 19,686 unique listing keys, 4,956 Vietnam listings from 1,017 shops. This filtered snapshot is neither a market census nor current prices.

## Evidence and product (5:30)
- **From fragmented listings to a decision.** Clean keys, extract attributes, rank candidates under constraints, and compare a supported price band with a seller-specific cost floor.
- **Data quality is a product feature.** Surface conflicting and missing attributes. Variant pricing and brand disagreements require review.
- **A wide price band is not a price recommendation.** The historical median asking price is 260,000 VND; the middle half spans 155,000–390,000 VND. This is orientation across heterogeneous products, not an optimal SKU price.
- **Competitive catalogs are uneven.** Top ten shops represent 9.9% of observed listings, not sales share. Compare direct competitors rather than simply copying the largest catalog.
- **Reliable unit pricing requires abstention.** Explain the eligibility funnel. A large raw dataset does not imply many comparable variants. This motivates verified catalog enrichment.
- **Find similar products. Admit uncertainty.** Exact titles provide a baseline; character TF-IDF generates ranked candidates under mandatory attribute constraints. 133 unit-price eligible listings become 119 matching-pool listings after 14 exclusions lacking brand or title. The 20 pairs are not listings. A queue is not a labeled benchmark. Human evaluation is pending.
- **Multimodal labels are not ground truth.** Image/text agreement is a consistency signal, not accuracy. Disagreements prioritize review.
- **Prioritize research, not inventory bets.** Screen observed brand-level popularity and shop counts; inspect weighting sensitivity. Not demand or a guaranteed investment.
- **A recommendation must respect margin.** Demo the local Streamlit Pricing Advisor. Select a historical product, enter cost, fees and margin. Show the floor and explain ABSTAIN if comparable evidence is insufficient. The alternative brand benchmark is orientation only. The notebook example assumes 162,000 VND cost, 12% fee, 20% margin and rounds the calculated 238,235.29 VND floor up to 239,000 VND; not a market quote.
- **Experience ShopScope.** Demonstrate overview, explorer, competitor analysis, price intelligence, opportunity finder and pricing advisor. Historical dataset only.

## Entrepreneurship (4:00)
- **Business model.** Freemium, proposed Pro at 99,000 VND/month, future Business at 299,000. Test pricing rather than claiming revenue.
- **Lean Canvas.** One seller decision and one category. Metrics: time saved, matching precision, paid conversion. Verified localized product data and corrections could become an advantage, not a proven moat.
- **Size in seller accounts, not GMV.** The all-seller annual subscription calculation is an optimistic ceiling, not measured TAM. Validate eligible accounts, SAM, acquisition and retention.
- **Competitive positioning.** Established analytics providers and manual tools are alternatives. Metric Starter Advanced: VND 8M/4 months (2M/month equivalent); Premium: VND 12M/4 months (3M/month equivalent), checked 19 November 2026. Our proposed wedge is a narrow, explainable pricing workflow. Actual differentiation remains to be tested.
- **Test before scaling.** Recruit 15 sellers for interviews, 10 for paired tasks, and 15 for paid offers. Thresholds: 10/15 report recurring pain, 50% median time reduction without lower accuracy, and 3 real paid commitments. Nothing is claimed as conducted.
- **Unit economics.** Assumed subscription 99,000 VND, variable cost 20,000 and fixed cost 20 million imply 254 paid accounts at operating break-even. Actual data costs, CAC and churn can change this substantially.

## Close (1:00)
- **Gated roadmap.** Validate customer pain and matching; acquire permission and reliable refresh; then validate acquisition and retention before expanding.
- **The ask.** Access to 15 small sellers, a domain reviewer and a licensed data partner. Evidence before scale.

## Defense questions
| Question | Answer |
|---|---|
| Why diapers? | Brand, pack quantity and variant ambiguity creates a focused comparison problem; category attractiveness is not proven. |
| Why not forecast demand with LSTM? | Only a cross-sectional snapshot and no verified transaction history. |
| Can you claim matching accuracy? | No. Candidate retrieval must be independently labeled; measure precision, candidate-set recall and coverage. |
| Are the 1,017 shops customers? | No. They are observed shop keys, not validated prospects. |
| Why not recommend the median price? | The raw median combines non-equivalent products and is not an optimal price. |
| Why is eligibility small? | Ambiguous quantity, size, product type and variant prices prevent trustworthy comparison. Improve verified catalogs, not weaker safeguards. |
| What is your moat? | Potential localized labeled data and feedback; not demonstrated yet. |
| What is your next step? | Interview real sellers, review product pairs, and obtain rights to refreshed data. |
