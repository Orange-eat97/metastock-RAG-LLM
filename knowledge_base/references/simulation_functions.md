---
canonical_id: reference.simulation_functions
title: Simulation Function Constraints
type: reference
card_bucket: references
category: simulation_functions
source: MetaStock Formula Primer II
status: active
priority: 10
supports_explorer: false
supports_system_tester: true
aliases:
  - text: Simulation.LongPositionCount
    type: exact
    weight: 1.0
  - text: Simulation.CurrentPositionPointDifference
    type: exact
    weight: 1.0
  - text: simulation functions
    type: phrase
    weight: 0.95
registry:
  enabled: true
  canonical_id: reference.simulation_functions
  supports_explorer: false
  supports_system_tester: true
  priority: 10
  properties:
    source_path: references/simulation_functions.md
---

# Simulation Function Constraints

`Simulation.*` values are available only in the Enhanced System Tester and describe the current simulated bar or position.

They must not be nested inside functions that require a historical series, including:

- `Ref()`
- `Mov()`
- `HHV()`
- `LLV()`
- `ValueWhen()`
- `BarsSince()`
- `Sum()`
- `Cum()`
- `ROC()`

## One-position entry guard

`Simulation.LongPositionCount` reports the number of open long positions.

For a one-position long-only Buy condition:

```metastock
BuySignal AND Simulation.LongPositionCount = 0
```

Keep this as a current-bar logical guard. Do not wrap it in a historical function.

## Reconstructing the current position entry price

`Simulation.CurrentPositionPointDifference` is the current point difference between the current price and the open position.

The project reconstructs the entry price as:

```metastock
EntryPrice := C - Simulation.CurrentPositionPointDifference;
```

A fixed 20 percent profit target can then be evaluated using the current bar high:

```metastock
EntryPrice := C - Simulation.CurrentPositionPointDifference;
H >= EntryPrice * 1.20
```

Paste this formula into the Sell Order formula editor. The condition becomes true when the current bar reaches a price at least 20 percent above the reconstructed entry price.

Do not place `Simulation.CurrentPositionPointDifference` inside `Ref()`, `Mov()`, or another historical-series function.
