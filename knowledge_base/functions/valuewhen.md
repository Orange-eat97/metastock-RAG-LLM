---
canonical_id: function.valuewhen
title: ValueWhen
type: function
card_bucket: functions
category: time_reference
source: generated_curated_from_primer
status: active
priority: 10
supports_explorer: true
function: ValueWhen
aliases:
- text: ValueWhen
  type: exact
  weight: 1.0
- text: value when event happened
  type: phrase
  weight: 0.95
- text: most recent occurrence value
  type: phrase
  weight: 0.9
- text: value at last signal
  type: phrase
  weight: 0.9
suggests:
- canonical_id: function.cross
  rationale: ValueWhen commonly retrieves the value at a Cross event.
  priority: 30
  properties:
    formula_role: event_expression
- canonical_id: function.barssince
  rationale: BarsSince and ValueWhen are often paired for event timing.
  priority: 30
  properties:
    formula_role: event_timing
semantic:
  concept_role: function
  mechanism: time_reference
  market_object: price
  outputs:
  - indicator_series
  supports_conditions:
  - threshold_comparison
  - crossover
  - state_filter
  does_not_cover:
  - complete_trading_pattern_by_itself
registry:
  enabled: true
  canonical_id: function.valuewhen
  supports_explorer: true
  priority: 10
  properties:
    formula_role: time_reference
    source_path: functions/valuewhen.md
    curation_level: upgraded_to_curated_quality
---

# ValueWhen

## Purpose

`ValueWhen` returns the value of a data array at the Nth most recent time an expression was true. It is used to remember the close, high, low, indicator value, or bar number from a prior event.

## Syntax

```metastock
ValueWhen(Nth, EXPRESSION, DATA ARRAY)
```

## Parameters

| Parameter | Meaning | Common values |
|---|---|---|
| Nth | Which occurrence to retrieve, counting backward from most recent. | `1`, `2`, `3` |
| EXPRESSION | Event condition to search for. | `Cross(C,Mov(C,50,S))` |
| DATA ARRAY | Value to return when the expression was true. | `C`, `H`, `RSI(14)`, `Cum(1)` |

## Default interpretation

If the user asks for the value at the most recent signal, use `ValueWhen(1,event,value)`. Use `ValueWhen(2,event,value)` for the previous occurrence before the most recent.

## Common formulas

```metastock
ValueWhen(1, Cross(C,Mov(C,50,S)), C)
ValueWhen(1, RSI(14) < 30, C)
ValueWhen(2, Cross(MACD(),Mov(MACD(),9,E)), MACD())
C > ValueWhen(1, Cross(C,Mov(C,50,S)), C)
```

## Natural language mappings

Use this function when the user says:

- value when
- value at last signal
- price at last crossover
- close when RSI was oversold
- most recent event value
- previous occurrence value

## Explorer column usage

Use ValueWhen in a column when the user asks to compare current values to the value at a prior event. Ensure the event can occur within the loaded records.

## Explorer examples

### Example 1: Close above price at last MA cross

User request:

```text
Find stocks where close is above the close at the last 50 MA crossover
```

Explorer output:

```text
Column A: C
Column B: ValueWhen(1, Cross(C,Mov(C,50,S)), C)
Filter: ColA > ColB
```
### Example 2: RSI above its last oversold value

User request:

```text
Find stocks where RSI is above the RSI value from the last oversold day
```

Explorer output:

```text
Column A: RSI(14)
Column B: ValueWhen(1, RSI(14) < 30, RSI(14))
Filter: ColA > ColB
```

## Filter-only usage

If the user only needs a pass/fail condition and does not need to inspect intermediate values, the function may be used directly in the Filter. For this project, prefer columns when the value helps the result table or when a pattern has multiple logical components.

## Valid Examples

```metastock
ValueWhen(1, Cross(C,Mov(C,50,S)), C)
ValueWhen(2, RSI(14) < 30, C)
```

## Common Mistakes

- Bad: `ValueWhen(Cross(C,Mov(C,50,S)),C)`; the Nth argument is missing.
- Bad: assuming ValueWhen has a value before the event has ever occurred.
- Bad: using a future-looking expression inside ValueWhen for Explorer scans.

## Assumptions

- Nth=1 means most recent occurrence.
- The function may be undefined until the event has occurred in loaded data.
- Explorer accuracy depends on sufficient loaded records.

## Related Patterns

- pattern.rsi_divergence
- pattern.pivot_high_low
- function.barssince

## Related functions and concepts

- Explorer columns and filters
- Price fields such as `C`, `H`, `L`, `O`, and `V`
- `Cross` when the user asks for a crossing event
- `Ref` when the user asks for previous-bar or prior-event logic



## Retrieval keywords

ValueWhen, event value, last signal value, Nth occurrence, value at crossover.

## Test Queries

- Find stocks above the close at the last moving average crossover
