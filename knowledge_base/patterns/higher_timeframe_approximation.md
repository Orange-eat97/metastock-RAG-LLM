---
canonical_id: pattern.higher_timeframe_approximation
title: 'Pattern: Higher Timeframe Approximation'
type: pattern
card_bucket: patterns
category: multi_timeframe
source: MetaStock Formula Primer / Formula Primer II / internal project pattern
status: active
priority: 10
supports_explorer: true
functions:
- Mov
- Security
aliases:
- text: 'Pattern: Higher Timeframe Approximation'
  type: synonym
  weight: 0.85
- text: Higher Timeframe Approximation
  type: exact
  weight: 1.0
- text: weekly condition on daily chart
  type: synonym
  weight: 0.85
- text: monthly trend filter approximation
  type: synonym
  weight: 0.85
- text: daily scan with weekly moving average approximation
  type: synonym
  weight: 0.85
- text: multi timeframe filter
  type: synonym
  weight: 0.85
requires:
- canonical_id: function.mov
  rationale: This card usually needs function.mov for correct formula generation.
  priority: 10
  properties:
    source: registry_ready_transform
    formula_role: requires
suggests:
- canonical_id: function.security
  rationale: function.security is often useful context for this card but is not always mandatory.
  priority: 40
  properties:
    source: registry_ready_transform
    formula_role: suggests
- canonical_id: reference.higher_timeframe_explorer_limitations
  rationale: reference.higher_timeframe_explorer_limitations is often useful context for this card but is not always mandatory.
  priority: 40
  properties:
    source: registry_ready_transform
    formula_role: suggests
- canonical_id: reference.lookahead_future_reference_pitfalls
  rationale: reference.lookahead_future_reference_pitfalls is often useful context for this card but is not always mandatory.
  priority: 40
  properties:
    source: registry_ready_transform
    formula_role: suggests
semantic:
  concept_role: pattern
  mechanism: multi_timeframe
  market_object: price
  directions_supported:
  - bullish
  - bearish
  operations_supported:
  - multi_timeframe
  required_components:
  - mov
  does_not_cover:
  - unrelated_pattern_substitution
  - guaranteed_trade_profitability
registry:
  enabled: true
  canonical_id: pattern.higher_timeframe_approximation
  supports_explorer: true
  priority: 10
  properties:
    formula_role: multi_timeframe
    supports_explorer: true
    source_path: patterns/higher_timeframe_approximation.md
    generated_schema_version: registry_ready_v2
---

# Pattern: Higher Timeframe Approximation

## Intent

Represent higher-timeframe style logic inside lower-timeframe or daily formulas, with explicit caveats about approximation and data availability.

## Natural Language Triggers

- higher timeframe approximation
- weekly condition on daily chart
- monthly trend filter approximation
- daily scan with weekly moving average approximation
- multi timeframe filter

## Required Logical Components

- Define the target higher timeframe concept precisely.
- Prefer actual higher timeframe data if available through MetaStock data organization.
- If approximating, translate periods carefully, such as 10 weekly bars about 50 daily bars.
- Avoid future-looking references.

## Formula Building Blocks

```metastock
Mov(C,50,S) {approx 10-week MA on daily data}
C > Mov(C,50,S)
Security("SPY",C) > Mov(Security("SPY",C),50,S)
```

## Example Compositions

```metastock
C > Mov(C,50,S)
C > Mov(C,100,S) AND Mov(C,50,S) > Mov(C,100,S)
```

## Default Assumptions

- Approximation is not identical to true higher-timeframe calculation.
- The user must specify daily/weekly/monthly intent for precise formulas.
- Default approximation: 1 week ≈ 5 trading days, 1 month ≈ 21 trading days.

## Pitfalls

- Do not claim approximation equals true weekly/monthly computation.
- Do not use positive future references.
- Do not use Security unless the target symbol exists.

## Related functions and concepts

- function.mov
- function.security
- reference.higher_timeframe_explorer_limitations
- reference.lookahead_future_reference_pitfalls

## Retrieval keywords

higher timeframe approximation, weekly condition on daily chart, monthly trend filter approximation, daily scan with weekly moving average approximation, multi timeframe filter, Mov, Security.

## Test Queries

- Find daily stocks above approximate weekly moving average
- Create a higher timeframe trend filter approximation
