---
canonical_id: pattern.williams_r_recovery
title: 'Pattern: Williams %R Recovery'
type: pattern
card_bucket: patterns
category: momentum_recovery
source: MetaStock Formula Primer / Formula Primer II / internal project pattern
status: active
priority: 10
supports_explorer: true
functions:
- WillR
- Cross
aliases:
- text: 'Pattern: Williams %R Recovery'
  type: phrase
  weight: 0.9
- text: Williams %R Recovery
  type: exact
  weight: 1.0
- text: Williams R crosses above -80
  type: phrase
  weight: 0.9
- text: WillR oversold recovery
  type: phrase
  weight: 0.9
- text: Williams percent R buy signal
  type: synonym
  weight: 0.85
- text: Williams R turns up from oversold
  type: phrase
  weight: 0.9
requires:
- canonical_id: function.willr
  rationale: This card usually needs function.willr for correct formula generation.
  priority: 10
  properties:
    source: registry_ready_transform
    formula_role: requires
- canonical_id: function.cross
  rationale: This card usually needs function.cross for correct formula generation.
  priority: 10
  properties:
    source: registry_ready_transform
    formula_role: requires
suggests:
- canonical_id: function.mov
  rationale: function.mov is often useful context for this card but is not always mandatory.
  priority: 40
  properties:
    source: registry_ready_transform
    formula_role: suggests
semantic:
  concept_role: pattern
  mechanism: momentum_recovery
  market_object: price
  directions_supported:
  - bullish
  - bearish
  operations_supported:
  - momentum_recovery
  required_components:
  - willr
  - cross
  does_not_cover:
  - unrelated_pattern_substitution
  - guaranteed_trade_profitability
registry:
  enabled: true
  canonical_id: pattern.williams_r_recovery
  supports_explorer: true
  priority: 10
  properties:
    formula_role: momentum_recovery
    supports_explorer: true
    source_path: patterns/williams_r_recovery.md
    generated_schema_version: registry_ready_v2
---

# Pattern: Williams %R Recovery

## Intent

Detect securities where Williams %R recovers upward from an oversold region, normally by crossing above -80.

## Natural Language Triggers

- Williams %R recovery
- Williams R crosses above -80
- WillR oversold recovery
- Williams percent R buy signal
- Williams R turns up from oversold

## Required Logical Components

- Calculate Williams %R, usually `WillR(14)`.
- Use -80 as the oversold recovery threshold by default.
- Use `Cross(WillR(14),-80)` for bullish recovery.
- Use -20 for overbought/upper-zone logic.

## Formula Building Blocks

```metastock
WillR(14)
Cross(WillR(14),-80)
WillR(14) < -80
WillR(14) > -20
```

## Example Compositions

```metastock
Cross(WillR(14),-80)
Cross(WillR(14),-80) AND C > Mov(C,50,S)
```

## Default Assumptions

- Default period is 14.
- Oversold threshold is -80, not positive 80.
- Recovery means crossing above -80.

## Pitfalls

- Do not use positive thresholds such as 80/20 for Williams %R.
- Do not invent `WilliamsR()`.
- Do not reverse the Cross arguments for bullish recovery.

## Related functions and concepts

- function.willr
- function.cross
- function.mov

## Retrieval keywords

Williams %R recovery, Williams R crosses above -80, WillR oversold recovery, Williams percent R buy signal, Williams R turns up from oversold, WillR, Cross.

## Test Queries

- Find stocks where Williams R crosses above -80
- Find Williams %R oversold recovery stocks
