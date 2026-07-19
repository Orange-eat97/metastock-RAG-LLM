---
canonical_id: pattern.system_test_long_only
title: Long-only System Test
type: pattern
card_bucket: patterns
category: system_tester
source: MetaStock Formula Primer / Formula Primer II
status: active
priority: 10
supports_explorer: false
supports_system_tester: true
aliases:
  - text: long-only system test
    type: exact
    weight: 1.0
requires:
  - canonical_id: reference.system_tester_environment
    rationale: Defines the four System Tester order-condition slots.
    priority: 10
  - canonical_id: reference.simulation_functions
    rationale: Defines current-bar constraints and the long-position-count guard.
    priority: 10
registry:
  enabled: true
  canonical_id: pattern.system_test_long_only
  supports_explorer: false
  supports_system_tester: true
  priority: 10
  properties:
    source_path: patterns/system_test_long_only.md
---

# Long-only System Test

## Required structure

- Order bias: long
- Portfolio bias: single
- Position limit enabled with maximum one position
- Buy enabled
- Sell enabled
- Sell Short disabled
- Buy to Cover disabled
- Stops disabled
- Optimizations disabled

## Buy condition

Preserve the validated and expanded Explorer Filter as the entry logic. Add `Simulation.LongPositionCount = 0` as a current-bar guard.

## Sell condition

Use an explicit long exit. Reverse `Cross(A,B)` to `Cross(B,A)` only when the original entry is exactly that crossover event. For other entries, require a precise exit specification.

## Safety rules

- Never fabricate a sell rule merely to complete the object.
- Never silently enable short orders, stops, or optimizations.
- Never use Explorer column references in the output.
