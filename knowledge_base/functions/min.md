---
canonical_id: function.min
title: Min
type: function
card_bucket: functions
category: math
source: MetaStock Formula Primer / Formula Primer II
status: active
priority: 10
supports_explorer: true
function: Min
aliases:
- text: Min
  type: exact
  weight: 1.0
- text: minimum
  type: exact
  weight: 1.0
- text: smallest of two values
  type: synonym
  weight: 0.85
- text: smaller of two values
  type: synonym
  weight: 0.85
- text: lesser of two values
  type: synonym
  weight: 0.85
- text: below both moving averages
  type: phrase
  weight: 0.9
- text: lowest of two calculations
  type: synonym
  weight: 0.85
- text: cap at a maximum value
  type: synonym
  weight: 0.85
- text: do not exceed a ceiling
  type: synonym
  weight: 0.85
suggests:
- canonical_id: function.max
  rationale: function.max is often useful context for this card but is not always mandatory.
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
  canonical_id: function.min
  supports_explorer: true
  priority: 10
  properties:
    source_notes:
    - Formula Primer: Min(DATA ARRAY, DATA ARRAY) returns the smallest of the two parameters.
    source_path: functions/min.md
    generated_schema_version: registry_ready_v2
---

# Min

## Purpose

`Min` returns the smaller of two values or data arrays.

In this project, `Min` is mainly used for Explorer formulas such as:

- require price below the smaller of two moving averages
- clamp a calculated value so it does not exceed a ceiling
- construct True Range together with `Max`
- simplify multiple less-than comparisons

## Syntax

```metastock
Min(DATA ARRAY, DATA ARRAY)
```

## Common formulas

Close below both 13-period and 40-period moving averages:

```metastock
C < Min(Mov(C,13,S), Mov(C,40,S))
```

True range lower part:

```metastock
Min(Ref(C,-1), L)
```

Clamp a value to 100 or below:

```metastock
Min(RSI(14), 100)
```

## Natural language mappings

Use this function when the user says:

- minimum
- min
- smaller of two values
- lesser of two values
- below both moving averages
- lowest of two calculations
- cap at a maximum value
- do not exceed a ceiling

## Explorer column usage

```text
Column A: C
Column B: Min(Mov(C,13,S), Mov(C,40,S))
Filter: ColA < ColB
```

## What not to do

Do not use `Min` as a rolling lowest value function. Use `LLV` for lookback lows.

Bad for 20-day low:

```metastock
Min(L,20)
```

Correct:

```metastock
LLV(L,20)
```

## Assumptions

- Use `Min(A,B)` for two-value comparisons.
- Use `LLV(DATA ARRAY,N)` for lowest value over a lookback period.

## Related functions and concepts

- Max: larger of two values
- LLV: rolling lowest value
- ATR: true range construction
- Mov: moving average comparisons

## Retrieval keywords

Min, minimum, smaller value, lesser of two values, below both moving averages, cap value, True Range, Min(Ref(C,-1), L), C < Min(Mov(C,13,S), Mov(C,40,S)).

## Parameters

- `DATA ARRAY 1`: first value or series to compare.
- `DATA ARRAY 2`: second value or series to compare.


## Valid Examples

```metastock
Min(L, Ref(C,-1))
Min(C, Ref(C,-1))
```


## Common Mistakes

- Do not use `Min` as a rolling lowest-low function; use `LLV(DATA ARRAY, PERIODS)` for lookback lows.
- Do not write `Minimum(C,20)`; use `Min(A,B)` or `LLV(C,20)` depending on intent.
- Do not confuse current-bar low `L` with `LLV(L,N)`.


## Related Patterns

- pattern.bollinger_band_squeeze


## Test Queries

- Use Min to compare today low and yesterday close
- Build a true range formula with Min
