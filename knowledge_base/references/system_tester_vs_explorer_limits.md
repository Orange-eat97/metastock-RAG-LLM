---
canonical_id: reference.system_tester_vs_explorer_limits
title: System Tester vs Explorer Limits
type: reference
card_bucket: references
category: environment_limits
source: generated_curated_from_primer
status: active
priority: 10
supports_explorer: true
aliases:
- text: System Tester vs Explorer
  type: exact
  weight: 1.0
- text: OPT variables in Explorer
  type: phrase
  weight: 0.95
- text: simulation functions in Explorer
  type: phrase
  weight: 0.95
- text: Explorer cannot use simulation functions
  type: phrase
  weight: 0.95
suggests:
- canonical_id: reference.explorer_environment_limitations
  rationale: Explorer environment rules are needed when rejecting System Tester-only constructs.
  priority: 30
  properties:
    formula_role: explorer_validation
semantic:
  concept_role: reference
  mechanism: environment_limits
  market_object: formula_environment
  outputs:
  - generation_rule
  - validation_rule
  supports_conditions:
  - environment_validation
  - syntax_validation
  does_not_cover:
  - specific_trading_signal_by_itself
registry:
  enabled: true
  canonical_id: reference.system_tester_vs_explorer_limits
  supports_explorer: true
  priority: 10
  properties:
    formula_role: environment_limits
    source_path: references/system_tester_vs_explorer_limits.md
    curation_level: upgraded_to_curated_quality
---

# System Tester vs Explorer Limits

## Purpose

This card separates what is valid in MetaStock Explorer from what belongs only in the System Tester or Expert Advisor. It prevents the generator from using optimisation variables, trade-state simulation functions, or commentary functions in Explorer formulas.

## Rules

- `OPT` variables are System Tester optimisation variables; do not use them in Explorer output.
- Simulation functions are System Tester-specific and should not be generated for Explorer scans.
- Simulation functions only have current-bar values and should not be nested inside historical functions such as `Ref()` or `ValueWhen()`.
- Expert Advisor commentary functions such as `WriteIf()` and `WriteVal()` are not Explorer filter functions.
- If a user asks for backtest exits, position count, equity, or trade entry price, route to System Tester/backtest planning rather than Explorer generation.
- For Explorer approximations, replace System Tester state with explicit price/indicator conditions and state assumptions.

## Examples

```metastock
{Explorer-safe MA condition}
C > Mov(C,50,S)
{System Tester style, not Explorer}
Mov(C,OPT1,E) > Mov(C,OPT2,E)
{Explorer-safe fixed replacement}
Mov(C,15,E) > Mov(C,40,E)
```

## What Not To Do

- Bad Explorer: `Mov(C,OPT1,E) > Mov(C,OPT2,E)`.
- Bad Explorer: `Simulation.LongPositionCount = 1`.
- Bad Explorer: `WriteIf(C>Mov(C,50,S),"Bullish","Bearish")`.
- Bad: promising a position-aware trailing stop inside Explorer without explicit state logic.

## Validation checklist

- Reject `OPT1`, `OPT2`, etc. in Explorer output.
- Reject `Simulation.` functions in Explorer output.
- Reject `WriteIf` and `WriteVal` in Explorer filters.
- Ask for backtest/system-test context if the user request requires trade state.

## Related functions and concepts

- function.input
- function.writeif
- function.writeval
- pattern.atr_trailing_stop



## Test Queries

- Can I use OPT1 in Explorer?
- Find stocks using a System Tester simulation function in Explorer
