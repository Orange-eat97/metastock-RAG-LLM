---
canonical_id: pattern.logical_switch_state_machine
title: 'Pattern: Logical Switch State Machine'
type: pattern
card_bucket: patterns
category: state_logic
source: MetaStock Formula Primer / Formula Primer II / internal project pattern
status: active
priority: 10
supports_explorer: true
functions:
- If
- PREV
- Cross
- Mov
aliases:
- text: 'Pattern: Logical Switch State Machine'
  type: synonym
  weight: 0.85
- text: Logical Switch State Machine
  type: exact
  weight: 1.0
- text: logical switch formula
  type: synonym
  weight: 0.85
- text: state machine formula
  type: synonym
  weight: 0.85
- text: two state switch
  type: synonym
  weight: 0.85
- text: persistent buy signal until exit
  type: synonym
  weight: 0.85
- text: PREV switch logic
  type: synonym
  weight: 0.85
- text: signal stays true until stop condition
  type: synonym
  weight: 0.85
requires:
- canonical_id: reference.prev_usage_and_circular_logic
  rationale: This card usually needs reference.prev_usage_and_circular_logic for correct formula generation.
  priority: 10
  properties:
    source: registry_ready_transform
    formula_role: requires
- canonical_id: function.if
  rationale: This card usually needs function.if for correct formula generation.
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
  mechanism: state_logic
  market_object: price
  directions_supported:
  - bullish
  - bearish
  operations_supported:
  - state_logic
  required_components:
  - reference.prev_usage_and_circular_logic
  - if
  does_not_cover:
  - unrelated_pattern_substitution
  - guaranteed_trade_profitability
registry:
  enabled: true
  canonical_id: pattern.logical_switch_state_machine
  supports_explorer: true
  priority: 10
  properties:
    formula_role: state_logic
    supports_explorer: true
    source_path: patterns/logical_switch_state_machine.md
    generated_schema_version: registry_ready_v2
---

# Pattern: Logical Switch State Machine

## Intent

Represent persistent state logic where a condition turns a signal on and another condition turns it off, usually using `PREV`.

## Natural Language Triggers

- logical switch formula
- state machine formula
- two state switch
- persistent buy signal until exit
- PREV switch logic
- signal stays true until stop condition

## Required Logical Components

- Define entry/on condition.
- Define exit/off condition.
- Use `If(entry,1,If(exit,0,PREV))` style logic.
- Check for circular/self-reference pitfalls.

## Formula Building Blocks

```metastock
If(entry_condition,1,If(exit_condition,0,PREV))
If(Cross(C,Mov(C,50,S)),1,If(Cross(Mov(C,50,S),C),0,PREV))
```

## Example Compositions

```metastock
If(Cross(C,Mov(C,50,S)),1,If(Cross(Mov(C,50,S),C),0,PREV))
```

## Default Assumptions

- Use only when persistent state is explicitly needed.
- PREV references the previous formula result.
- Complex state logic should be validated in MetaStock.

## Pitfalls

- Do not use PREV casually for simple current-bar filters.
- Do not create circular variables that cannot initialize.
- Do not ignore Explorer/runtime limitations.

## Related functions and concepts

- reference.prev_usage_and_circular_logic
- function.if
- function.cross
- function.mov
- reference.system_tester_vs_explorer_limits

## Retrieval keywords

logical switch formula, state machine formula, two state switch, persistent buy signal until exit, PREV switch logic, signal stays true until stop condition, If, PREV, Cross, Mov.

## Test Queries

- Create a two state switch formula with PREV
- Find stocks where a signal remains active until price crosses below moving average
