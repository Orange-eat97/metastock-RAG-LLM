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
    rationale: Defines the System Tester order-condition slots and manual settings.
    priority: 10
  - canonical_id: reference.simulation_functions
    rationale: Defines the position guard and fixed profit-target calculation.
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

- Name: `AI - <Explorer name> - System Test`
- Order bias: long
- Portfolio bias: single
- Position limit enabled
- Maximum positions: one
- Buy enabled
- Sell enabled
- Sell Short disabled
- Buy to Cover disabled
- Stops disabled
- Optimizations disabled

## Buy condition

1. Load the validated stored Explorer.
2. Expand every Explorer column reference.
3. Preserve the expanded Filter as the entry strategy.
4. Assign the final entry condition to `BuySignal`.
5. Require `Simulation.LongPositionCount = 0`.

Template:

```metastock
<variable declarations, when required>
BuySignal := <expanded Explorer filter>;
BuySignal AND Simulation.LongPositionCount = 0
```

## Sell condition

Use the fixed 20 percent profit target:

```metastock
EntryPrice := C - Simulation.CurrentPositionPointDifference;
H >= EntryPrice * 1.20
```

Do not replace this with a reverse crossover, an LLM-generated exit, a stop-loss, or a short-side signal.

## User-facing instructions

Tell the user exactly where each block belongs:

- Buy formula → Buy Order formula editor
- Sell formula → Sell Order formula editor

Also state which General settings to select and which features to leave disabled.

## Safety rules

- Never fabricate extra exit logic.
- Never silently enable short orders, stops, or optimizations.
- Never leave Explorer column references in the Buy formula.
- Never persist a System Test generated from an invalid Explorer.
