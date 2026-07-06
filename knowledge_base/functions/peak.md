---
canonical_id: function.peak
title: Peak
type: function
card_bucket: functions
category: zigzag_based
source: generated_curated_from_primer
status: active
priority: 10
supports_explorer: true
function: Peak
aliases:
- text: Peak
  type: exact
  weight: 1.0
- text: peak value
  type: phrase
  weight: 0.95
- text: last ZigZag peak
  type: phrase
  weight: 0.9
- text: previous peak
  type: phrase
  weight: 0.85
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
  canonical_id: function.peak
  supports_explorer: true
  priority: 10
  properties:
    formula_role: zigzag_based
    source_path: functions/peak.md
    curation_level: upgraded_to_curated_quality
---

# Peak

## Purpose

Returns the value of a ZigZag-based peak. Useful for historical resistance-style swing levels, but the most recent peak can change.

## Syntax

```metastock
Peak(Nth, DATA ARRAY, % MINIMUM CHANGE)
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
Peak(1,H,5)
C > Peak(1,H,5)
Peak(2,H,5)
```

## Natural language mappings

Use this function when the user says:

- peak value
- previous peak
- last swing high
- ZigZag peak
- historical peak

## Explorer column usage

Use Peak in Explorer only with repaint caveats. For non-ZigZag recent highs, prefer `HHV` and `Ref(HHV(...),-1)`.

## Explorer examples

### Example 1: Peak example

User request:

```text
Find stocks using Peak with 5 percent swings
```

Explorer output:

```text
Column A: Peak(1,H,5)
Filter: ColA > 0
```

## Filter-only usage

If the user only needs a pass/fail condition and does not need to inspect intermediate values, the function may be used directly in the Filter. For this project, prefer columns when the value helps the result table or when a pattern has multiple logical components.

## Valid Examples

```metastock
Peak(1,H,5)
C > Peak(1,H,5)
Peak(2,H,5)
```

## Common Mistakes

- Bad: using Peak when user asks for a fixed 20-day high. Use HHV instead.
- Bad: ignoring ZigZag repaint risk.
- Bad: omitting Nth or minimum change.

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

Peak, ZigZag, swing, repaint, minimum change.

## Test Queries

- Find stocks using Peak with 5 percent ZigZag swings
