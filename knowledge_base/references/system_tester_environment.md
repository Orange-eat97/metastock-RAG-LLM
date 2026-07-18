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

## Primer-derived rules

A System Test may contain up to four condition formulas:

- Enter Long
- Exit Long
- Enter Short
- Exit Short

The formula field contains the logical condition. MetaStock treats zero as false and a non-zero result as true.

The System Tester has environment-specific facilities that are not valid in Explorer:

- `OPT1`, `OPT2`, and other OPT variables are System Tester optimization variables.
- `Simulation.*` values are System Tester-only current-bar values.

## Long-only project mapping

For the current long-only conversion:

- Buy maps to Enter Long.
- Sell maps to Exit Long.
- Sell Short is disabled.
- Buy to Cover is disabled.
- Stops and Optimizations remain disabled.

## Constraints

- Do not copy `ColA`, `ColB`, or other Explorer column references into a System Test.
- Expand each referenced Explorer column into its underlying formula first.
- Do not add short-side conditions to a long-only test.
- Do not add OPT variables when optimizations are disabled.
