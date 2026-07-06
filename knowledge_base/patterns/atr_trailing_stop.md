---
canonical_id: pattern.atr_trailing_stop
title: 'Pattern: ATR Trailing Stop'
type: pattern
card_bucket: patterns
category: stop_logic
source: generated_curated_from_primer
status: active
priority: 10
supports_explorer: true
aliases:
- text: ATR trailing stop
  type: exact
  weight: 1.0
- text: 2 ATR trailing stop
  type: phrase
  weight: 0.95
- text: close above ATR stop
  type: phrase
  weight: 0.9
- text: ATR stop level
  type: phrase
  weight: 0.9
requires:
- canonical_id: function.atr
  rationale: ATR trailing stop requires ATR as the volatility distance.
  priority: 30
  properties:
    formula_role: volatility_distance
suggests:
- canonical_id: function.hhv
  rationale: Long-side trailing stop often anchors to a recent high.
  priority: 30
  properties:
    formula_role: long_stop_anchor
- canonical_id: function.llv
  rationale: Short-side trailing stop often anchors to a recent low.
  priority: 30
  properties:
    formula_role: short_stop_anchor
semantic:
  concept_role: pattern
  mechanism: stop_logic
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
  canonical_id: pattern.atr_trailing_stop
  supports_explorer: true
  priority: 10
  properties:
    formula_role: stop_logic
    source_path: patterns/atr_trailing_stop.md
    curation_level: upgraded_to_curated_quality
---

# Pattern: ATR Trailing Stop

## Intent

Represent an Explorer-friendly ATR stop or trailing-stop proxy. This card does not implement a full position-aware System Tester trailing stop. It gives scan formulas such as close above a recent-high-minus-ATR stop level.

## Natural Language Triggers

- ATR trailing stop
- 2 ATR stop
- close above ATR stop
- price below ATR stop
- volatility stop
- ATR based stop

## Keywords

- ATR trailing stop
- ATR stop
- 2 ATR
- HHV minus ATR
- LLV plus ATR

## Required Logical Components

- Choose long-side or short-side stop.
- Choose anchor such as recent highest high or recent lowest low.
- Choose ATR period and multiplier.
- Compare current price against the stop level.

## Optional Confirmation Components

- Trend confirmation, such as close above a moving average.
- Volume confirmation, such as `V > Mov(V,20,S)`.
- Momentum confirmation, such as RSI, MACD, or ROC improving.
- Recency confirmation using `BarsSince()` when the user asks for recent signals.

## Formula Building Blocks

```metastock
HHV(H,20) - 2 * ATR(14)
LLV(L,20) + 2 * ATR(14)
C > HHV(H,20) - 2 * ATR(14)
C < LLV(L,20) + 2 * ATR(14)
```

## Composition Guidance

- For long-side stop proxy, use recent high minus ATR multiple.
- For short-side stop proxy, use recent low plus ATR multiple.
- State that this is not a true trade-state trailing stop unless used in System Tester with position logic.
- If the user gives multiplier or period, use those values.

## Example Compositions

### Close above 2 ATR long stop proxy

User request:

```text
Find stocks where close is above a 2 ATR trailing stop
```

Explorer output:

```text
Column A: C
Column B: HHV(H,20) - 2 * ATR(14)
Filter: ColA > ColB
```
### Close below 3 ATR short stop proxy

User request:

```text
Find stocks where close is below a 3 ATR short stop
```

Explorer output:

```text
Column A: C
Column B: LLV(L,20) + 3 * ATR(14)
Filter: ColA < ColB
```

## Observable Outputs

Useful Explorer columns:

- Current close
- ATR value
- ATR stop level
- Distance from stop

## Default Assumptions

- Default ATR period is 14.
- Default anchor lookback is 20 if unspecified.
- Long-side default stop is `HHV(H,20)-2*ATR(14)`.

## Pitfalls

- Do not claim this is a fully position-aware trailing stop in Explorer.
- Do not use future references to know later highs/lows.
- Do not use System Tester-only simulation functions in Explorer.

## Good outputs

```metastock
C > HHV(H,20) - 2 * ATR(14)
C < LLV(L,20) + 2 * ATR(14)
```

## What not to do

- Bad: `Simulation.EntryPrice` in Explorer.
- Bad: `ATRTrailingStop(14,2)` invented function.
- Bad: using `Ref(C,1)` for future confirmation.

## Related functions and concepts

- function.atr
- function.hhv
- function.llv
- reference.system_tester_vs_explorer_limits

## Retrieval keywords

ATR trailing stop, ATR stop, 2 ATR, HHV minus ATR, LLV plus ATR.

## Test Queries

- Find stocks where close is above a 2 ATR trailing stop
