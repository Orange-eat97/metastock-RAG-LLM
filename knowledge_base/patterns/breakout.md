---
type: pattern
card_bucket: patterns
category: breakout
source: MetaStock Formula Primer / Formula Primer II / internal project pattern
priority: high
status: active
functions:
  - HHV
  - LLV
  - Ref
fields:
  - C
  - H
  - L
keywords:
  - breakout
  - breakdown
  - resistance breakout
  - support breakdown
  - new high
  - new low
  - previous high
  - previous low
  - close above previous high
  - close below previous low
  - HHV
  - LLV
  - Ref(HHV)
  - Ref(LLV)
---

# Pattern: Breakout

## Intent

Detect stocks where price breaks above a recent prior high, or breaks below a recent prior low.

This pattern is used when the user describes a breakout, resistance breakout, new high breakout, support breakdown, or new low breakdown.

## Natural Language Triggers

- breakout
- price breakout
- breaks above recent high
- breaks above previous high
- close above previous high
- new high breakout
- resistance breakout
- high breaks above previous high
- breakdown
- support breakdown
- breaks below recent low
- close below previous low
- new low breakdown

## Keywords

- breakout
- breakdown
- resistance breakout
- support breakdown
- new high
- new low
- previous high
- previous low
- recent high
- recent low
- close breakout
- high breakout
- close breakdown
- low breakdown
- HHV
- LLV
- Ref
- Ref(HHV)
- Ref(LLV)
- C > Ref(HHV(C,N),-1)
- H > Ref(HHV(H,N),-1)
- C < Ref(LLV(C,N),-1)
- L < Ref(LLV(L,N),-1)

## Required Logical Components

1. Choose breakout direction:
   - bullish breakout above prior high
   - bearish breakdown below prior low
2. Choose price field:
   - close `C` for close-based breakout
   - high `H` for intrabar high breakout
   - low `L` for intrabar low breakdown
3. Define the prior lookback boundary:
   - previous highest value for breakout
   - previous lowest value for breakdown
4. Compare current price field against the prior boundary.

## Optional Confirmation Components

- Volume confirmation:
  - current volume above average volume
- Trend confirmation:
  - price above a moving average
  - short moving average above long moving average
- Momentum confirmation:
  - RSI improving
  - rate of change positive
- Close confirmation:
  - use close `C` instead of high `H` for stricter breakout confirmation

## Formula Building Blocks

Bullish close breakout boundary:

```metastock
Ref(HHV(C,N),-1)
```

Bullish high breakout boundary:

```metastock
Ref(HHV(H,N),-1)
```

Bearish close breakdown boundary:

```metastock
Ref(LLV(C,N),-1)
```

Bearish low breakdown boundary:

```metastock
Ref(LLV(L,N),-1)
```

Bullish close breakout condition:

```metastock
C > Ref(HHV(C,N),-1)
```

Bullish high breakout condition:

```metastock
H > Ref(HHV(H,N),-1)
```

Bearish close breakdown condition:

```metastock
C < Ref(LLV(C,N),-1)
```

Bearish low breakdown condition:

```metastock
L < Ref(LLV(L,N),-1)
```

## Composition Guidance

- If the user says breakout without specifying direction, assume bullish breakout.
- If the user says breakout without specifying price field, use close `C` for confirmation.
- If the user says high breakout, use `H > Ref(HHV(H,N),-1)`.
- If the user says close breakout, use `C > Ref(HHV(C,N),-1)`.
- If the user says breakdown or support breakdown, use the corresponding `LLV` condition.
- If the user says previous high or previous low, exclude the current bar by using `Ref(HHV(...),-1)` or `Ref(LLV(...),-1)`.
- If the user asks for volume confirmation, combine this breakout pattern with the volume-above-average pattern using `AND`.
- If the user asks for both bullish and bearish breakouts, combine the bullish and bearish conditions using `OR`.

## Example Compositions

20-period close breakout:

```metastock
C > Ref(HHV(C,20),-1)
```

50-period high breakout:

```metastock
H > Ref(HHV(H,50),-1)
```

20-period close breakdown:

```metastock
C < Ref(LLV(C,20),-1)
```

20-period low breakdown:

```metastock
L < Ref(LLV(L,20),-1)
```

Close breakout with volume confirmation:

```metastock
C > Ref(HHV(C,20),-1) AND V > Mov(V,20,S)
```

## Observable Outputs

Useful values to expose as Explorer columns:

- Current close: `C`
- Current high: `H`
- Current low: `L`
- Prior highest close: `Ref(HHV(C,N),-1)`
- Prior highest high: `Ref(HHV(H,N),-1)`
- Prior lowest close: `Ref(LLV(C,N),-1)`
- Prior lowest low: `Ref(LLV(L,N),-1)`
- Current volume: `V`
- Average volume: `Mov(V,20,S)`

Column selection guidance:

- Include only columns relevant to the final filter.
- Prefer columns that explain why the stock passed the breakout or breakdown condition.
- For a close breakout, show `C` and the prior highest close.
- For a high breakout, show `H` and the prior highest high.
- For a volume-confirmed breakout, show `V` and average volume.

## Pitfalls

- Do not compare current close to `HHV(C,N)` when the user asks for a previous N-period high, because `HHV(C,N)` includes the current bar.
- Do not simplify a previous-high breakout to `C > HHV(C,N)`.
- Prefer `C > Ref(HHV(C,N),-1)` for a close breakout above the previous N-period highest close.
- Prefer `H > Ref(HHV(H,N),-1)` for a high breakout above the previous N-period highest high.
- Do not use future references in Explorer scans.
- Do not use `Ref(HHV(H,N),1)` for a breakout scan.
- Do not use `Cross` unless the user specifically asks for a crossover event.

## Default Assumptions

- If the user says breakout without defining the price field, use close `C`.
- If the user says high breakout, use high `H`.
- If the user says breakdown without defining the price field, use close `C`.
- If the user says low breakdown, use low `L`.
- If the user says previous high or previous low, exclude the current bar with `Ref(...,-1)`.
- If the user says recent high or recent low without a period, use 20 periods as a common first version.

## Source Notes

- `HHV(DATA ARRAY, PERIODS)` returns the highest value over the most recent periods and includes the current period.
- `LLV(DATA ARRAY, PERIODS)` returns the lowest value over the most recent periods and includes the current period.
- `Ref(DATA ARRAY, PERIODS)` is used to reference previous or future bars; negative periods reference prior bars.
