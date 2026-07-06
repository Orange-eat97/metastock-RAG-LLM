---
canonical_id: function.abs
title: Abs
type: function
card_bucket: functions
category: math
source: MetaStock Formula Primer / Formula Primer II
status: active
priority: 10
supports_explorer: true
function: Abs
aliases:
- text: Abs
  type: exact
  weight: 1.0
- text: absolute value
  type: synonym
  weight: 0.85
- text: ignore sign
  type: synonym
  weight: 0.85
- text: absolute change
  type: synonym
  weight: 0.85
- text: regardless of direction
  type: synonym
  weight: 0.85
- text: moved more than
  type: synonym
  weight: 0.85
- text: within 2 percent of
  type: synonym
  weight: 0.85
- text: close to moving average
  type: synonym
  weight: 0.85
- text: distance from moving average
  type: synonym
  weight: 0.85
- text: magnitude of movement
  type: synonym
  weight: 0.85
suggests:
- canonical_id: function.roc
  rationale: function.roc is often useful context for this card but is not always mandatory.
  priority: 40
  properties:
    source: registry_ready_transform
    formula_role: suggests
- canonical_id: reference.price_fields
  rationale: reference.price_fields is optional helper context for examples involving this function.
  priority: 40
  properties:
    source: converted_from_old_function_requires
    formula_role: suggests
semantic:
  concept_role: function
  mechanism: math
  market_object: price
  outputs:
  - numeric_value
  supports_conditions:
  - threshold_comparison
  - crossover
  - state_filter
  does_not_cover:
  - complete_trading_pattern_by_itself
registry:
  enabled: true
  canonical_id: function.abs
  supports_explorer: true
  priority: 10
  properties:
    source_notes:
    - Formula Primer: Abs(DATA ARRAY) returns the absolute value without positive or negative sign.
    source_path: functions/abs.md
    generated_schema_version: registry_ready_v2
---

# Abs

## Purpose

`Abs` returns the absolute value of a data array.

In this project, `Abs` is mainly used for Explorer filters such as:

- price moved more than a threshold regardless of direction
- close is within a percentage distance of a moving average
- distance between two series
- volatility-style filters

## Syntax

```metastock
Abs(DATA ARRAY)
```

## Common formulas

Absolute one-day percent move greater than 5 percent:

```metastock
Abs(ROC(C,1,%)) > 5
```

Distance from close to 50 MA as percent of close:

```metastock
Abs(C - Mov(C,50,S)) / C * 100
```

Close within 2 percent of 50 MA:

```metastock
Abs(C - Mov(C,50,S)) / C * 100 <= 2
```

## Natural language mappings

Use this function when the user says:

- absolute value
- absolute change
- regardless of direction
- moved more than
- within 2 percent of
- close to moving average
- distance from moving average
- ignore sign
- magnitude of movement

## Explorer column usage

Distance-to-moving-average column:

```text
Column A: C
Column B: Mov(C,50,S)
Column C: Abs(C - Mov(C,50,S)) / C * 100
Filter: ColC <= 2
```

## Explorer examples

### Example 1: Close within 2 percent of 50 MA

User request:

```text
Find stocks where close is within 2 percent of the 50 day moving average
```

Explorer output:

```text
Column A: C
Column B: Mov(C,50,S)
Column C: Abs(C - Mov(C,50,S)) / C * 100
Filter: ColC <= 2
```

### Example 2: Big one-day move

User request:

```text
Find stocks that moved more than 5 percent today regardless of direction
```

Explorer output:

```text
Column A: Abs(ROC(C,1,%))
Filter: ColA > 5
```

## What not to do

Do not use `Abs` when direction matters.

Bad for bullish price increase:

```metastock
Abs(ROC(C,1,%)) > 5
```

Correct:

```metastock
ROC(C,1,%) > 5
```

## Assumptions

- Use `Abs` when the user explicitly says “within”, “distance”, “moved more than”, or “regardless of direction”.
- For directional movement, use `ROC` or direct comparison without `Abs`.

## Related functions and concepts

- ROC: percent or point change
- Mov: distance from moving average
- ATR: volatility threshold
- Max: clamp lower bound

## Retrieval keywords

Abs, absolute value, absolute change, ignore sign, regardless of direction, moved more than, distance from moving average, close within 2 percent of MA, Abs(ROC(C,1,%)), Abs(C - Mov(C,50,S)).

## Parameters

- `DATA ARRAY`: the value or series whose absolute value should be returned.


## Valid Examples

```metastock
Abs(C - Ref(C,-1))
Abs(ROC(C,1,$))
Abs(H - L)
```


## Common Mistakes

- Do not use `Abs` to detect direction; it removes the sign.
- Do not write `Absolute(C)`; use `Abs(C)`.
- Do not use natural language like `absolute change` inside a formula.


## Related Patterns

- pattern.bollinger_band_squeeze
- pattern.consecutive_condition


## Test Queries

- Find stocks where the absolute price change is greater than 2
- Find stocks with large absolute daily range
