---
canonical_id: function.zig
title: Zig
type: function
card_bucket: functions
category: zigzag_based
source: generated_curated_from_primer
status: active
priority: 10
supports_explorer: true
function: Zig
aliases:
- text: Zig
  type: exact
  weight: 1.0
- text: Zig Zag
  type: synonym
  weight: 0.95
- text: ZigZag
  type: synonym
  weight: 0.95
- text: zigzag reversal
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
  canonical_id: function.zig
  supports_explorer: true
  priority: 10
  properties:
    formula_role: zigzag_based
    source_path: functions/zig.md
    curation_level: upgraded_to_curated_quality
---

# Zig

## Purpose

Zig Zag indicator on a data array. It filters moves smaller than the minimum change and redraws the most recent leg as new data arrives. It is useful for historical swing structure but risky for current-bar buy/sell signals.

## Syntax

```metastock
Zig(DATA ARRAY, MINIMUM CHANGE, DIFF_METHOD)
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
Zig(C,5,%)
Zig(C,10,%)
Cross(C,Zig(C,5,%))
```

## Natural language mappings

Use this function when the user says:

- Zig Zag
- ZigZag
- swing reversal
- minimum change reversal
- zigzag trend

## Explorer column usage

Use Zig as a visual or historical swing column only when the user explicitly asks for ZigZag. Prefer non-repainting alternatives for live Explorer scans.

## Explorer examples

### Example 1: Zig example

User request:

```text
Find stocks using Zig with 5 percent swings
```

Explorer output:

```text
Column A: Zig(C,5,%)
Filter: ColA > 0
```

## Filter-only usage

If the user only needs a pass/fail condition and does not need to inspect intermediate values, the function may be used directly in the Filter. For this project, prefer columns when the value helps the result table or when a pattern has multiple logical components.

## Valid Examples

```metastock
Zig(C,5,%)
Zig(C,10,%)
Cross(C,Zig(C,5,%))
```

## Common Mistakes

- Bad: treating the last ZigZag value as final.
- Bad: using Zig for current buy/sell decisions without a repaint warning.
- Bad: omitting diff method `%` or `$`.

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

Zig, ZigZag, swing, repaint, minimum change.

## Test Queries

- Find stocks using Zig with 5 percent ZigZag swings
