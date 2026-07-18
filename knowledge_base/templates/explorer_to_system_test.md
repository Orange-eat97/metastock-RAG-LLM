---
canonical_id: template.explorer_to_system_test
title: Explorer to System Test Conversion
type: template
card_bucket: templates
category: system_tester
template: explorer_to_system_test
source: MetaStock Formula Primer / Formula Primer II
status: active
priority: 10
supports_explorer: false
supports_system_tester: true
aliases:
  - text: explorer to system test
    type: exact
    weight: 1.0
registry:
  enabled: true
  canonical_id: template.explorer_to_system_test
  supports_explorer: false
  supports_system_tester: true
  priority: 10
  properties:
    source_path: templates/explorer_to_system_test.md
---

# Explorer to System Test Conversion

## Entry conversion

An Explorer Filter and a System Tester order formula are both logical conditions. Preserve the Explorer Filter as the long-entry strategy after expanding all Explorer column references.

Example:

```text
Column A: RSI(14)
Column B: Mov(C,50,S)
Filter: ColA < 30 AND C > ColB
```

Expanded entry condition:

```metastock
RSI(14) < 30 AND C > Mov(C,50,S)
```

One-position Buy condition:

```metastock
BuySignal := RSI(14) < 30 AND C > Mov(C,50,S);
BuySignal AND Simulation.LongPositionCount = 0
```

## Exit conversion

The exit condition is a separate strategy decision. A reverse crossover is unambiguous only when the entry event is a simple crossover:

```metastock
Enter Long: Cross(A,B)
Exit Long: Cross(B,A)
```

For compound filters or state conditions, do not invent an exit. Require an explicit sell formula or a precise conversion instruction.

## Forbidden output

- `ColA` through `ColL`
- `Filter:` labels
- `Column A:` labels
- positive/future `Ref()` offsets
- OPT variables when optimization is disabled
- short-side formulas in a long-only conversion
