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

`Simulation.*` functions are available only in the Enhanced System Tester.

They have values only for the current bar. Therefore they must not be nested inside functions that require historical or future series, including:

- `Ref()`
- `Mov()`
- `HHV()`
- `LLV()`
- `ValueWhen()`
- `BarsSince()`
- `Sum()`
- `Cum()`
- `ROC()`

## Position-count guard

`Simulation.LongPositionCount` reports the number of open long positions. For a one-position long-only entry condition, use it as a current-bar logical guard:

```metastock
BuySignal AND Simulation.LongPositionCount = 0
```

Do not wrap that simulation value in a historical function.
