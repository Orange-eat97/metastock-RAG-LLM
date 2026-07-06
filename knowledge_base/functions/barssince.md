---
type: function
function: BarsSince
category: event_reference
source: MetaStock Formula Primer / Formula Primer II
priority: 10
status: active
aliases:
- bars since
- days since signal
- periods since event
- recently occurred
requires:
- reference.price_fields
suggests:
- function.valuewhen
- function.cross
registry:
  supports_explorer: true
  priority: 25
  properties:
    source_notes:
    - Formula Primer: BarsSince(DATA ARRAY) counts how many periods have passed since
        an event occurred.
  enabled: true
---

# BarsSince

## Purpose

`BarsSince` counts how many periods have passed since a condition was true.

In this project, `BarsSince` is mainly used for Explorer filters such as:

- signal occurred within the last N bars
- recently crossed above a moving average
- breakout happened recently
- number of days since RSI became oversold

## Syntax

```metastock
BarsSince(DATA ARRAY)
```

The data array is usually a logical expression.

## Common formulas

Bars since close was above 40:

```metastock
BarsSince(C > 40)
```

MA cross happened within the last 5 bars:

```metastock
BarsSince(Cross(C, Mov(C,50,S))) <= 5
```

Breakout happened within the last 3 bars:

```metastock
BarsSince(C > Ref(HHV(C,20),-1)) <= 3
```

## Natural language mappings

Use this function when the user says:

- bars since
- days since
- periods since
- recently happened
- happened within last N bars
- crossed within last N days
- breakout in the last N days
- signal age
- how many bars ago

## Explorer column usage

Signal age column:

```text
Column A: BarsSince(Cross(C, Mov(C,50,S)))
Filter: ColA <= 5
```

## Explorer examples

### Example 1: Recent 50 MA bullish cross

User request:

```text
Find stocks where price crossed above the 50 day moving average within the last 5 bars
```

Explorer output:

```text
Column A: BarsSince(Cross(C, Mov(C,50,S)))
Filter: ColA <= 5
```

### Example 2: Recent 20-day breakout

User request:

```text
Find stocks that broke above their previous 20 day high within the last 3 bars
```

Explorer output:

```text
Column A: BarsSince(C > Ref(HHV(C,20),-1))
Filter: ColA <= 3
```

## What not to do

Do not use `BarsSince` when the user asks for the event only on the current bar. Use the event condition directly.

Current-bar cross:

```metastock
Cross(C, Mov(C,50,S))
```

Recent cross within 5 bars:

```metastock
BarsSince(Cross(C, Mov(C,50,S))) <= 5
```

Be careful: formulas using `BarsSince` can be undefined until the event has occurred in the loaded data.

## Assumptions

- `BarsSince(condition)=0` means the condition is true on the current bar.
- Use `<= N` for “within the last N bars”.
- Ensure enough records are loaded when using this in an exploration.

## Related functions and concepts

- ValueWhen: value at event
- Cross: crossover event
- HHV: breakout event
- LLV: breakdown event
- Sum: repeated condition over a lookback

## Retrieval keywords

BarsSince, bars since, days since, periods since, recent signal, within last N bars, signal age, recent crossover, recent breakout, BarsSince(Cross(C, Mov(C,50,S))).

## Parameters

- `DATA ARRAY`: a true/false condition or binary series whose last true occurrence should be counted from.


## Valid Examples

```metastock
BarsSince(C > Mov(C,50,S))
BarsSince(Cross(RSI(14),30)) < 5
```


## Common Mistakes

- Do not use `BarsSince` before the event can ever become true; early values may be undefined.
- For Explorer scans, ensure enough records are loaded for the lookback condition.
- Do not write `BarsAgo(condition)`; use `BarsSince(condition)`.


## Related Patterns

- pattern.consecutive_condition
- pattern.rsi_recovery


## Test Queries

- Find stocks where RSI crossed above 30 within the last five bars
- Find stocks where the close moved above the 50 day average recently
