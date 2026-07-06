---
type: function
function: Min
category: math
source: MetaStock Formula Primer / Formula Primer II
priority: 10
status: active
aliases:
- minimum
- smallest of two values
requires:
- reference.price_fields
suggests:
- function.max
registry:
  supports_explorer: true
  priority: 30
  properties:
    source_notes:
    - Formula Primer: Min(DATA ARRAY, DATA ARRAY) returns the smallest of the two
        parameters.
  enabled: true
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
