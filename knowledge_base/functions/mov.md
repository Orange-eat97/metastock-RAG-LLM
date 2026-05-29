---
type: function
function: Mov
category: moving_average
source: MetaStock Formula Primer
priority: high
status: patched
---

# Mov

## Purpose

`Mov` calculates a moving average of a data array.

In this project, `Mov` is mainly used for Explorer filters such as:

- price above or below a moving average
- close above 20-day or 50-day moving average
- fast moving average crossing above slow moving average
- volume above average volume
- moving average trend filters

## Syntax

```metastock
Mov(DATA ARRAY, PERIODS, METHOD)
```

## Parameters

| Parameter | Meaning | Common values |
|---|---|---|
| DATA ARRAY | The price, volume, indicator, or formula series to average | `C`, `H`, `L`, `O`, `V`, `RSI(14)`, `MACD()` |
| PERIODS | Number of periods used in the average | `10`, `20`, `50`, `100`, `200` |
| METHOD | Moving average method | `S`, `E`, `W`, `T`, `TRI`, `VAR`, `VOL` |

## Common method abbreviations

```text
S   = Simple
E   = Exponential
W   = Weighted
T   = Time Series
TRI = Triangular
VAR = Variable
VOL = Volume Adjusted
```

## Default interpretation

If the user says “moving average” or “MA” without specifying the method, use simple moving average:

```metastock
Mov(C,50,S)
```

If the user says “exponential moving average” or “EMA”, use:

```metastock
Mov(C,50,E)
```

If the user says “fast moving average” but gives no period, use 20 periods.

If the user says “slow moving average” but gives no period, use 50 periods.

## Common formulas

20-period simple moving average of close:

```metastock
Mov(C,20,S)
```

50-period simple moving average of close:

```metastock
Mov(C,50,S)
```

20-period exponential moving average of close:

```metastock
Mov(C,20,E)
```

20-period average volume:

```metastock
Mov(V,20,S)
```

9-period exponential moving average of MACD:

```metastock
Mov(MACD(),9,E)
```

## Natural language mappings

Use this function when the user says:

- moving average
- simple moving average
- exponential moving average
- weighted moving average
- MA
- SMA
- EMA
- WMA
- 20 day moving average
- 50 day moving average
- 200 day moving average
- 20 day average
- 50 day average
- average price
- average close
- average volume
- volume average
- moving average of volume
- price above moving average
- price below moving average
- close above moving average
- close below moving average
- close above 20 day moving average
- close above 50 day moving average
- close above MA50
- close below MA50
- fast moving average
- slow moving average
- fast MA
- slow MA
- short moving average
- long moving average
- moving average crossover
- MA crossover
- fast MA crosses above slow MA
- fast moving average crosses above slow moving average
- bullish moving average crossover
- bearish moving average crossover

## Explorer column usage

If the user wants to inspect both price and moving average values, define them as Explorer columns.

Example:

```text
Column A: C
Column B: Mov(C,50,S)
Filter: ColA > ColB
```

If the user wants a moving average crossover, define each moving average as a column.

Example:

```text
Column A: Mov(C,20,S)
Column B: Mov(C,50,S)
Filter: Cross(ColA, ColB)
```

## Explorer examples

### Example 1: Close above 50 day moving average

User request:

```text
Find stocks where close is above 50 day moving average
```

Explorer output:

```text
Column A: C
Column B: Mov(C,50,S)
Filter: ColA > ColB
```

Notes:

```text
C means close price.
50 day moving average defaults to 50-period simple moving average.
```

### Example 2: Close below 200 day moving average

User request:

```text
Find stocks where close is below 200 day moving average
```

Explorer output:

```text
Column A: C
Column B: Mov(C,200,S)
Filter: ColA < ColB
```

### Example 3: Fast moving average crosses above slow moving average

User request:

```text
Find stocks where fast moving average crosses above slow moving average
```

Explorer output:

```text
Column A: Mov(C,20,S)
Column B: Mov(C,50,S)
Filter: Cross(ColA, ColB)
```

Notes:

```text
Fast moving average is interpreted as a shorter-period moving average.
Slow moving average is interpreted as a longer-period moving average.
If periods are not specified, use 20 and 50 as defaults.
```

### Example 4: 20 day MA crosses above 50 day MA

User request:

```text
Find stocks where 20 day moving average crosses above 50 day moving average
```

Explorer output:

```text
Column A: Mov(C,20,S)
Column B: Mov(C,50,S)
Filter: Cross(ColA, ColB)
```

### Example 5: Volume above 20 day average volume

User request:

```text
Find stocks where volume is above 20 day average volume
```

Explorer output:

```text
Column A: V
Column B: Mov(V,20,S)
Filter: ColA > ColB
```

Notes:

```text
V means volume.
20 day average volume means Mov(V,20,S).
```

## Filter-only usage

Filter-only formulas are acceptable if the user does not need result table columns.

Example:

```metastock
C > Mov(C,50,S)
```

However, for this project, prefer Explorer columns when values are useful for inspection.

Preferred:

```text
Column A: C
Column B: Mov(C,50,S)
Filter: ColA > ColB
```

## Good outputs

Good:

```metastock
Mov(C,50,S)
```

Good:

```metastock
C > Mov(C,50,S)
```

Good:

```text
Column A: C
Column B: Mov(C,50,S)
Filter: ColA > ColB
```

Good:

```text
Column A: Mov(C,20,S)
Column B: Mov(C,50,S)
Filter: Cross(ColA, ColB)
```

Good:

```text
Column A: V
Column B: Mov(V,20,S)
Filter: ColA > ColB
```

## What not to do

Do not invent unsupported moving average function names.

Bad:

```metastock
MovingAverage(C,50)
```

Correct:

```metastock
Mov(C,50,S)
```

Do not write MA as if it were a MetaStock function unless a card explicitly supports it.

Bad:

```metastock
MA(C,50)
```

Correct:

```metastock
Mov(C,50,S)
```

Do not use natural language inside formulas.

Bad:

```metastock
close > 50 day moving average
```

Correct:

```metastock
C > Mov(C,50,S)
```

Do not omit the moving average method.

Bad:

```metastock
Mov(C,50)
```

Correct:

```metastock
Mov(C,50,S)
```

Do not use undefined Explorer columns.

Bad:

```text
Column A: Mov(C,50,S)
Filter: ColB > ColA
```

Correct:

```text
Column A: C
Column B: Mov(C,50,S)
Filter: ColA > ColB
```

Do not use `Ref(ColA,-1)` to get historical values of Explorer columns.

Bad:

```text
Column A: Mov(C,50,S)
Filter: Ref(ColA,-1) < ColA
```

Correct:

```text
Column A: Mov(C,50,S)
Column B: Ref(Mov(C,50,S),-1)
Filter: ColB < ColA
```

## Assumptions

- If the user says moving average without a method, use simple moving average `S`.
- If the user says EMA, use exponential moving average `E`.
- If the user says fast moving average without a period, use `Mov(C,20,S)`.
- If the user says slow moving average without a period, use `Mov(C,50,S)`.
- If the user gives exact periods, use the user-provided periods.
- If the moving average is applied to price and no price field is specified, use close `C`.
- If the moving average is applied to volume, use volume `V`.

## Related functions and concepts

Useful related cards:

- Cross: crossover detection
- C: close price
- V: volume
- Ref: previous value reference
- MACD: MACD indicator

## Retrieval keywords

Mov, moving average, MA, SMA, EMA, WMA, simple moving average, exponential moving average, close above moving average, close above 50 day moving average, price above moving average, volume above average volume, average volume, fast moving average, slow moving average, fast MA, slow MA, MA crossover, moving average crossover, bullish crossover, bearish crossover, MetaStock moving average, Explorer moving average.
