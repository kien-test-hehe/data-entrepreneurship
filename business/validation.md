# Seller pilot: validation protocol

Status: **not conducted**. Never fabricate responses.

## Test 1: Problem
Recruit 15 active small online sellers in Vietnam. Ask for their most recent pricing decision, what tools were used, time spent, recurring errors, and fee/margin awareness. Pass: 10/15 describe recurrent pricing difficulty. Owner: Business Lead. Review: Week 1.

## Test 2: Product
Recruit 10 sellers. Counterbalance manual versus prototype order. Use identical or matched pricing tasks with a human-reviewed reference answer. Record completion time, accuracy and confidence. Pass: median time decreases at least 50%, with no decrease in accuracy. Owner: Product Lead. Review: Week 3.

## Test 3: Revenue
Offer 15 eligible sellers a real paid pilot at VND 99,000/month after obtaining data permission. Pass: 3 actual paid commitments. Record actual payments separately from stated willingness. Owner: Growth Lead. Review: Week 4.

## Matching labels
Use outputs/private/matching_review_queue.csv locally. Review title, physical package, size, product line and variant. Two reviewers label 1 equivalent, 0 not equivalent, blank unclear. Resolve disagreements independently. Save reviewed labels to evaluation/reviewed_pairs.csv; rerun notebook. Do not publish listing-level identifiers or personal data without rights. Candidate-set recall is not full retrieval recall.

## Data collection template
Use anonymous IDs; obtain consent. Fields: participant_id, seller_category, active_seller, recent_pricing_task, recurring_pain, manual_seconds, prototype_seconds, manual_correct, prototype_correct, paid_commitment, notes. No names or contact details in public repository.
