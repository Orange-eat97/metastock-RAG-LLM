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

## Source requirement

Convert only a stored Explorer whose deterministic validation has passed.

The System Test name is:

```text
AI - <Explorer name> - System Test
```

## Entry conversion

An Explorer Filter and a System Tester order formula are both logical conditions. Preserve the validated Explorer Filter as the long-entry strategy after expanding every `ColA`-style reference.

Example Explorer:

```text
Column A: RSI(14)
Column B: Mov(C,50,S)
Filter: ColA < 30 AND C > ColB
```

Expanded condition:

```metastock
RSI(14) < 30 AND C > Mov(C,50,S)
```

Buy Order formula:

```metastock
BuySignal := RSI(14) < 30 AND C > Mov(C,50,S);
BuySignal AND Simulation.LongPositionCount = 0
```

Paste the complete Buy formula into the Buy Order formula editor.

## Fixed exit conversion

The current project uses one deterministic Sell condition for every generated System Test:

```metastock
EntryPrice := C - Simulation.CurrentPositionPointDifference;
H >= EntryPrice * 1.20
```

Paste the complete formula into the Sell Order formula editor.

This is a 20 percent profit target. It does not add a stop-loss, short-side order, optimization, or alternative exit rule.

## General settings

- Order Bias: Long Orders
- Portfolio Bias: Single
- Position limit: enabled
- Maximum simultaneous positions: 1
- Buy: enabled
- Sell: enabled
- Sell Short: disabled
- Buy to Cover: disabled
- Stops: disabled
- Optimizations: disabled

## Forbidden output

- `ColA` through `ColL`
- `Filter:` labels
- `Column A:` labels
- positive or future `Ref()` offsets
- `OPT` variables
- short-side formulas
- invented stop-loss logic
