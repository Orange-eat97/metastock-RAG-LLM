---
canonical_id: pattern.rsi_divergence
title: 'Pattern: RSI Divergence'
type: pattern
card_bucket: patterns
category: indicator_divergence
source: generated_curated_from_primer
status: active
priority: 10
supports_explorer: true
aliases:
- text: RSI divergence
  type: exact
  weight: 1.0
- text: bullish RSI divergence
  type: phrase
  weight: 0.95
- text: bearish RSI divergence
  type: phrase
  weight: 0.95
- text: price lower low RSI higher low
  type: phrase
  weight: 0.9
requires:
- canonical_id: function.rsi
  rationale: RSI divergence requires RSI values.
  priority: 30
  properties:
    formula_role: indicator_series
suggests:
- canonical_id: function.divergence
  rationale: Built-in Divergence can express ZigZag-based divergence.
  priority: 30
  properties:
    formula_role: zigzag_divergence
- canonical_id: function.llv
  rationale: Transparent bullish divergence often compares price lows.
  priority: 30
  properties:
    formula_role: price_low_component
- canonical_id: function.valuewhen
  rationale: Event-based divergence may retrieve prior pivot values.
  priority: 30
  properties:
    formula_role: prior_pivot_value
semantic:
  concept_role: pattern
  mechanism: indicator_divergence
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
  canonical_id: pattern.rsi_divergence
  supports_explorer: true
  priority: 10
  properties:
    formula_role: indicator_divergence
    source_path: patterns/rsi_divergence.md
    curation_level: upgraded_to_curated_quality
---

# Pattern: RSI Divergence

## Intent

Detect divergence between price and RSI. Bullish divergence usually means price makes a lower low while RSI makes a higher low. Bearish divergence usually means price makes a higher high while RSI makes a lower high. This is a pattern card because exact divergence requires defining pivots, lookback, and confirmation.

## Natural Language Triggers

- RSI divergence
- bullish RSI divergence
- bearish RSI divergence
- price lower low RSI higher low
- price higher high RSI lower high

## Keywords

- RSI divergence
- bullish divergence
- bearish divergence
- Divergence(RSI(14),C,5)
- lower low higher RSI

## Required Logical Components

- Choose bullish or bearish direction.
- Define the price pivot or swing comparison.
- Define the RSI pivot or swing comparison.
- Choose transparent fixed-window logic or ZigZag-based `Divergence` function.
- Warn about ZigZag repaint if using built-in Divergence.

## Optional Confirmation Components

- Trend confirmation, such as close above a moving average.
- Volume confirmation, such as `V > Mov(V,20,S)`.
- Momentum confirmation, such as RSI, MACD, or ROC improving.
- Recency confirmation using `BarsSince()` when the user asks for recent signals.

## Formula Building Blocks

```metastock
Divergence(RSI(14),C,5) = 1
C < Ref(LLV(C,20),-1) AND RSI(14) > Ref(LLV(RSI(14),20),-1)
C > Ref(HHV(C,20),-1) AND RSI(14) < Ref(HHV(RSI(14),20),-1)
```

## Composition Guidance

- If user asks generally and accepts a simple scan, use fixed-window divergence approximation.
- If user explicitly asks for MetaStock Divergence function, use `Divergence(RSI(14),C,5)` and include repaint caveat.
- Do not use simple RSI oversold as a substitute for divergence.

## Example Compositions

### Simple bullish RSI divergence approximation

User request:

```text
Find bullish RSI divergence
```

Explorer output:

```text
Column A: C
Column B: Ref(LLV(C,20),-1)
Column C: RSI(14)
Column D: Ref(LLV(RSI(14),20),-1)
Filter: ColA < ColB AND ColC > ColD
```
### ZigZag-based RSI divergence function

User request:

```text
Find stocks with RSI divergence using the MetaStock Divergence function
```

Explorer output:

```text
Column A: Divergence(RSI(14),C,5)
Filter: ColA <> 0
```

## Observable Outputs

Useful Explorer columns:

- Current close
- Prior price low/high
- Current RSI
- Prior RSI low/high
- Divergence flag

## Default Assumptions

- Default RSI period is 14.
- Default fixed lookback is 20 if user does not specify.
- Built-in Divergence is ZigZag-based and may repaint.

## Pitfalls

- Do not equate RSI below 30 with divergence.
- Do not use future pivot logic for current Explorer scans.
- Do not ignore argument order and direction when using Divergence.

## Good outputs

```metastock
C < Ref(LLV(C,20),-1) AND RSI(14) > Ref(LLV(RSI(14),20),-1)
Divergence(RSI(14),C,5) <> 0
```

## What not to do

- Bad: `RSI(14) < 30` as RSI divergence.
- Bad: using `Ref(C,1)` to confirm a pivot on the current bar.
- Bad: claiming ZigZag-based divergence is stable on the latest bar.

## Related functions and concepts

- function.rsi
- function.divergence
- function.llv
- function.hhv
- reference.zigzag_based_function_repaint_pitfall

## Retrieval keywords

RSI divergence, bullish divergence, bearish divergence, Divergence(RSI(14),C,5), lower low higher RSI.

## Test Queries

- Find bullish RSI divergence
- Find stocks where price makes lower low but RSI makes higher low
