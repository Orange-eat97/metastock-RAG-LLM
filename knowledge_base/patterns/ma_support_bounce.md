---
canonical_id: pattern.ma_support_bounce
title: 'Pattern: Moving Average Support Bounce'
type: pattern
card_bucket: patterns
category: support_bounce
source: MetaStock Formula Primer II / internal project pattern
status: active
priority: 10
supports_explorer: true
functions:
- Mov
- Ref
- Sum
aliases:
- text: 'Pattern: Moving Average Support Bounce'
  type: phrase
  weight: 0.9
- text: Moving Average Support Bounce
  type: exact
  weight: 1.0
- text: MA bounce
  type: synonym
  weight: 0.85
- text: bounce from moving average
  type: synonym
  weight: 0.85
- text: pullback to MA
  type: synonym
  weight: 0.85
- text: MA support bounce
  type: phrase
  weight: 0.9
- text: moving average support
  type: phrase
  weight: 0.9
- text: pullback to 50 MA
  type: synonym
  weight: 0.85
- text: price touched the moving average and closed above it
  type: phrase
  weight: 0.9
- text: low touched MA and close recovered
  type: synonym
  weight: 0.85
- text: bounce off support
  type: phrase
  weight: 0.9
- text: close reclaims moving average
  type: synonym
  weight: 0.85
requires:
- canonical_id: function.mov
  rationale: This card usually needs function.mov for correct formula generation.
  priority: 10
  properties:
    source: registry_ready_transform
    formula_role: requires
suggests:
- canonical_id: function.ref
  rationale: function.ref is often useful context for this card but is not always mandatory.
  priority: 40
  properties:
    source: registry_ready_transform
    formula_role: suggests
- canonical_id: pattern.volume_above_average
  rationale: pattern.volume_above_average is often useful context for this card but is not always mandatory.
  priority: 40
  properties:
    source: registry_ready_transform
    formula_role: suggests
- canonical_id: pattern.rsi_recovery
  rationale: pattern.rsi_recovery is often useful context for this card but is not always mandatory.
  priority: 40
  properties:
    source: registry_ready_transform
    formula_role: suggests
semantic:
  concept_role: pattern
  mechanism: support_bounce
  market_object: price
  directions_supported:
  - bullish
  - bearish
  operations_supported:
  - support_bounce
  required_components:
  - mov
  does_not_cover:
  - unrelated_pattern_substitution
  - guaranteed_trade_profitability
registry:
  enabled: true
  canonical_id: pattern.ma_support_bounce
  supports_explorer: true
  priority: 10
  properties:
    source_path: patterns/ma_support_bounce.md
    generated_schema_version: registry_ready_v2
---

# Pattern: Moving Average Support Bounce

## Intent

Detect stocks where price pulls back to a moving average support area and closes back above it.

This pattern is used when the user describes a bounce from moving average support, pullback to MA, or close reclaiming an average after touching it.

## Natural Language Triggers

- bounce from moving average
- MA support bounce
- moving average support
- pullback to 50 MA
- price touched the moving average and closed above it
- low touched MA and close recovered
- bounce off support
- close reclaims moving average

## Keywords

- MA bounce
- moving average support
- support bounce
- pullback to MA
- touch moving average
- low below MA close above MA
- L <= Mov(C,N,S) AND C > Mov(C,N,S)

## Required Logical Components

1. Choose moving average period.
2. Define support average using `Mov(C,N,S)` by default.
3. Detect touch or pullback:
   - `L <= Mov(C,N,S)`
4. Detect recovery close:
   - `C > Mov(C,N,S)`
5. Optionally require trend confirmation:
   - price above longer MA
   - short MA above long MA

## Formula Building Blocks

50 MA bounce:

```metastock
L <= Mov(C,50,S) AND C > Mov(C,50,S)
```

100 MA bounce:

```metastock
L <= Mov(C,100,S) AND C > Mov(C,100,S)
```

50 MA bounce with volume confirmation:

```metastock
L <= Mov(C,50,S) AND C > Mov(C,50,S) AND V > Mov(V,20,S)
```

## Composition Guidance

- If the user says “bounce” from MA, use low touching or falling below the MA and close above the MA.
- If the user says “near MA” or “within X percent”, use an `Abs` distance condition instead.
- If the user gives no MA period, ask for a period in interactive mode; otherwise default to 50 for a first-pass scan.
- If the user asks for confirmation, combine with volume or RSI recovery using `AND`.

## Example Compositions

Close bounces off 50 MA:

```metastock
L <= Mov(C,50,S) AND C > Mov(C,50,S)
```

Close bounces off 50 MA with RSI recovery:

```metastock
L <= Mov(C,50,S) AND C > Mov(C,50,S) AND RSI(14) > Ref(RSI(14),-1)
```

## Observable Outputs

Useful Explorer columns:

- Close: `C`
- Low: `L`
- Support moving average: `Mov(C,50,S)`
- Volume confirmation if used: `V` and `Mov(V,20,S)`
- RSI confirmation if used: `RSI(14)` and `Ref(RSI(14),-1)`

## Explorer examples

### Example 1: 50 MA bounce

User request:

```text
Find stocks bouncing off the 50 day moving average
```

Explorer output:

```text
Column A: L
Column B: C
Column C: Mov(C,50,S)
Filter: ColA <= ColC AND ColB > ColC
```

### Example 2: 50 MA bounce with volume confirmation

User request:

```text
Find stocks bouncing off the 50 day moving average with volume above average
```

Explorer output:

```text
Column A: L
Column B: C
Column C: Mov(C,50,S)
Column D: V
Column E: Mov(V,20,S)
Filter: ColA <= ColC AND ColB > ColC AND ColD > ColE
```

## Pitfalls

- Do not treat every price above MA as a bounce. A bounce needs a touch or pullback condition.
- Do not use `Cross(C, Mov(C,N,S))` unless the user specifically asks for a cross back above the MA.
- Do not over-specify bounce conditions until they become impossible to satisfy.

## Default Assumptions

- Moving average method defaults to simple `S`.
- If the user says MA support but gives no period, use 50 as a first-pass default or ask for the period if clarification is allowed.
- Bounce means `L <= MA AND C > MA`.

## Related functions and concepts

- Mov: support moving average
- Ref: rising confirmation
- Volume Above Average pattern: volume confirmation
- RSI Recovery pattern: momentum confirmation
- Abs: near moving average distance

## Retrieval keywords

MA bounce, moving average support bounce, bounce from 50 MA, pullback to moving average, low touched MA, close above MA, L <= Mov(C,50,S) AND C > Mov(C,50,S).

## Test Queries

- Find stocks bouncing from the 50 day moving average
- Find stocks where price pulls back to MA support and closes above it
