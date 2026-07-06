---
type: function
function: MACD
category: momentum
source: MetaStock Formula Primer
priority: 10
status: active
aliases:
- MACD
- moving average convergence divergence
- MACD line
requires:
- function.mov
suggests:
- function.cross
- pattern.macd_crossover
registry:
  supports_explorer: true
  priority: 20
  properties:
    source_notes:
    - Formula Primer introduces MACD() as a predefined indicator function with empty
      parentheses.
  enabled: true
---

# MACD

## Purpose

`MACD` returns the predefined Moving Average Convergence/Divergence indicator value.

In this project, `MACD` is mainly used for Explorer filters such as:

- MACD above zero
- MACD below zero
- MACD crosses above its signal line
- MACD momentum confirmation

## Syntax

```metastock
MACD()
```

## Common formulas

MACD value:

```metastock
MACD()
```

MACD above zero:

```metastock
MACD() > 0
```

MACD signal line using 9-period exponential moving average:

```metastock
Mov(MACD(),9,E)
```

MACD crosses above signal line:

```metastock
Cross(MACD(), Mov(MACD(),9,E))
```

MACD crosses below signal line:

```metastock
Cross(Mov(MACD(),9,E), MACD())
```

## Natural language mappings

Use this function when the user says:

- MACD
- MACD line
- MACD above zero
- MACD below zero
- MACD signal line
- MACD bullish crossover
- MACD bearish crossover
- MACD crosses above signal
- MACD crosses below signal
- moving average convergence divergence

## Explorer column usage

MACD crossover columns:

```text
Column A: MACD()
Column B: Mov(MACD(),9,E)
Filter: Cross(ColA, ColB)
```

MACD positive momentum:

```text
Column A: MACD()
Filter: ColA > 0
```

## Explorer examples

### Example 1: MACD crosses above signal line

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

### Example 2: MACD above zero

User request:

```text
Find stocks where MACD is above zero
```

Explorer output:

```text
Column A: MACD()
Filter: ColA > 0
```

## What not to do

Do not write MACD without parentheses.

Bad:

```metastock
MACD > 0
```

Correct:

```metastock
MACD() > 0
```

Do not invent a separate `Signal()` function unless a supported card defines it.

Bad:

```metastock
Cross(MACD(), Signal(MACD()))
```

Correct:

```metastock
Cross(MACD(), Mov(MACD(),9,E))
```

## Assumptions

- If the user says MACD signal line without specifying otherwise, use a 9-period exponential moving average of `MACD()`.
- Bullish MACD cross means `Cross(MACD(), Mov(MACD(),9,E))`.
- Bearish MACD cross means `Cross(Mov(MACD(),9,E), MACD())`.

## Related functions and concepts

- Mov: signal line smoothing
- Cross: crossover event
- MACD Crossover pattern
- ROC: momentum confirmation

## Retrieval keywords

MACD, MACD(), MACD signal line, MACD crossover, bullish MACD cross, bearish MACD cross, moving average convergence divergence, Cross(MACD(), Mov(MACD(),9,E)).

## Parameters

- `MACD()` takes no explicit parameters in MetaStock. The empty parentheses are required.


## Valid Examples

```metastock
MACD()
MACD() > 0
Cross(MACD(), Mov(MACD(),9,E))
```


## Common Mistakes

- Do not write `MACD` without parentheses.
- Do not invent `MACDSignal()`; use `Mov(MACD(),9,E)` for a common signal line.
- Do not reverse the `Cross` arguments for a bullish signal.


## Related Patterns

- pattern.macd_crossover


## Test Queries

- Find stocks where MACD crosses above its signal line
- Find stocks where MACD is above zero
