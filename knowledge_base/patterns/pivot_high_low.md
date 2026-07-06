---
canonical_id: pattern.pivot_high_low
title: 'Pattern: Pivot High / Pivot Low'
type: pattern
card_bucket: patterns
category: pivot
source: generated_curated_from_primer
status: active
priority: 10
supports_explorer: true
aliases:
- text: pivot high
  type: exact
  weight: 1.0
- text: pivot low
  type: exact
  weight: 1.0
- text: minor pivot high
  type: phrase
  weight: 0.95
- text: minor pivot low
  type: phrase
  weight: 0.95
- text: swing high pivot
  type: phrase
  weight: 0.9
requires:
- canonical_id: function.ref
  rationale: Pivot definitions require comparing neighboring bars.
  priority: 30
  properties:
    formula_role: neighbor_bar_reference
suggests:
- canonical_id: function.max
  rationale: Pivot high may compare against max of adjacent highs.
  priority: 30
  properties:
    formula_role: adjacent_high_comparison
- canonical_id: function.min
  rationale: Pivot low may compare against min of adjacent lows.
  priority: 30
  properties:
    formula_role: adjacent_low_comparison
semantic:
  concept_role: pattern
  mechanism: pivot
  market_object: price
  directions_supported:
  - bullish
  - bearish
  operations_supported:
  - screening
  - confirmation
  - threshold_filter
  required_components:
  - condition_definition
  - lookback_or_threshold
  does_not_cover:
  - unrelated_pattern
registry:
  enabled: true
  canonical_id: pattern.pivot_high_low
  supports_explorer: true
  priority: 10
  properties:
    formula_role: pivot
    source_path: patterns/pivot_high_low.md
    curation_level: upgraded_to_curated_quality
---

# Pattern: Pivot High / Pivot Low

## Intent

Identify local pivot highs and lows. A strict current-bar pivot high requires knowing the next bar, which is future-looking for Explorer scans. For Explorer-safe scans, use delayed confirmation: identify whether the previous bar was a pivot after the current bar exists.

## Natural Language Triggers

- pivot high
- pivot low
- swing high
- swing low
- minor pivot
- fractal high
- fractal low

## Keywords

- pivot high
- pivot low
- swing high
- swing low
- Ref(H,-1)
- Ref(H,-2)
- delayed pivot

## Required Logical Components

- Choose pivot high or pivot low.
- Compare the candidate pivot bar with the bar before and after it.
- Avoid future-looking current-bar pivots in Explorer.
- Use delayed confirmation for previous-bar pivot on current exploration date.

## Optional Confirmation Components

- Trend confirmation, such as close above a moving average.
- Volume confirmation, such as `V > Mov(V,20,S)`.
- Momentum confirmation, such as RSI, MACD, or ROC improving.
- Recency confirmation using `BarsSince()` when the user asks for recent signals.

## Formula Building Blocks

```metastock
Ref(H,-1) > Ref(H,-2) AND Ref(H,-1) > H
Ref(L,-1) < Ref(L,-2) AND Ref(L,-1) < L
H > Max(Ref(H,-1),Ref(H,1))  {not Explorer-safe for current bar}
```

## Composition Guidance

- Use delayed previous-bar pivot formulas for Explorer-safe scans.
- If the user wants historical plotted pivots, explain that forward references may be involved.
- Do not use `Ref(H,1)` for current Explorer signals unless explicitly analysing historical hindsight.

## Example Compositions

### Previous bar pivot high confirmed today

User request:

```text
Find stocks where the previous bar was a pivot high
```

Explorer output:

```text
Column A: Ref(H,-1)
Column B: Ref(H,-2)
Column C: H
Filter: ColA > ColB AND ColA > ColC
```
### Previous bar pivot low confirmed today

User request:

```text
Find stocks where the previous bar was a pivot low
```

Explorer output:

```text
Column A: Ref(L,-1)
Column B: Ref(L,-2)
Column C: L
Filter: ColA < ColB AND ColA < ColC
```

## Observable Outputs

Useful Explorer columns:

- Candidate pivot high/low
- Prior neighboring value
- Current neighboring value
- Pivot flag

## Default Assumptions

- Explorer-safe pivot means delayed confirmation on the previous bar.
- Current-bar centered pivot would require future reference and should be avoided.
- Use high for pivot high and low for pivot low.

## Pitfalls

- Do not use `Ref(H,1)` in a live Explorer scan.
- Do not confuse fixed lookback high with local pivot high.
- Do not use ZigZag Peak/Trough without repaint warning.

## Good outputs

```metastock
Ref(H,-1) > Ref(H,-2) AND Ref(H,-1) > H
Ref(L,-1) < Ref(L,-2) AND Ref(L,-1) < L
```

## What not to do

- Bad: `H > Max(Ref(H,-1),Ref(H,1))` for current live Explorer signal.
- Bad: `HHV(H,20)` as a local pivot high.
- Bad: no delayed-confirmation assumption.

## Related functions and concepts

- function.ref
- function.max
- function.min
- reference.lookahead_future_reference_pitfalls

## Retrieval keywords

pivot high, pivot low, swing high, swing low, Ref(H,-1), Ref(H,-2), delayed pivot.

## Test Queries

- Find stocks where the previous bar was a pivot high
- Find stocks where the previous bar was a pivot low
