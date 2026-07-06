---
canonical_id: pattern.zigzag_swing_reversal
title: 'Pattern: Zig Zag Swing Reversal'
type: pattern
card_bucket: patterns
category: swing_reversal
source: MetaStock Formula Primer / Formula Primer II / internal project pattern
status: active
priority: 10
supports_explorer: true
functions:
- Zig
- Ref
aliases:
- text: 'Pattern: Zig Zag Swing Reversal'
  type: synonym
  weight: 0.85
- text: Zig Zag Swing Reversal
  type: exact
  weight: 1.0
- text: Zig Zag trend turn
  type: synonym
  weight: 0.85
- text: swing reversal using Zig
  type: synonym
  weight: 0.85
- text: Zig based reversal
  type: synonym
  weight: 0.85
- text: Zig Zag upturn
  type: synonym
  weight: 0.85
requires:
- canonical_id: function.zig
  rationale: This card usually needs function.zig for correct formula generation.
  priority: 10
  properties:
    source: registry_ready_transform
    formula_role: requires
suggests:
- canonical_id: function.ref
  rationale: function.ref is often useful context for this card but is not always mandatory.
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
  mechanism: swing_reversal
  market_object: price
  directions_supported:
  - bullish
  - bearish
  operations_supported:
  - swing_reversal
  required_components:
  - zig
  does_not_cover:
  - unrelated_pattern_substitution
  - guaranteed_trade_profitability
registry:
  enabled: true
  canonical_id: pattern.zigzag_swing_reversal
  supports_explorer: true
  priority: 10
  properties:
    formula_role: swing_reversal
    supports_explorer: true
    source_path: patterns/zigzag_swing_reversal.md
    generated_schema_version: registry_ready_v2
---

# Pattern: Zig Zag Swing Reversal

## Intent

Identify Zig Zag based swing turns or confirmed historical reversal context, with explicit warning that current Zig Zag legs can revise.

## Natural Language Triggers

- Zig Zag swing reversal
- Zig Zag trend turn
- swing reversal using Zig
- Zig based reversal
- Zig Zag upturn

## Required Logical Components

- Choose data array, usually close `C`.
- Choose minimum change threshold and diff method.
- Compare Zig value to previous Zig value for direction, or use Peak/Trough functions.
- Treat current-bar signal as provisional.

## Formula Building Blocks

```metastock
Zig(C,5,%)
Zig(C,5,%) > Ref(Zig(C,5,%),-1)
Zig(C,5,%) < Ref(Zig(C,5,%),-1)
```

## Example Compositions

```metastock
Zig(C,5,%) > Ref(Zig(C,5,%),-1)
Zig(C,5,%) < Ref(Zig(C,5,%),-1)
```

## Default Assumptions

- Default minimum change is 5 percent if unspecified.
- Use `%` for percent unless user specifies points.
- Current Zig Zag leg may revise.

## Pitfalls

- Do not use Zig Zag as a guaranteed real-time reversal signal.
- Do not omit diff method `%` or `$`.
- Do not ignore repaint caveat.

## Related functions and concepts

- function.zig
- function.ref
- reference.zigzag_based_function_repaint_pitfall

## Retrieval keywords

Zig Zag swing reversal, Zig Zag trend turn, swing reversal using Zig, Zig based reversal, Zig Zag upturn, Zig, Ref.

## Test Queries

- Find Zig Zag swing reversal stocks
- Find stocks where Zig Zag has turned up
