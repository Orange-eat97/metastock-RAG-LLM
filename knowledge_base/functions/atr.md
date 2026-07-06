---
type: function
function: ATR
category: volatility
source: MetaStock Formula Primer / Formula Primer II
priority: 10
status: active
aliases:
- ATR
- average true range
- true range volatility
requires:
- reference.price_fields
suggests:
- function.mov
- function.ref
- function.max
- function.min
registry:
  supports_explorer: true
  priority: 25
  properties:
    source_notes:
    - Formula Primer: atr(PERIODS) calculates Average True Range.
    - Formula Primer II: True Range can be expressed with max(H,Ref(C,-1)) - min(Ref(C,-1),L).
  enabled: true
---

# ATR

## Purpose

`ATR` calculates Average True Range, a volatility indicator.

In this project, `ATR` is mainly used for Explorer filters such as:

- high volatility stocks
- low volatility stocks
- price move larger than ATR
- breakout range greater than volatility threshold
- ATR-based stop or distance calculations

## Syntax

```metastock
ATR(PERIODS)
```

## Common formulas

14-period ATR:

```metastock
ATR(14)
```

Close-to-close move greater than one ATR:

```metastock
Abs(C - Ref(C,-1)) > ATR(14)
```

Daily range greater than ATR:

```metastock
(H - L) > ATR(14)
```

ATR as percent of close:

```metastock
ATR(14) / C * 100
```

Custom true range building block:

```metastock
Max(H, Ref(C,-1)) - Min(Ref(C,-1), L)
```

## Natural language mappings

Use this function when the user says:

- ATR
- average true range
- true range
- volatility
- high volatility
- low volatility
- range greater than ATR
- price move larger than ATR
- ATR stop
- volatility filter

## Explorer column usage

Volatility column:

```text
Column A: ATR(14)
Column B: ATR(14) / C * 100
Filter: ColB > 3
```

## Explorer examples

### Example 1: High volatility stocks

User request:

```text
Find stocks where 14 day ATR is more than 3 percent of close
```

Explorer output:

```text
Column A: C
Column B: ATR(14)
Column C: ATR(14) / C * 100
Filter: ColC > 3
```

### Example 2: Large daily range

User request:

```text
Find stocks where today's range is greater than 14 day ATR
```

Explorer output:

```text
Column A: H - L
Column B: ATR(14)
Filter: ColA > ColB
```

## What not to do

Do not invent `AverageTrueRange(14)`.

Correct:

```metastock
ATR(14)
```

Do not use ATR alone as a bullish or bearish signal. ATR measures volatility, not direction.

## Assumptions

- If the user says ATR without a period, use `ATR(14)`.
- If the user asks for ATR percent, use `ATR(14) / C * 100`.
- ATR is a volatility filter and should usually be combined with a directional condition.

## Related functions and concepts

- Abs: absolute price movement
- Ref: previous close
- Max: true range construction
- Min: true range construction
- Mov: custom ATR variants

## Retrieval keywords

ATR, average true range, true range, volatility, high volatility, low volatility, ATR percent, volatility filter, range greater than ATR, ATR(14), Abs(C - Ref(C,-1)) > ATR(14).

## Parameters

- `PERIODS`: number of periods used to calculate Average True Range, commonly `14`.


## Valid Examples

```metastock
ATR(14)
C > Mov(C,50,S) AND ATR(14) > Mov(ATR(14),20,S)
```


## Common Mistakes

- Do not write `ATR(C,14)`; `ATR` only takes the period argument.
- Do not confuse ATR with Bollinger Bands; ATR is a volatility value, not an upper/lower price band.
- Do not use `AverageTrueRange(14)`; use `ATR(14)`.


## Related Patterns

- pattern.ma_support_bounce
- pattern.bollinger_band_squeeze


## Test Queries

- Find stocks where ATR is above its 20 day average
- Find volatile stocks using 14 day ATR
