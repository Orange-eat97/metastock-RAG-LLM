---
type: pattern
card_bucket: patterns
category: momentum_crossover
source: MetaStock Formula Primer / internal project pattern
priority: 10
status: active
functions:
- MACD
- Mov
- Cross
aliases:
- MACD crossover
- MACD bullish crossover
- MACD crosses above signal
- MACD signal cross
requires:
- function.macd
- function.mov
- function.cross
suggests:
- template.explorer_columns_filter
registry:
  supports_explorer: true
  priority: 10
  properties:
    default_signal_line: Mov(MACD(),9,E)
  enabled: true
---

# Pattern: MACD Crossover

## Intent

Detect stocks where the MACD line crosses above or below its signal line.

This pattern is used when the user describes a MACD bullish crossover, bearish crossover, or MACD signal-line cross.

## Natural Language Triggers

- MACD crossover
- MACD bullish crossover
- MACD bearish crossover
- MACD crosses above signal
- MACD crosses below signal
- MACD crosses above its signal line
- MACD signal line cross
- bullish MACD signal
- bearish MACD signal

## Keywords

- MACD
- MACD()
- signal line
- MACD signal
- MACD crossover
- bullish crossover
- bearish crossover
- Cross(MACD(), Mov(MACD(),9,E))
- Mov(MACD(),9,E)

## Required Logical Components

1. Define the MACD line:
   - `MACD()`
2. Define the default signal line:
   - `Mov(MACD(),9,E)`
3. Choose crossover direction:
   - bullish: MACD crosses above signal
   - bearish: signal crosses above MACD
4. Use `Cross` for the event.

## Formula Building Blocks

MACD line:

```metastock
MACD()
```

Signal line:

```metastock
Mov(MACD(),9,E)
```

Bullish MACD crossover:

```metastock
Cross(MACD(), Mov(MACD(),9,E))
```

Bearish MACD crossover:

```metastock
Cross(Mov(MACD(),9,E), MACD())
```

## Composition Guidance

- If the user says MACD crosses above signal line, use `Cross(MACD(), Mov(MACD(),9,E))`.
- If the user says MACD crosses below signal line, use `Cross(Mov(MACD(),9,E), MACD())`.
- If the user asks for MACD above signal but not a crossing event, use `MACD() > Mov(MACD(),9,E)`.
- If the user asks for signal columns, expose both MACD and signal line.
- If the user asks for trend confirmation, combine this pattern with price above moving average using `AND`.

## Example Compositions

Bullish MACD cross:

```metastock
Cross(MACD(), Mov(MACD(),9,E))
```

Bullish MACD cross with price above 50 MA:

```metastock
Cross(MACD(), Mov(MACD(),9,E)) AND C > Mov(C,50,S)
```

## Observable Outputs

Useful Explorer columns:

- MACD line: `MACD()`
- Signal line: `Mov(MACD(),9,E)`
- Close price: `C`
- Trend moving average, if used: `Mov(C,50,S)`

## Explorer examples

### Example 1: MACD crosses above signal

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

### Example 2: MACD bullish cross with trend confirmation

User request:

```text
Find stocks where MACD crosses above its signal line and close is above the 50 day moving average
```

Explorer output:

```text
Column A: MACD()
Column B: Mov(MACD(),9,E)
Column C: C
Column D: Mov(C,50,S)
Filter: Cross(ColA, ColB) AND ColC > ColD
```

## Pitfalls

- Do not write `MACD > signal` because `MACD` needs parentheses and signal must be defined.
- Do not invent `Signal()`.
- Do not use `Cross` if the user asks for a continuing above/below condition.
- Do not reverse the `Cross` arguments for a bullish crossover.

## Default Assumptions

- Default signal line is `Mov(MACD(),9,E)`.
- Bullish means MACD crosses above signal.
- Bearish means MACD crosses below signal.

## Related functions and concepts

- MACD: MACD line
- Mov: signal line smoothing
- Cross: crossover event
- Moving Average Crossover pattern

## Retrieval keywords

MACD crossover, MACD bullish crossover, MACD crosses above signal, MACD signal line, Cross(MACD(), Mov(MACD(),9,E)), bullish MACD, bearish MACD.

## Test Queries

- Find stocks where MACD crosses above its signal line
- Find stocks with a bearish MACD signal cross
