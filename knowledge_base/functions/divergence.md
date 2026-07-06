---
canonical_id: function.divergence
title: Divergence
type: function
card_bucket: functions
category: zigzag_based
source: generated_curated_from_primer
status: active
priority: 10
supports_explorer: true
function: Divergence
aliases:
- text: Divergence
  type: exact
  weight: 1.0
- text: indicator divergence
  type: phrase
  weight: 0.95
- text: RSI divergence function
  type: phrase
  weight: 0.9
- text: MACD divergence function
  type: phrase
  weight: 0.9
suggests:
- canonical_id: reference.zigzag_based_function_repaint_pitfall
  rationale: ZigZag-based functions have uncertain current values and repaint risk.
  priority: 30
  properties:
    formula_role: repaint_warning
semantic:
  concept_role: function
  mechanism: zigzag_based
  market_object: price
  outputs:
  - indicator_series
  supports_conditions:
  - threshold_comparison
  - crossover
  - state_filter
  does_not_cover:
  - complete_trading_pattern_by_itself
registry:
  enabled: true
  canonical_id: function.divergence
  supports_explorer: true
  priority: 10
  properties:
    formula_role: zigzag_based
    source_path: functions/divergence.md
    curation_level: upgraded_to_curated_quality
---

# Divergence

## Purpose

Compares two data arrays using ZigZag-based movement and returns a value indicating divergence or convergence. Because it is ZigZag-based, the most recent signal can change.

## Syntax

```metastock
Divergence(DATA ARRAY 1, DATA ARRAY 2, % MINIMUM CHANGE)
```

## Parameters

| Parameter | Meaning | Common values |
|---|---|---|
| Nth | Which historical peak/trough, if applicable. | `1`, `2` |
| DATA ARRAY | Series to evaluate. | `C`, `H`, `L`, `RSI(14)` |
| MINIMUM CHANGE | Reversal threshold. | `5`, `10` |
| DIFF_METHOD | For `Zig`, use percent or points. | `%`, `$` |

## Default interpretation

Use percent minimum change when the user says percent. Use `5` percent as an example only when the user does not specify and the card is being used for a generic draft. Always surface the repaint/uncertain-last-leg assumption.

## Common formulas

```metastock
Divergence(RSI(14),C,5)
Divergence(MACD(),C,5) = 1
```

## Natural language mappings

Use this function when the user says:

- indicator divergence
- RSI divergence
- MACD divergence
- ZigZag divergence

## Explorer column usage

Use only when the user explicitly asks for divergence and accepts ZigZag-based behavior. For transparent divergence logic, prefer dedicated pattern cards that define price/indicator pivots.

## Explorer examples

### Example 1: Divergence example

User request:

```text
Find stocks using Divergence with 5 percent swings
```

Explorer output:

```text
Column A: Divergence(RSI(14),C,5)
Filter: ColA > 0
```

## Filter-only usage

If the user only needs a pass/fail condition and does not need to inspect intermediate values, the function may be used directly in the Filter. For this project, prefer columns when the value helps the result table or when a pattern has multiple logical components.

## Valid Examples

```metastock
Divergence(RSI(14),C,5)
Divergence(MACD(),C,5) = 1
```

## Common Mistakes

- Bad: assuming +1 always means bullish without checking argument order.
- Bad: ignoring ZigZag repaint risk.
- Bad: substituting Divergence for a simple crossover.

## Assumptions

- ZigZag-based values can change as new data arrives.
- Use only when the user explicitly asks for swing/ZigZag-style logic.
- For fixed lookback highs/lows, prefer HHV/LLV instead.

## Related Patterns

- reference.zigzag_based_function_repaint_pitfall
- pattern.zigzag_swing_reversal

## Related functions and concepts

- Explorer columns and filters
- Price fields such as `C`, `H`, `L`, `O`, and `V`
- `Cross` when the user asks for a crossing event
- `Ref` when the user asks for previous-bar or prior-event logic



## Retrieval keywords

Divergence, ZigZag, swing, repaint, minimum change.

## Test Queries

- Find stocks using Divergence with 5 percent ZigZag swings
