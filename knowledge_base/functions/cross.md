---
type: function
function: Cross
category: crossover
source: MetaStock Formula Primer
priority: high
status: draft
---

# Cross

## Purpose

`Cross` detects when one data array crosses above another data array.

In this project, `Cross` is mainly used for Explorer filters such as:

- price crosses above moving average
- fast moving average crosses above slow moving average
- MACD crosses above signal line
- RSI crosses above a threshold
- bullish crossover signal

## Syntax

```metastock
Cross(DATA ARRAY 1, DATA ARRAY 2)
```

## Meaning

`Cross(A, B)` is true on the bar where `A` rises above `B`.

It should be used for a crossing event, not for a continuing above/below condition.

## Common formulas

Close crosses above 50-period moving average:

```metastock
Cross(C, Mov(C,50,S))
```

20-period MA crosses above 50-period MA:

```metastock
Cross(Mov(C,20,S), Mov(C,50,S))
```

MACD crosses above its 9-period EMA signal line:

```metastock
Cross(MACD(), Mov(MACD(),9,E))
```

RSI crosses above 30:

```metastock
Cross(RSI(14), 30)
```

## Natural language mappings

Use this function when the user says:

- crosses above
- crossover
- bullish crossover
- price crosses above moving average
- close crosses above MA
- fast MA crosses above slow MA
- MACD crosses above signal
- RSI crosses above 30
- breakout above average
- turns upward through

## Explorer column usage

Price crosses above moving average:

```text
Column A: C
Column B: Mov(C,50,S)
Filter: Cross(ColA, ColB)
```

Fast moving average crossover:

```text
Column A: Mov(C,20,S)
Column B: Mov(C,50,S)
Filter: Cross(ColA, ColB)
```

## Explorer examples

### Example 1: Price crosses above 50 MA

User request:

```text
Find stocks where close crosses above the 50 day moving average
```

Explorer output:

```text
Column A: C
Column B: Mov(C,50,S)
Filter: Cross(ColA, ColB)
```

### Example 2: Fast MA crosses above slow MA

User request:

```text
Find stocks where the 20 day moving average crosses above the 50 day moving average
```

Explorer output:

```text
Column A: Mov(C,20,S)
Column B: Mov(C,50,S)
Filter: Cross(ColA, ColB)
```

### Example 3: MACD bullish cross

User request:

```text
Find stocks where MACD crosses above its signal line
```

Explorer output:

```text
Column A: MACD()
Column B: Mov(MACD(),9,E)
Filter: Cross(ColA, ColB)
```

## Cross versus greater-than

Use `Cross(A,B)` when the user asks for the crossing event.

Use `A > B` when the user asks for a continuing condition.

Crossing event:

```metastock
Cross(C, Mov(C,50,S))
```

Continuing condition:

```metastock
C > Mov(C,50,S)
```

## Good outputs

Good:

```metastock
Cross(C, Mov(C,50,S))
```

Good:

```text
Column A: C
Column B: Mov(C,50,S)
Filter: Cross(ColA, ColB)
```

## What not to do

Do not use `Cross` for a continuing above condition.

Bad:

```text
User says: close is above the 50 day moving average
Output: Cross(C, Mov(C,50,S))
```

Correct:

```metastock
C > Mov(C,50,S)
```

Do not reverse the arguments for a bullish cross.

Bad:

```metastock
Cross(Mov(C,50,S), C)
```

Correct:

```metastock
Cross(C, Mov(C,50,S))
```

Do not invent unsupported names.

Bad:

```metastock
CrossOver(C, Mov(C,50,S))
```

Correct:

```metastock
Cross(C, Mov(C,50,S))
```

## Assumptions

- “Crosses above” means use `Cross(A,B)`.
- “Crosses below” can often be represented by reversing the arguments: `Cross(B,A)`.
- “Bullish crossover” usually means the faster or price series crosses above the slower/reference series.
- “Bearish crossover” usually means the slower/reference series crosses above the faster/price series, or the faster series crosses below the slower series.

## Related functions and concepts

- Mov: moving averages
- MACD: MACD line
- RSI: threshold cross
- Ref: previous-bar checks

## Retrieval keywords

Cross, crossover, crosses above, crosses below, bullish crossover, bearish crossover, price crosses moving average, MACD signal cross, fast MA slow MA cross.
