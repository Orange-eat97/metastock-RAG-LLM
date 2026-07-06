---
canonical_id: pattern.peak_trough_breakout
title: 'Pattern: Peak Trough Breakout'
type: pattern
card_bucket: patterns
category: swing_breakout
source: MetaStock Formula Primer / Formula Primer II / internal project pattern
status: active
priority: 10
supports_explorer: true
functions:
- Peak
- Trough
- HHV
- LLV
aliases:
- text: 'Pattern: Peak Trough Breakout'
  type: phrase
  weight: 0.9
- text: Peak Trough Breakout
  type: exact
  weight: 1.0
- text: break above previous peak
  type: phrase
  weight: 0.9
- text: break below previous trough
  type: phrase
  weight: 0.9
- text: price above last swing high
  type: phrase
  weight: 0.9
- text: price below last swing low
  type: phrase
  weight: 0.9
requires:
- canonical_id: function.peak
  rationale: This card usually needs function.peak for correct formula generation.
  priority: 10
  properties:
    source: registry_ready_transform
    formula_role: requires
- canonical_id: function.trough
  rationale: This card usually needs function.trough for correct formula generation.
  priority: 10
  properties:
    source: registry_ready_transform
    formula_role: requires
suggests:
- canonical_id: function.hhv
  rationale: function.hhv is often useful context for this card but is not always mandatory.
  priority: 40
  properties:
    source: registry_ready_transform
    formula_role: suggests
- canonical_id: function.llv
  rationale: function.llv is often useful context for this card but is not always mandatory.
  priority: 40
  properties:
    source: registry_ready_transform
    formula_role: suggests
- canonical_id: reference.zigzag_based_function_repaint_pitfall
  rationale: reference.zigzag_based_function_repaint_pitfall is often useful context for this card but is not always mandatory.
  priority: 40
  properties:
    source: registry_ready_transform
    formula_role: suggests
semantic:
  concept_role: pattern
  mechanism: swing_breakout
  market_object: price
  directions_supported:
  - bullish
  - bearish
  operations_supported:
  - breakout_detection
  - swing_breakout
  required_components:
  - peak
  - trough
  does_not_cover:
  - unrelated_pattern_substitution
  - guaranteed_trade_profitability
registry:
  enabled: true
  canonical_id: pattern.peak_trough_breakout
  supports_explorer: true
  priority: 10
  properties:
    formula_role: swing_breakout
    supports_explorer: true
    source_path: patterns/peak_trough_breakout.md
    generated_schema_version: registry_ready_v2
---

# Pattern: Peak Trough Breakout

## Intent

Detect price breaking above a previous Zig Zag peak or below a previous Zig Zag trough.

## Natural Language Triggers

- break above previous peak
- break below previous trough
- price above last swing high
- price below last swing low
- Peak Trough breakout

## Required Logical Components

- Use `Peak(1,H,threshold)` for prior swing high boundary.
- Use `Trough(1,L,threshold)` for prior swing low boundary.
- Compare current price to that boundary.
- Consider HHV/LLV alternative for non-repainting Explorer scans.

## Formula Building Blocks

```metastock
C > Peak(1,H,5)
C < Trough(1,L,5)
H > Peak(1,H,5)
L < Trough(1,L,5)
```

## Example Compositions

```metastock
C > Peak(1,H,5)
C < Trough(1,L,5)
```

## Default Assumptions

- Default threshold is 5 percent.
- Use close for confirmed breakout unless user specifies high/low.
- Peak/Trough are Zig Zag based and may revise.

## Pitfalls

- Do not use Peak/Trough without repaint warning.
- Do not confuse previous peak with current HHV.
- Do not omit threshold.

## Related functions and concepts

- function.peak
- function.trough
- function.hhv
- function.llv
- reference.zigzag_based_function_repaint_pitfall

## Retrieval keywords

break above previous peak, break below previous trough, price above last swing high, price below last swing low, Peak Trough breakout, Peak, Trough, HHV, LLV.

## Test Queries

- Find stocks breaking above previous peak
- Find stocks breaking below previous trough
