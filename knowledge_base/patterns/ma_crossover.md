---
canonical_id: pattern.ma_crossover
title: 'Pattern: Moving Average Crossover'
type: pattern
card_bucket: patterns
category: moving_average_crossover
source: MetaStock Formula Primer / internal project pattern
status: active
priority: 10
supports_explorer: true
functions:
- Mov
- Cross
aliases:
- text: 'Pattern: Moving Average Crossover'
  type: phrase
  weight: 0.9
- text: Moving Average Crossover
  type: exact
  weight: 1.0
- text: MA crossover
  type: phrase
  weight: 0.9
- text: golden cross
  type: phrase
  weight: 0.9
- text: death cross
  type: phrase
  weight: 0.9
- text: fast moving average crosses above slow moving average
  type: phrase
  weight: 0.9
- text: 20 day moving average crosses above 50 day moving average
  type: phrase
  weight: 0.9
- text: bullish moving average crossover
  type: phrase
  weight: 0.9
- text: bearish moving average crossover
  type: phrase
  weight: 0.9
requires:
- canonical_id: function.mov
  rationale: This card usually needs function.mov for correct formula generation.
  priority: 10
  properties:
    source: registry_ready_transform
    formula_role: requires
- canonical_id: function.cross
  rationale: This card usually needs function.cross for correct formula generation.
  priority: 10
  properties:
    source: registry_ready_transform
    formula_role: requires
suggests:
- canonical_id: template.explorer_columns_filter
  rationale: template.explorer_columns_filter is often useful context for this card but is not always mandatory.
  priority: 40
  properties:
    source: registry_ready_transform
    formula_role: suggests
semantic:
  concept_role: pattern
  mechanism: moving_average_crossover
  market_object: price
  directions_supported:
  - bullish
  - bearish
  operations_supported:
  - crossover_detection
  - moving_average_crossover
  required_components:
  - mov
  - cross
  does_not_cover:
  - unrelated_pattern_substitution
  - guaranteed_trade_profitability
registry:
  enabled: true
  canonical_id: pattern.ma_crossover
  supports_explorer: true
  priority: 10
  properties:
    source_path: patterns/ma_crossover.md
    generated_schema_version: registry_ready_v2
---

# Pattern: Moving Average Crossover

## Intent

Detect stocks where a faster moving average crosses above or below a slower moving average.

This pattern is used when the user describes MA crossover, fast MA crossing slow MA, golden cross, death cross, or trend crossover signals.

## Natural Language Triggers

- moving average crossover
- MA crossover
- fast moving average crosses above slow moving average
- 20 day moving average crosses above 50 day moving average
- bullish moving average crossover
- bearish moving average crossover
- golden cross
- death cross

## Keywords

- MA crossover
- moving average crossover
- fast MA
- slow MA
- Cross(Mov(C,20,S), Mov(C,50,S))
- golden cross
- death cross
- 20 day MA
- 50 day MA
- 200 day MA

## Required Logical Components

1. Identify the fast moving average period.
2. Identify the slow moving average period.
3. Choose moving average method:
   - simple `S` by default
   - exponential `E` if the user says EMA
4. Use `Cross(fast, slow)` for bullish crossover.
5. Use `Cross(slow, fast)` for bearish crossover.

## Formula Building Blocks

Bullish 20/50 SMA cross:

```metastock
Cross(Mov(C,20,S), Mov(C,50,S))
```

Bearish 20/50 SMA cross:

```metastock
Cross(Mov(C,50,S), Mov(C,20,S))
```

Golden cross default:

```metastock
Cross(Mov(C,50,S), Mov(C,200,S))
```

Death cross default:

```metastock
Cross(Mov(C,200,S), Mov(C,50,S))
```

## Composition Guidance

- If the user gives two periods, the smaller period is the fast MA.
- If the user says fast and slow but gives no periods, use 20 and 50.
- If the user says golden cross, use 50 SMA crossing above 200 SMA.
- If the user says death cross, use 200 SMA crossing above 50 SMA.
- If the user says MA is above another MA, use `>` rather than `Cross`.

## Example Compositions

20 SMA crosses above 50 SMA:

```metastock
Cross(Mov(C,20,S), Mov(C,50,S))
```

20 EMA crosses above 50 EMA:

```metastock
Cross(Mov(C,20,E), Mov(C,50,E))
```

## Observable Outputs

Useful Explorer columns:

- Fast moving average: `Mov(C,20,S)`
- Slow moving average: `Mov(C,50,S)`
- Close price: `C`

## Explorer examples

### Example 1: 20 MA crosses above 50 MA

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

### Example 2: Golden cross

User request:

```text
Find stocks with a golden cross
```

Explorer output:

```text
Column A: Mov(C,50,S)
Column B: Mov(C,200,S)
Filter: Cross(ColA, ColB)
```

## Pitfalls

- Do not use `Cross` when the user asks for an ongoing above/below condition.
- Do not reverse the arguments for bullish cross.
- Do not use unsupported names such as `SMA()` or `EMA()` unless a card explicitly supports them.

## Default Assumptions

- Moving average method defaults to simple `S`.
- Fast/slow defaults to 20/50 if periods are missing.
- Golden cross defaults to 50/200 simple moving averages.

## Related functions and concepts

- Mov: moving average calculation
- Cross: crossover event
- MA Trend Stack pattern
- Price Fields

## Retrieval keywords

moving average crossover, MA crossover, fast MA crosses above slow MA, golden cross, death cross, 20 day MA crosses above 50 day MA, Cross(Mov(C,20,S), Mov(C,50,S)).

## Test Queries

- Find stocks where the 20 day moving average crosses above the 50 day moving average
- Find stocks with a golden cross
