---
canonical_id: reference.system_tester_environment
title: System Tester Environment
type: reference
card_bucket: references
category: system_tester_environment
source: MetaStock Formula Primer / Formula Primer II
status: active
priority: 10
supports_explorer: false
supports_system_tester: true
aliases:
  - text: system tester
    type: exact
    weight: 1.0
  - text: enter long exit long
    type: phrase
    weight: 0.95
registry:
  enabled: true
  canonical_id: reference.system_tester_environment
  supports_explorer: false
  supports_system_tester: true
  priority: 10
  properties:
    source_path: references/system_tester_environment.md
---

# System Tester Environment

## Order-condition slots

A System Test can define four independent order conditions:

- Enter Long
- Exit Long
- Enter Short
- Exit Short

Each formula is a logical condition. Zero is false and a non-zero result is true.

For the current project, the conversion is long-only:

- Buy maps to Enter Long.
- Sell maps to Exit Long.
- Sell Short remains disabled.
- Buy to Cover remains disabled.
- Stops remain disabled.
- Optimizations remain disabled.

## Manual-entry locations

When presenting a generated System Test to a user:

1. Put the generated entry formula in the Buy Order formula editor.
2. Put the generated exit formula in the Sell Order formula editor.
3. Enable Buy and Sell.
4. Leave Sell Short and Buy to Cover disabled.
5. Set Order Bias to Long Orders.
6. Set Portfolio Bias to Single.
7. Enable the position limit and set the maximum to one position.

## Explorer conversion constraints

Explorer columns are not available as `ColA`-style variables in a System Test. Expand every referenced Explorer column into its formula before producing the Buy condition.

Do not copy any of these into a System Test formula:

- `Column A:` labels
- `Filter:` labels
- `ColA` through `ColL`
- Explorer-only presentation text

## Environment-specific facilities

The System Tester supports facilities that are not valid in Explorer:

- `OPT1`, `OPT2`, and other `OPT` variables are optimization variables.
- `Simulation.*` values describe the current simulation state.

Do not introduce optimization variables while Optimizations are disabled.
