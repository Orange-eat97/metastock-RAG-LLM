---
canonical_id: pattern.profit_target_stop
title: 'Pattern: Profit Target Stop'
type: pattern
card_bucket: patterns
category: system_tester_stop
source: MetaStock Formula Primer / Formula Primer II / internal project pattern
status: active
priority: 10
supports_explorer: false
functions:
- Ref
aliases:
- text: 'Pattern: Profit Target Stop'
  type: synonym
  weight: 0.85
- text: Profit Target Stop
  type: exact
  weight: 1.0
- text: exit at profit target
  type: synonym
  weight: 0.85
- text: system tester profit target
  type: synonym
  weight: 0.85
- text: close above entry price by percent
  type: phrase
  weight: 0.9
- text: optimized profit target
  type: synonym
  weight: 0.85
requires:
- canonical_id: reference.system_tester_vs_explorer_limits
  rationale: This card usually needs reference.system_tester_vs_explorer_limits for correct formula generation.
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
  - reference.system_tester_vs_explorer_limits
  does_not_cover:
  - unrelated_pattern_substitution
  - guaranteed_trade_profitability
registry:
  enabled: true
  canonical_id: pattern.profit_target_stop
  supports_explorer: false
  priority: 10
  properties:
    formula_role: system_tester_stop
    supports_explorer: false
    source_path: patterns/profit_target_stop.md
    generated_schema_version: registry_ready_v2
---

# Pattern: Profit Target Stop

## Intent

Represent profit-target exit logic, mainly for System Tester formulas rather than Explorer scans.

## Natural Language Triggers

- profit target stop
- exit at profit target
- system tester profit target
- close above entry price by percent
- optimized profit target

## Required Logical Components

- Define entry price or proxy for entry price.
- Define target percentage or point gain.
- Compare current high/close against target level.
- Use System Tester-specific context if actual trade entry price is needed.

## Formula Building Blocks

```metastock
H > entryprice * 1.1
H > entryprice * ((OPT1/100)+1)
```

## Example Compositions

```metastock
H > entryprice * 1.1
```

## Default Assumptions

- This is primarily a System Tester concept.
- Explorer cannot know actual trade entry price unless encoded externally.
- Use fixed constants instead of OPT outside System Tester.

## Pitfalls

- Do not use OPT variables in Explorer.
- Do not assume Explorer knows trade entry price.
- Do not confuse close condition with executable stop order.

## Related functions and concepts

- reference.system_tester_vs_explorer_limits
- function.ref

## Retrieval keywords

profit target stop, exit at profit target, system tester profit target, close above entry price by percent, optimized profit target, Ref.

## Test Queries

- Create a system tester profit target stop
- Explain why profit target stop is not a normal Explorer filter
