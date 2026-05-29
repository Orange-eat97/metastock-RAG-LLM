---
type: function
function: LLV
category: highest_lowest
source: MetaStock Formula Primer
priority: high
status: draft
---

# LLV

## Purpose

`LLV` returns the lowest value of a data array over a lookback period.

In this project, `LLV` is mainly used for Explorer filters such as:

- close makes a new low
- low breaks below recent low
- 20 day breakdown
- lowest close over 50 periods
- price near recent low

## Syntax

```metastock
LLV(DATA ARRAY, PERIODS)
```

## Parameters

| Parameter | Meaning | Common values |
|---|---|---|
| DATA ARRAY | Data series to evaluate | L, C, V, RSI(14) |
| PERIODS | Lookback period | 20, 40, 50, 100, 252 |

## Common formulas

Lowest low over 20 periods:

```metastock
LLV(L,20)
```

Lowest close over 50 periods:

```metastock
LLV(C,50)
```

Current low is a 20-period low:

```metastock
L = LLV(L,20)
```

Close breaks below previous 20-period lowest close:

```metastock
C < Ref(LLV(C,20),-1)
```

Low breaks below previous 40-period low:

```metastock
L < Ref(LLV(L,40),-1)
```

## Natural language mappings

Use this function when the user says:

- lowest low
- lowest close
- recent low
- new low
- 20 day low
- 52 week low
- breakdown
- price breakdown
- close makes new low
- low below recent low
- support breakdown

## Explorer column usage

Close at 50-period low:

```text
Column A: C
Column B: LLV(C,50)
Filter: ColA = ColB
```

Close breaks below previous 20-period low:

```text
Column A: C
Column B: Ref(LLV(C,20),-1)
Filter: ColA < ColB
```

## Explorer examples

### Example 1: New 20-day low

User request:

```text
Find stocks making a new 20 day low
```

Explorer output:

```text
Column A: L
Column B: LLV(L,20)
Filter: ColA = ColB
```

### Example 2: Close breaks below previous 50-day low

User request:

```text
Find stocks where close breaks below the previous 50 day low
```

Explorer output:

```text
Column A: C
Column B: Ref(LLV(C,50),-1)
Filter: ColA < ColB
```

## Good outputs

Good:

```metastock
LLV(L,20)
```

Good:

```metastock
C < Ref(LLV(C,20),-1)
```

## What not to do

Do not invent function names.

Bad:

```metastock
LowestLow(L,20)
```

Correct:

```metastock
LLV(L,20)
```

Do not confuse `LLV` with `L`.

Bad:

```metastock
C < L(20)
```

Correct:

```metastock
C < LLV(L,20)
```

Be careful when comparing against the current lookback low. This can include the current bar.

For a breakdown below the previous low, prefer:

```metastock
C < Ref(LLV(C,20),-1)
```

instead of:

```metastock
C < LLV(C,20)
```

because the second formula is usually impossible when the current close is included in the `LLV` calculation.

## Assumptions

- “New low” can mean current value equals the lookback lowest value.
- “Breaks below previous low” should usually use `Ref(LLV(...),-1)`.
- If the user says “price breakdown” without specifying price type, use close `C`.
- If the user says “lowest low”, use `L`.
- If the user says “lowest close”, use `C`.

## Related functions and concepts

- HHV: highest value
- Ref: previous lookback value
- Cross: crossover/breakdown event
- C: close price
- L: low price

## Retrieval keywords

LLV, lowest low, lowest value, new low, recent low, breakdown, price breakdown, 20 day low, 50 day low, 52 week low, support breakdown.
