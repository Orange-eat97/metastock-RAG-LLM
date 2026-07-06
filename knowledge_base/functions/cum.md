---
canonical_id: function.cum
title: Cum
type: function
card_bucket: functions
category: aggregation
source: generated_curated_from_primer
status: active
priority: 10
supports_explorer: true
function: Cum
aliases:
- text: Cum
  type: exact
  weight: 1.0
- text: cumulate
  type: synonym
  weight: 0.9
- text: cumulative total
  type: phrase
  weight: 0.9
- text: bar count
  type: phrase
  weight: 0.85
- text: Cum(1)
  type: phrase
  weight: 0.9
suggests:
- canonical_id: function.valuewhen
  rationale: Cum(1) is often used with ValueWhen to store bar numbers at events.
  priority: 30
  properties:
    formula_role: bar_number_at_event
- canonical_id: function.barssince
  rationale: Cum can be paired with BarsSince in staged formulas.
  priority: 30
  properties:
    formula_role: event_timing
semantic:
  concept_role: function
  mechanism: aggregation
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
  canonical_id: function.cum
  supports_explorer: true
  priority: 10
  properties:
    formula_role: aggregation
    source_path: functions/cum.md
    curation_level: upgraded_to_curated_quality
---

# Cum

## Purpose

`Cum` keeps a running total of a data array. `Cum(1)` counts the number of loaded records and is often used as a bar counter in advanced formulas. In Explorer generation, it is useful for cumulative counts, indexing event bars, and reproducing Primer II style staged calculations.

## Syntax

```metastock
Cum(DATA ARRAY)
```

## Parameters

| Parameter | Meaning | Common values |
|---|---|---|
| DATA ARRAY | Series to accumulate. | `1`, `V`, `If(condition,1,0)` |

## Default interpretation

Use `Cum(1)` when a formula needs a running bar number. Use `Cum(If(condition,1,0))` when the user asks for cumulative event counts.

## Common formulas

```metastock
Cum(1)
Cum(V)
Cum(If(C > Mov(C,20,S),1,0))
ValueWhen(1, Cross(C,Mov(C,50,S)), Cum(1))
```

## Natural language mappings

Use this function when the user says:

- cumulative
- running total
- bar count
- number each bar
- count loaded records
- cumulative volume
- cumulative signals

## Explorer column usage

Use Cum carefully in Explorer because its value depends on how many records are loaded. Prefer simpler functions when a fixed lookback Sum is enough.

## Explorer examples

### Example 1: Bar number at last crossover

User request:

```text
Show the bar number when price last crossed above the 50 MA
```

Explorer output:

```text
Column A: Cum(1)
Column B: ValueWhen(1, Cross(C,Mov(C,50,S)), Cum(1))
Filter: ColA >= ColB
```
### Example 2: Cumulative volume

User request:

```text
Show cumulative volume
```

Explorer output:

```text
Column A: Cum(V)
Filter: ColA > 0
```

## Filter-only usage

If the user only needs a pass/fail condition and does not need to inspect intermediate values, the function may be used directly in the Filter. For this project, prefer columns when the value helps the result table or when a pattern has multiple logical components.

## Valid Examples

```metastock
Cum(1)
Cum(V)
Cum(If(RSI(14)<30,1,0))
```

## Common Mistakes

- Bad: using `Cum(1)` as a fixed calendar day count without considering loaded records.
- Bad: using Cum when `Sum(condition,N)` would better express a fixed recent window.
- Bad: assuming Cum resets by month or year unless you explicitly code that logic.

## Assumptions

- `Cum(1)` counts loaded bars.
- Cum includes the current bar.
- Explorer results depend on loaded records.

## Related Patterns

- function.sum
- function.valuewhen
- function.barssince

## Related functions and concepts

- Explorer columns and filters
- Price fields such as `C`, `H`, `L`, `O`, and `V`
- `Cross` when the user asks for a crossing event
- `Ref` when the user asks for previous-bar or prior-event logic



## Retrieval keywords

Cum, cumulative total, running total, bar count, Cum(1).

## Test Queries

- Show cumulative volume
- Find the bar number of the last moving average crossover
