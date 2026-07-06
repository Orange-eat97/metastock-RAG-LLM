---
canonical_id: pattern.macd_divergence
title: 'Pattern: MACD Divergence'
type: pattern
card_bucket: patterns
category: indicator_divergence
source: generated_curated_from_primer
status: active
priority: 10
supports_explorer: true
aliases:
- text: MACD divergence
  type: exact
  weight: 1.0
- text: bullish MACD divergence
  type: phrase
  weight: 0.95
- text: bearish MACD divergence
  type: phrase
  weight: 0.95
- text: price lower low MACD higher low
  type: phrase
  weight: 0.9
requires:
- canonical_id: function.macd
  rationale: MACD divergence requires MACD values.
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
  canonical_id: pattern.macd_divergence
  supports_explorer: true
  priority: 10
  properties:
    formula_role: indicator_divergence
    source_path: patterns/macd_divergence.md
    curation_level: upgraded_to_curated_quality
---

# Pattern: MACD Divergence

## Intent

Detect divergence between price and MACD. Bullish divergence usually means price makes a lower low while MACD makes a higher low. Bearish divergence usually means price makes a higher high while MACD makes a lower high.

## Natural Language Triggers

- MACD divergence
- bullish MACD divergence
- bearish MACD divergence
- price lower low MACD higher low
- price higher high MACD lower high

## Keywords

- MACD divergence
- bullish divergence
- bearish divergence
- Divergence(MACD(),C,5)
- lower low higher MACD

## Required Logical Components

- Choose bullish or bearish direction.
- Define price swing comparison.
- Define MACD swing comparison.
- Choose fixed-window approximation or ZigZag-based Divergence function.
- Warn about ZigZag repaint if using Divergence.

## Optional Confirmation Components

- Trend confirmation, such as close above a moving average.
- Volume confirmation, such as `V > Mov(V,20,S)`.
- Momentum confirmation, such as RSI, MACD, or ROC improving.
- Recency confirmation using `BarsSince()` when the user asks for recent signals.

## Formula Building Blocks

```metastock
Divergence(MACD(),C,5) = 1
C < Ref(LLV(C,20),-1) AND MACD() > Ref(LLV(MACD(),20),-1)
C > Ref(HHV(C,20),-1) AND MACD() < Ref(HHV(MACD(),20),-1)
```

## Composition Guidance

- Use fixed-window approximation for Explorer-friendly transparent logic.
- Use built-in Divergence only when user wants ZigZag-based divergence.
- Do not substitute MACD crossover for divergence.

## Example Compositions

### Simple bullish MACD divergence approximation

User request:

```text
Find bullish MACD divergence
```

Explorer output:

```text
Column A: C
Column B: Ref(LLV(C,20),-1)
Column C: MACD()
Column D: Ref(LLV(MACD(),20),-1)
Filter: ColA < ColB AND ColC > ColD
```
### ZigZag-based MACD divergence

User request:

```text
Find MACD divergence using Divergence
```

Explorer output:

```text
Column A: Divergence(MACD(),C,5)
Filter: ColA <> 0
```

## Observable Outputs

Useful Explorer columns:

- Current close
- Prior price low/high
- Current MACD
- Prior MACD low/high
- Divergence flag

## Default Assumptions

- Default MACD is `MACD()`.
- Default fixed lookback is 20 if unspecified.
- Built-in Divergence is ZigZag-based and may repaint.

## Pitfalls

- Do not equate MACD crossover with divergence.
- Do not use future references to confirm current pivot.
- Do not ignore repaint caveat for ZigZag-based divergence.

## Good outputs

```metastock
C < Ref(LLV(C,20),-1) AND MACD() > Ref(LLV(MACD(),20),-1)
Divergence(MACD(),C,5) <> 0
```

## What not to do

- Bad: `Cross(MACD(),Mov(MACD(),9,E))` as MACD divergence.
- Bad: using `Ref(C,1)` in Explorer.
- Bad: claiming ZigZag-based divergence is stable on latest bar.

## Related functions and concepts

- function.macd
- function.divergence
- function.llv
- function.hhv
- reference.zigzag_based_function_repaint_pitfall

## Retrieval keywords

MACD divergence, bullish divergence, bearish divergence, Divergence(MACD(),C,5), lower low higher MACD.

## Test Queries

- Find bullish MACD divergence
- Find stocks where price makes lower low but MACD makes higher low
