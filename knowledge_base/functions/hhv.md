---
type: function
function: HHV
category: highest_lowest
source: MetaStock Formula Primer / Formula Primer II
priority: high
status: draft
---

# HHV

## Purpose

`HHV` returns the highest value of a data array over a lookback period.

In this project, `HHV` is mainly used for Explorer filters such as:

- close makes a new high
- high breaks above recent high
- 20 day breakout
- highest close over 50 periods
- price near recent high

## Syntax

```metastock
HHV(DATA ARRAY, PERIODS)
```

## Parameters

| Parameter | Meaning | Common values |
|---|---|---|
| DATA ARRAY | Data series to evaluate | H, C, V, RSI(14) |
| PERIODS | Lookback period | 20, 40, 50, 100, 252 |

## Common formulas

Highest high over 20 periods:

```metastock
HHV(H,20)
```

Highest close over 50 periods:

```metastock
HHV(C,50)
```

Current high is a 20-period high:

```metastock
H = HHV(H,20)
```

Close breaks above previous 20-period highest close:

```metastock
C > Ref(HHV(C,20),-1)
```

High breaks above previous 40-period high:

```metastock
H > Ref(HHV(H,40),-1)
```

## Natural language mappings

Use this function when the user says:

- highest high
- highest close
- recent high
- new high
- 20 day high
- 52 week high
- breakout
- price breakout
- close makes new high
- high above recent high
- resistance breakout

## Explorer column usage

Close at 50-period high:

```text
Column A: C
Column B: HHV(C,50)
Filter: ColA = ColB
```

Close breaks above previous 20-period high:

```text
Column A: C
Column B: Ref(HHV(C,20),-1)
Filter: ColA > ColB
```

## Explorer examples

### Example 1: New 20-day high

User request:

```text
Find stocks making a new 20 day high
```

Explorer output:

```text
Column A: H
Column B: HHV(H,20)
Filter: ColA = ColB
```

### Example 2: Close breaks above previous 50-day high

User request:

```text
Find stocks where close breaks above the previous 50 day high
```

Explorer output:

```text
Column A: C
Column B: Ref(HHV(C,50),-1)
Filter: ColA > ColB
```

### Example 3: 40-bar pivot high style signal

User request:

```text
Find stocks where high is above the previous 40 bar highest high
```

Explorer output:

```text
Column A: H
Column B: Ref(HHV(H,40),-1)
Filter: ColA > ColB
```

## Good outputs

Good:

```metastock
HHV(H,20)
```

Good:

```metastock
C > Ref(HHV(C,20),-1)
```

## What not to do

Do not invent function names.

Bad:

```metastock
HighestHigh(H,20)
```

Correct:

```metastock
HHV(H,20)
```

Do not confuse `HHV` with `H`.

Bad:

```metastock
C > H(20)
```

Correct:

```metastock
C > HHV(H,20)
```

Be careful when comparing against the current lookback high. This can include the current bar.

For a breakout above the previous high, prefer:

```metastock
C > Ref(HHV(C,20),-1)
```

instead of:

```metastock
C > HHV(C,20)
```

because the second formula is usually impossible when the current close is included in the `HHV` calculation.

## Assumptions

- “New high” can mean current value equals the lookback highest value.
- “Breaks above previous high” should usually use `Ref(HHV(...),-1)`.
- If the user says “price breakout” without specifying price type, use close `C`.
- If the user says “highest high”, use `H`.
- If the user says “highest close”, use `C`.

## Related functions and concepts

- LLV: lowest value
- Ref: previous lookback value
- Cross: breakout event
- C: close price
- H: high price

## Retrieval keywords

HHV, highest high, highest value, new high, recent high, breakout, price breakout, 20 day high, 50 day high, 52 week high, resistance breakout.
