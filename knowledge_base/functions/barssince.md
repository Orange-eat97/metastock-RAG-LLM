---
canonical_id: function.barssince
title: BarsSince
type: function
card_bucket: functions
category: time_reference
source: generated_curated_from_primer
status: active
priority: 10
supports_explorer: true
function: BarsSince
aliases:
- text: BarsSince
  type: exact
  weight: 1.0
- text: bars since
  type: phrase
  weight: 1.0
- text: days since signal
  type: phrase
  weight: 0.9
- text: within last N bars
  type: phrase
  weight: 0.9
- text: recent event
  type: phrase
  weight: 0.85
suggests:
- canonical_id: function.alert
  rationale: Alert can sometimes be simpler for recent-event scans.
  priority: 30
  properties:
    formula_role: recent_event_alternative
- canonical_id: function.valuewhen
  rationale: BarsSince is often paired with ValueWhen for event timing.
  priority: 30
  properties:
    formula_role: event_value_pair
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
  canonical_id: function.barssince
  supports_explorer: true
  priority: 10
  properties:
    formula_role: time_reference
    source_path: functions/barssince.md
    curation_level: upgraded_to_curated_quality
---

# BarsSince

## Purpose

`BarsSince` counts how many periods have passed since an expression was true. It returns 0 if the expression is true on the current bar. In Explorer generation it is used for recent-event windows, delayed confirmations, and formulas that must become valid only after enough data exists.

## Syntax

```metastock
BarsSince(EXPRESSION)
```

## Parameters

| Parameter | Meaning | Common values |
|---|---|---|
| EXPRESSION | Condition or event to count from. | `Cross(C,Mov(C,50,S))`, `RSI(14)<30` |

## Default interpretation

If the user says an event happened “within the last N bars”, use `BarsSince(event) <= N-1` if including today, or `< N` as a readable equivalent. If the event must be today, use the event itself or `BarsSince(event)=0`.

## Common formulas

```metastock
BarsSince(Cross(C,Mov(C,50,S)))
BarsSince(Cross(C,Mov(C,50,S))) < 5
BarsSince(RSI(14) < 30) <= 10
If(BarsSince(Cum(1) >= 50) >= 0, C, 0)
```

## Natural language mappings

Use this function when the user says:

- bars since
- days since
- within last 5 bars
- recent crossover
- recent signal
- event happened recently
- not long ago

## Explorer column usage

Use BarsSince as a column if the user wants to inspect recency. For simple recent-event filters, compare BarsSince to a threshold. Ensure Explorer loads enough records for the event history.

## Explorer examples

### Example 1: MA cross within last 5 bars

User request:

```text
Find stocks where close crossed above the 50 day moving average within the last 5 bars
```

Explorer output:

```text
Column A: BarsSince(Cross(C,Mov(C,50,S)))
Filter: ColA < 5
```
### Example 2: RSI oversold within last 10 bars

User request:

```text
Find stocks that were oversold within the last 10 days
```

Explorer output:

```text
Column A: BarsSince(RSI(14) < 30)
Filter: ColA < 10
```

## Filter-only usage

If the user only needs a pass/fail condition and does not need to inspect intermediate values, the function may be used directly in the Filter. For this project, prefer columns when the value helps the result table or when a pattern has multiple logical components.

## Valid Examples

```metastock
BarsSince(Cross(C,Mov(C,50,S))) < 5
BarsSince(RSI(14) < 30) = 0
```

## Common Mistakes

- Bad: assuming BarsSince is defined before the event has ever happened.
- Bad: using too few loaded records in Explorer for long lookback event scans.
- Bad: using `BarsSince(ColA)` as historical column logic. Use the underlying condition instead.

## Assumptions

- 0 means the event is true now.
- Recent within N bars includes the current bar unless the user says otherwise.
- Explorer needs sufficient loaded records.

## Related Patterns

- pattern.alert_recent_event
- function.valuewhen
- function.alert

## Related functions and concepts

- Explorer columns and filters
- Price fields such as `C`, `H`, `L`, `O`, and `V`
- `Cross` when the user asks for a crossing event
- `Ref` when the user asks for previous-bar or prior-event logic



## Retrieval keywords

BarsSince, bars ago, recent event, within last bars, days since signal.

## Test Queries

- Find stocks where MACD crossed above signal within the last 3 bars
