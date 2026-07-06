---
type: function
function: Max
category: math
source: MetaStock Formula Primer / Formula Primer II
priority: 10
status: active
aliases:
- maximum
- largest of two values
requires:
- reference.price_fields
suggests:
- function.min
registry:
  supports_explorer: true
  priority: 30
  properties:
    source_notes:
    - Formula Primer: Max(DATA ARRAY, DATA ARRAY) returns the largest of the two parameters.
  enabled: true
---

# Max

## Purpose

`Max` returns the larger of two values or data arrays.

In this project, `Max` is mainly used for Explorer formulas such as:

- require price above the larger of two moving averages
- clamp a calculated value so it does not go below a floor
- construct True Range together with `Min`
- simplify multiple greater-than comparisons

## Syntax

```metastock
Max(DATA ARRAY, DATA ARRAY)
```

## Common formulas

Close above both 13-period and 40-period moving averages:

```metastock
C > Max(Mov(C,13,S), Mov(C,40,S))
```

True range upper part:

```metastock
Max(H, Ref(C,-1))
```

Clamp a value to zero or above:

```metastock
Max(ROC(C,1,$), 0)
```

## Natural language mappings

Use this function when the user says:

- maximum
- max
- larger of two values
- greater of two values
- above both moving averages
- highest of two calculations
- clamp to at least zero
- do not go below zero

## Explorer column usage

```text
Column A: C
Column B: Max(Mov(C,13,S), Mov(C,40,S))
Filter: ColA > ColB
```

## What not to do

Do not use `Max` as a rolling highest value function. Use `HHV` for lookback highs.

Bad for 20-day high:

```metastock
Max(H,20)
```

Correct:

```metastock
HHV(H,20)
```

## Assumptions

- Use `Max(A,B)` for two-value comparisons.
- Use `HHV(DATA ARRAY,N)` for highest value over a lookback period.

## Related functions and concepts

- Min: smaller of two values
- HHV: rolling highest value
- ATR: true range construction
- Mov: moving average comparisons

## Retrieval keywords

Max, maximum, larger value, greater of two values, above both moving averages, clamp minimum, True Range, Max(H, Ref(C,-1)), C > Max(Mov(C,13,S), Mov(C,40,S)).

## Parameters

- `DATA ARRAY 1`: first value or series to compare.
- `DATA ARRAY 2`: second value or series to compare.


## Valid Examples

```metastock
Max(H - L, Abs(H - Ref(C,-1)))
Max(C, Ref(C,-1))
```


## Common Mistakes

- Do not use `Max` as a rolling highest-high function; use `HHV(DATA ARRAY, PERIODS)` for lookback highs.
- Do not pass a period as the second argument unless that period is actually a value to compare.
- Do not write `Maximum(C,20)`; use `Max(A,B)` or `HHV(C,20)` depending on intent.


## Related Patterns

- pattern.bollinger_band_squeeze


## Test Queries

- Use Max to compare today high and yesterday close
- Build a true range formula with Max
