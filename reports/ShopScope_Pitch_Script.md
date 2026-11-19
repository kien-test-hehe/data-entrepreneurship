# ShopScope | English rehearsal script

23 core slides; appendices for questions. Suggested timing: 12–15 minutes. Evidence ID: 9e582388fd92

## Slide 01

Open with the seller decision: finding a price that is both competitive and sustainable. ShopScope turns marketplace information into an action, not just a report.

## Slide 02

Imagine a small seller comparing diapers in multiple browser tabs. A lower package price may actually mean a higher price per diaper, and price without cost says nothing about margin. These pain points are hypotheses to validate.

## Slide 03

External context: Metric reported 429.7 trillion VND of GMV across four platforms in 2025, up 34.75%, while active seller count fell 7.43%. This motivates research but does not prove our solution.

## Slide 04

Start narrow: Vietnamese mother-and-baby sellers. The job is one recurring decision — compare offers and decide whether a proposed asking price is feasible.

## Slide 05

24,896 observations reduce to 19,686 unique listing keys. Vietnam contributes 4,956 distinct listings. Start with Vietnam; use other markets for localization research, not demand comparisons.

## Slide 06

Explain the pipeline simply: clean listing keys, identify product attributes, retrieve candidates, and combine a price benchmark with a seller-specific cost floor.

## Slide 07

Conflicting positive price observations affect 1 Vietnam listing key(s); 3,820 have usable source brand labels. Show confidence and coverage; do not hide uncertainty or fill unknown attributes with guesses.

## Slide 08

Median observed asking price: 260,000 VND (n=4,955); interquartile band 155,000–390,000 VND. Use this for orientation only. Compare equivalent product packs before deciding a selling price.

## Slide 09

The ten largest observed shops by listing count contribute 9.9% of Vietnamese unique listings. Review these catalogs for assortment patterns; keep shop counts separate from company counts.

## Slide 10

Only 133 of 4,956 listings pass the conservative title and single-price screen (2.7%). Confirm exact pack and variant manually. A smaller trustworthy benchmark is better than a broad misleading one.

## Slide 11

Of 133 unit-price eligible listings, 14 lack a usable brand or title, leaving 119 in the matching pool. We generated 20 candidate pairs; 2 have identical normalized titles. No verified precision or recall is reported until people review the actual products.

## Slide 12

4,031 of 4,723 usable image/text annotation pairs agree. Route disagreements and missing labels to a reviewer; agreement does not establish correctness.

## Slide 13

45 segments pass the minimum size and shop thresholds. Top heuristic segment: bejoyle. Check supplier cost, product suitability and customer demand before committing capital.

## Slide 14

Advisor result: ABSTAIN: no cohort with three distinct shops. Broad bobby orientation: 142 shops; median 269,500 VND. Assumed cost floor 239,000 VND. Not a matched SKU. Illustrative unit cost 162,000 VND, fee 12%, margin 20%; divide by 1 minus fee and margin, round up to the nearest 1,000 VND. Withhold SKU advice when evidence is insufficient. Verify comparable packs and refresh prices before selecting a test price.

## Slide 15

Show the actual Streamlit interface. Start with market overview, explore a brand, then enter cost and margin in Pricing Advisor. The system abstains if it cannot find adequate evidence.

## Slide 16

The proposed subscription price is 99,000 VND per month; free and future premium tiers are hypotheses. We do not claim existing paying users.

## Slide 17

Walk through Lean Canvas. The key link is customer pain → useful decision → measurable seller value → recurring subscription. Data rights and acquisition cost are essential assumptions.

## Slide 18

Market sizing should count potential customer accounts, not diaper GMV. The broad TAM ceiling is purely illustrative; SAM and SOM require verified eligible accounts and conversion evidence.

## Slide 19

Metric Starter Advanced costs VND 8M for four months (2M/month equivalent); Premium VND 12M for four months (3M/month equivalent), checked 19 November 2026. ShopScope’s proposed focus and affordability are not feature parity; interviews must test the difference.

## Slide 20

Three experiments: validate the problem with 15 interviews, test 10 paired tasks, and offer a paid pilot to 15 sellers. No results have been fabricated.

## Slide 21

At 99,000 VND/month, 20,000 VND variable cost and 20 million VND fixed monthly cost, operating break-even is 254 paying accounts. Validate willingness to pay and actual licensing costs. This is an assumption-driven scenario, not traction.

## Slide 22

Do not scale first. Complete reviewed matching pairs, seller experiments, and licensed data sourcing, then expand only if unit economics and retention support it.

## Slide 23

Close with an evidence-led ask: recruit 15 sellers and a data partner. We are building a responsible price decision workflow, not promising profit.

## Slide 24

The most frequent usable raw brand label is bobby (376 listings). Explore positioning within a brand; listing frequency is not market share or brand revenue.

## Slide 25

Brand-level medians and interquartile ranges show observed price positions for sufficiently represented raw labels. Do not interpret price differences as brand premiums without controlling for variants and pack sizes.

## Slide 26

4,955 listings have both usable prices and the source field monthly_sold. Investigate counter patterns; do not multiply the counter by asking price to claim revenue.

## Slide 27

The chart shows up to 12 recorded brand groups with at least five eligible listings, ordered by eligible count. Treat price-per-diaper estimates as indicative until a reviewer confirms the pack and selected variant.

## Slide 28

Repeat-key rates differ by country because the collection uses overlapping filtered views. Deduplicate keys before counting listings or comparing observed coverage.

## Slide 29

1,995 of 4,956 listings have an equal recorded price and min/max range. Request variant-level details; an equal range is necessary but not sufficient for SKU equivalence.

## Slide 30

786 of 4,955 usable ranges have a maximum above twice the minimum. Do not compare listing minimums as if they represented identical quantities.

## Slide 31

7 brand segments stay in the top 10 under all three tested weights. Use stable candidates as interview priorities, not inventory recommendations.

## Slide 32

External context: four-platform GMV grew 34.75% in 2025; active seller count declined 7.43%. Test whether price intelligence addresses real seller pain; the macro trend is not causal evidence.

## Slide 33

Illustrative scenarios vary monthly fixed cost and per-account servicing cost at a 99,000 VND subscription. Obtain licensing and support quotes before committing to the business model.

## Slide 34

bobby has the most distinct observed shops (142). Compare actual SKU portfolios and avoid interpreting this as market share.

## Slide 35

Reference the original Kaggle release, publisher documentation, VCCI market context, and Metric pricing. All analytical charts share the notebook evidence bundle.