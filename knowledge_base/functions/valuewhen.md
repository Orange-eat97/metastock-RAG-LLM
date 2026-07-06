---
type: function
function: ValueWhen
category: event_reference
source: MetaStock Formula Primer / Formula Primer II
priority: 10
status: active
aliases:
- value when
- event value
- value at signal
- last occurrence value
requires:
- reference.price_fields
- function.ref
suggests:
- function.barssince
registry:
  supports_explorer: true
  priority: 25
  properties:
    source_notes:
    - Formula Primer: ValueWhen(Nth, EXPRESSION, DATA ARRAY) returns the data array
        value at the Nth most recent true expression.
  enabled: true
---

# ValueWhen

## Purpose

`ValueWhen` returns the value of a data array when a specified expression was true.

In this project, `ValueWhen` is mainly used for advanced Explorer or indicator logic such as:

- value of close at the most recent signal
- price when a crossover happened
- last breakout level
- value at a date or event condition
- comparing current price against a prior event price

## Syntax

```metastock
ValueWhen(Nth, EXPRESSION, DATA ARRAY)
```

## Parameters

| Parameter | Meaning | Common values |
|---|---|---|
| Nth | Which occurrence to use, counting backward from the most recent | `1`, `2` |
| EXPRESSION | Event condition | `Cross(C,Mov(C,50,S))`, `C > Ref(HHV(C,20),-1)` |
| DATA ARRAY | Value to return at that event | `C`, `H`, `L`, `RSI(14)` |

## Common formulas

Close at the most recent 50 MA cross:

```metastock
ValueWhen(1, Cross(C, Mov(C,50,S)), C)
```

RSI value at the most recent 20-day close breakout:

```metastock
ValueWhen(1, C > Ref(HHV(C,20),-1), RSI(14))
```

Current close above the close at the most recent bullish cross:

```metastock
C > ValueWhen(1, Cross(C, Mov(C,50,S)), C)
```

## Natural language mappings

Use this function when the user says:

- value when
- close when signal happened
- price at last crossover
- value at breakout
- last signal price
- most recent occurrence
- previous occurrence of a signal
- price when RSI crossed above 30
- compare against signal bar

## Explorer column usage

Event value column:

```text
Column A: C
Column B: ValueWhen(1, Cross(C, Mov(C,50,S)), C)
Filter: ColA > ColB
```

## Explorer examples

### Example 1: Close above most recent MA cross price

User request:

```text
Find stocks where close is above the price when it most recently crossed the 50 day moving average
```

Explorer output:

```text
Column A: C
Column B: ValueWhen(1, Cross(C, Mov(C,50,S)), C)
Filter: ColA > ColB
```

## What not to do

Do not use `ValueWhen` for simple previous-bar logic. Use `Ref` instead.

Bad for yesterday close:

```metastock
ValueWhen(1, 1, C)
```

Correct:

```metastock
Ref(C,-1)
```

Do not use vague event expressions. The event must be a formula condition.

Bad:

```metastock
ValueWhen(1, breakout, C)
```

Correct:

```metastock
ValueWhen(1, C > Ref(HHV(C,20),-1), C)
```

## Assumptions

- `Nth = 1` means the most recent occurrence.
- `Nth = 2` means the occurrence before the most recent occurrence.
- Use this only when the user explicitly needs a value from an event bar.

## Related functions and concepts

- BarsSince: bars since an event
- Cross: event condition
- Ref: fixed offset reference
- HHV: breakout event construction
- LLV: breakdown event construction

## Retrieval keywords

ValueWhen, value when, event value, close at signal, price at crossover, last signal price, most recent occurrence, value at breakout, ValueWhen(1, Cross(C, Mov(C,50,S)), C).

## Valid Examples

```metastock
ValueWhen(1, Cross(C, Mov(C,50,S)), C)
ValueWhen(1, C = HHV(C,20), C)
```


## Common Mistakes

- Do not omit the occurrence number.
- Do not use `ValueWhen` if the triggering event may never exist in loaded data.
- Do not use it to look into the future; the expression should be based on available bars.


## Related Patterns

- pattern.ma_support_bounce
- pattern.consecutive_condition


## Test Queries

- Get the close value when price crossed above the 50 day moving average
- Find the value when a 20 day high occurred
