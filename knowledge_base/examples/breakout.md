---
type: pattern
category: breakout
source: MetaStock Formula Primer II / internal project pattern
priority: high
status: draft
---

# Breakout

## Purpose

This pattern finds stocks breaking above a recent high or below a recent low.

It commonly uses `HHV`, `LLV`, and `Ref`.

## Bullish breakout pattern

Close breaks above the previous N-period highest close:

```metastock
C > Ref(HHV(C,N),-1)
```

High breaks above the previous N-period highest high:

```metastock
H > Ref(HHV(H,N),-1)
```

## Bearish breakdown pattern

Close breaks below the previous N-period lowest close:

```metastock
C < Ref(LLV(C,N),-1)
```

Low breaks below the previous N-period lowest low:

```metastock
L < Ref(LLV(L,N),-1)
```

## Natural language mappings

Use this pattern when the user says:

- breakout
- price breakout
- breaks above recent high
- close above previous high
- new high breakout
- resistance breakout
- breakdown
- support breakdown
- breaks below recent low
- close below previous low

## Explorer examples

### Example 1: 20-day close breakout

User request:

```text
Find stocks where close breaks above the previous 20 day highest close
```

Explorer output:

```text
Column A: C
Column B: Ref(HHV(C,20),-1)
Filter: ColA > ColB
```

### Example 2: 50-day high breakout

User request:

```text
Find stocks where high breaks above the previous 50 day high
```

Explorer output:

```text
Column A: H
Column B: Ref(HHV(H,50),-1)
Filter: ColA > ColB
```

### Example 3: 20-day close breakdown

User request:

```text
Find stocks where close breaks below the previous 20 day lowest close
```

Explorer output:

```text
Column A: C
Column B: Ref(LLV(C,20),-1)
Filter: ColA < ColB
```

## What not to do

Do not compare close to `HHV(C,N)` using `>` when the current bar is included in the `HHV` calculation.

Bad:

```metastock
C > HHV(C,20)
```

Better:

```metastock
C > Ref(HHV(C,20),-1)
```

Do not use future references for Explorer scans.

Bad:

```metastock
H > Ref(HHV(H,40),1)
```

Correct:

```metastock
H > Ref(HHV(H,40),-1)
```

## Assumptions

- If the user says breakout without defining the price field, use close `C`.
- If the user says high breakout, use `H`.
- If the user says previous high, use `Ref(HHV(...),-1)`.
- If the user says new high, equality to current `HHV` may be acceptable.

## Related functions and concepts

- HHV: highest value
- LLV: lowest value
- Ref: previous lookback high/low
- C: close
- H: high
- L: low

## Retrieval keywords

breakout, breakdown, resistance breakout, support breakdown, new high, new low, previous high, previous low, HHV, LLV, Ref(HHV), Ref(LLV).
