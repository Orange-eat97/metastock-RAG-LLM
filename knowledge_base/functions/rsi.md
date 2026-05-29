---
type: function
function: RSI
category: momentum
source: MetaStock Formula Primer
priority: high
status: draft
---

# RSI

## Purpose

RSI means Relative Strength Index.

It is a momentum indicator commonly used to identify overbought and oversold conditions.

In this project, RSI is mainly used for Explorer filters such as:

- finding oversold stocks
- finding overbought stocks
- filtering stocks by momentum condition
- combining RSI with moving average or price conditions

## Syntax

```metastock
RSI(periods)
```

## Parameters

| Parameter | Meaning | Common value |
|---|---|---|
| periods | Number of periods used to calculate RSI | 14 |

## Default interpretation

If the user mentions RSI but does not specify a period, use:

```metastock
RSI(14)
```

If the user says “oversold”, interpret it as:

```metastock
RSI(14) < 30
```

If the user says “overbought”, interpret it as:

```metastock
RSI(14) > 70
```

## Common formulas

RSI value:

```metastock
RSI(14)
```

RSI below 30:

```metastock
RSI(14) < 30
```

RSI above 70:

```metastock
RSI(14) > 70
```

RSI below a user-defined threshold:

```metastock
RSI(14) < 40
```

RSI above a user-defined threshold:

```metastock
RSI(14) > 60
```

## Natural language mappings

Use this function when the user says:

- RSI
- relative strength index
- momentum indicator
- oversold
- overbought
- RSI below 30
- RSI less than 30
- RSI under 30
- RSI smaller than 30
- RSI above 70
- RSI greater than 70
- RSI higher than 70
- RSI crosses above 30
- RSI crosses below 70
- weak momentum
- strong momentum

## Explorer column usage

If the user wants to inspect the RSI value, define RSI as an Explorer column.

Example:

```metastock
Column A: RSI(14)
```

Then reference the column in the filter:

```metastock
Filter: ColA < 30
```

## Explorer examples

### Example 1: RSI below 30

User request:

```text
Find stocks where RSI is below 30
```

Explorer output:

```text
Column A: RSI(14)
Filter: ColA < 30
```

### Example 2: Oversold stocks

User request:

```text
Find oversold stocks
```

Explorer output:

```text
Column A: RSI(14)
Filter: ColA < 30
```

Assumption:

```text
Oversold means RSI(14) < 30.
```

### Example 3: RSI above 70

User request:

```text
Find stocks where RSI is above 70
```

Explorer output:

```text
Column A: RSI(14)
Filter: ColA > 70
```

### Example 4: Overbought stocks

User request:

```text
Find overbought stocks
```

Explorer output:

```text
Column A: RSI(14)
Filter: ColA > 70
```

Assumption:

```text
Overbought means RSI(14) > 70.
```

### Example 5: Custom RSI period

User request:

```text
Find stocks where 21-day RSI is below 35
```

Explorer output:

```text
Column A: RSI(21)
Filter: ColA < 35
```

### Example 6: RSI condition combined with price condition

User request:

```text
Find stocks where RSI is below 30 and close is above 50 day moving average
```

Explorer output:

```text
Column A: C
Column B: RSI(14)
Column C: Mov(C,50,S)
Filter: ColB < 30 AND ColA > ColC
```

Notes:

```text
RSI period defaults to 14.
50 day moving average defaults to simple moving average.
C means close price.
```

## Filter-only usage

If the user only needs a filter and does not care about displaying RSI as a column, this is acceptable:

```metastock
Filter: RSI(14) < 30
```

However, for this project, prefer column-based output when the user may want to inspect the result table.

Preferred:

```metastock
Column A: RSI(14)
Filter: ColA < 30
```

## Good outputs

Good:

```metastock
RSI(14) < 30
```

Good:

```metastock
RSI(21) > 60
```

Good:

```text
Column A: RSI(14)
Filter: ColA < 30
```

Good:

```text
Column A: C
Column B: RSI(14)
Column C: Mov(C,50,S)
Filter: ColB < 30 AND ColA > ColC
```

## What not to do

Do not write RSI without a period argument.

Bad:

```metastock
RSI < 30
```

Correct:

```metastock
RSI(14) < 30
```

Do not invent unsupported function names.

Bad:

```metastock
RelativeStrengthIndex(14) < 30
```

Correct:

```metastock
RSI(14) < 30
```

Do not use programming-style equality or logical operators unless confirmed by MetaStock syntax.

Bad:

```metastock
RSI(14) < 30 && C > Mov(C,50,S)
```

Correct:

```metastock
RSI(14) < 30 AND C > Mov(C,50,S)
```

Do not use natural language price names inside formulas.

Bad:

```metastock
RSI(14) < 30 AND close > moving_average(close, 50)
```

Correct:

```metastock
RSI(14) < 30 AND C > Mov(C,50,S)
```

Do not reference undefined Explorer columns.

Bad:

```text
Column A: RSI(14)
Filter: ColB < 30
```

Correct:

```text
Column A: RSI(14)
Filter: ColA < 30
```

Do not use a threshold without checking the user’s wording.

Bad:

```text
User says: RSI below 40
Output: RSI(14) < 30
```

Correct:

```text
User says: RSI below 40
Output: RSI(14) < 40
```

## Assumptions

- If the user says “RSI” without a period, use RSI(14).
- If the user says “oversold” without a threshold, use RSI(14) < 30.
- If the user says “overbought” without a threshold, use RSI(14) > 70.
- If the user gives a specific RSI period, use that period.
- If the user gives a specific RSI threshold, use that threshold.
- If the user asks for result columns, include RSI as a column.
- If the user combines RSI with price or moving average conditions, define separate columns and reference them in the filter.

## Related functions and concepts

Useful related cards:

- Mov: moving average
- Cross: crossover condition
- C: close price
- H: high price
- L: low price
- O: open price
- V: volume

## Retrieval keywords

RSI, Relative Strength Index, momentum, oversold, overbought, below 30, above 70, under 30, higher than 70, weak momentum, strong momentum, RSI filter, RSI Explorer, MetaStock RSI.