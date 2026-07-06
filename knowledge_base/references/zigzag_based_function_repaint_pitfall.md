---
canonical_id: reference.zigzag_based_function_repaint_pitfall
title: Zig Zag Based Function Repaint Pitfall
type: reference
card_bucket: references
category: zigzag_based_function_repaint_pitfall
source: MetaStock Formula Primer / Formula Primer II / internal project rule
status: active
priority: 10
supports_explorer: true
aliases:
- text: Zig Zag Based Function Repaint Pitfall
  type: exact
  weight: 1.0
- text: Zig Zag repaint
  type: synonym
  weight: 0.85
- text: Peak repaint warning
  type: synonym
  weight: 0.85
- text: Trough repaint warning
  type: synonym
  weight: 0.85
- text: Divergence repaint warning
  type: phrase
  weight: 0.9
- text: last Zig Zag value uncertain
  type: synonym
  weight: 0.85
requires:
- canonical_id: function.zig
  rationale: This card usually needs function.zig for correct formula generation.
  priority: 10
  properties:
    source: registry_ready_transform
    formula_role: requires
semantic:
  concept_role: reference
  mechanism: zigzag_based_function_repaint_pitfall
  market_object: formula_language
  operations_supported:
  - retrieval_context
  - formula_validation
  - generation_constraint
  required_components:
  - rule_application
  does_not_cover:
  - standalone_trading_signal
registry:
  enabled: true
  canonical_id: reference.zigzag_based_function_repaint_pitfall
  supports_explorer: true
  priority: 10
  properties:
    formula_role: zigzag_based_function_repaint_pitfall
    supports_explorer: true
    source_path: references/zigzag_based_function_repaint_pitfall.md
    generated_schema_version: registry_ready_v2
---

# Zig Zag Based Function Repaint Pitfall

## Purpose

Warn that Zig Zag based functions such as Zig, Peak, Trough, PeakBars, TroughBars, and Divergence can revise near the latest bars.

## Rules

- Zig Zag filters moves after the fact and its last segment can change.
- Peak, Trough, and Divergence are based on Zig Zag style movement.
- These functions are useful for historical swing context but risky as direct live buy/sell conditions.
- Prefer HHV/LLV/Ref alternatives for stable Explorer breakouts when possible.

## Examples

```metastock
Zig(C,5,%)
Peak(1,H,5)
Trough(1,L,5)
Divergence(RSI(14),C,5)
```

## What Not To Do

- Do not present Zig Zag based latest-bar signals as final.
- Do not use Peak/Trough without a repaint caveat.
- Do not use Divergence without specifying threshold and argument order.

## Natural Language Mappings

- Zig Zag repaint
- Peak repaint warning
- Trough repaint warning
- Divergence repaint warning
- last Zig Zag value uncertain

## Retrieval keywords

Zig Zag repaint, Peak repaint warning, Trough repaint warning, Divergence repaint warning, last Zig Zag value uncertain.

## Test Queries

- Zig Zag repaint
- Peak repaint warning
