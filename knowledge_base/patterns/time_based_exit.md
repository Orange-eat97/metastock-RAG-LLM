---
canonical_id: pattern.time_based_exit
title: 'Pattern: Time Based Exit'
type: pattern
card_bucket: patterns
category: system_tester_stop
source: MetaStock Formula Primer / Formula Primer II / internal project pattern
status: active
priority: 10
supports_explorer: true
functions:
- BarsSince
- Cross
- Mov
aliases:
- text: 'Pattern: Time Based Exit'
  type: synonym
  weight: 0.85
- text: Time Based Exit
  type: exact
  weight: 1.0
- text: exit after 10 bars
  type: synonym
  weight: 0.85
- text: bars since entry condition
  type: synonym
  weight: 0.85
- text: hold for N bars then exit
  type: synonym
  weight: 0.85
- text: BarsSince exit rule
  type: synonym
  weight: 0.85
requires:
- canonical_id: function.barssince
  rationale: This card usually needs function.barssince for correct formula generation.
  priority: 10
  properties:
    source: registry_ready_transform
    formula_role: requires
suggests:
- canonical_id: function.cross
  rationale: function.cross is often useful context for this card but is not always mandatory.
  priority: 40
  properties:
    source: registry_ready_transform
    formula_role: suggests
- canonical_id: function.mov
  rationale: function.mov is often useful context for this card but is not always mandatory.
  priority: 40
  properties:
    source: registry_ready_transform
    formula_role: suggests
- canonical_id: reference.system_tester_vs_explorer_limits
  rationale: reference.system_tester_vs_explorer_limits is often useful context for this card but is not always mandatory.
  priority: 40
  properties:
    source: registry_ready_transform
    formula_role: suggests
semantic:
  concept_role: pattern
  mechanism: system_tester_stop
  market_object: price
  directions_supported:
  - bullish
  - bearish
  operations_supported:
  - system_tester_stop
  required_components:
  - barssince
  does_not_cover:
  - unrelated_pattern_substitution
  - guaranteed_trade_profitability
registry:
  enabled: true
  canonical_id: pattern.time_based_exit
  supports_explorer: true
  priority: 10
  properties:
    formula_role: system_tester_stop
    supports_explorer: true
    source_path: patterns/time_based_exit.md
    generated_schema_version: registry_ready_v2
---

# Pattern: Time Based Exit

## Intent

Represent exit logic after a fixed number of bars since an entry condition or event.

## Natural Language Triggers

- time based exit
- exit after 10 bars
- bars since entry condition
- hold for N bars then exit
- BarsSince exit rule

## Required Logical Components

- Define the entry condition or event.
- Calculate bars since that event.
- Compare bars-since value to the holding period.
- Use as System Tester exit logic or Explorer recent-event logic with caution.

## Formula Building Blocks

```metastock
BarsSince(entry_condition) >= 10
BarsSince(Cross(C,Mov(C,50,S))) >= 10
```

## Example Compositions

```metastock
BarsSince(Cross(C,Mov(C,50,S))) >= 10
```

## Default Assumptions

- Default holding period must be specified by the user; if absent, ask or choose a documented project default.
- This is more natural as System Tester exit logic.
- Explorer can scan for signals older/newer than N bars if the entry condition is defined.

## Pitfalls

- Do not invent an entry condition.
- Do not use this as a backtest without System Tester context.
- Do not confuse `BarsSince` with `Alert`.

## Related functions and concepts

- function.barssince
- function.cross
- function.mov
- reference.system_tester_vs_explorer_limits

## Retrieval keywords

time based exit, exit after 10 bars, bars since entry condition, hold for N bars then exit, BarsSince exit rule, BarsSince, Cross, Mov.

## Test Queries

- Find stocks where price crossed above MA 10 bars ago
- Create a time based exit after 10 bars
