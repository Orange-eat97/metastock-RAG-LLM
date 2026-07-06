---
canonical_id: pattern.relative_security_strength
title: 'Pattern: Relative Security Strength'
type: pattern
card_bucket: patterns
category: relative_strength
source: MetaStock Formula Primer / Formula Primer II / internal project pattern
status: active
priority: 10
supports_explorer: true
functions:
- Security
- Ref
- Mov
aliases:
- text: 'Pattern: Relative Security Strength'
  type: synonym
  weight: 0.85
- text: Relative Security Strength
  type: exact
  weight: 1.0
- text: relative strength versus SPY
  type: synonym
  weight: 0.85
- text: compare stock to index
  type: synonym
  weight: 0.85
- text: stock outperforming benchmark
  type: synonym
  weight: 0.85
- text: price divided by SPY is rising
  type: synonym
  weight: 0.85
- text: security relative strength line
  type: synonym
  weight: 0.85
requires:
- canonical_id: function.security
  rationale: This card usually needs function.security for correct formula generation.
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
- canonical_id: function.mov
  rationale: function.mov is often useful context for this card but is not always mandatory.
  priority: 40
  properties:
    source: registry_ready_transform
    formula_role: suggests
- canonical_id: reference.price_fields
  rationale: reference.price_fields is often useful context for this card but is not always mandatory.
  priority: 40
  properties:
    source: registry_ready_transform
    formula_role: suggests
semantic:
  concept_role: pattern
  mechanism: relative_strength
  market_object: security_series
  directions_supported:
  - bullish
  - bearish
  operations_supported:
  - relative_strength
  required_components:
  - security
  does_not_cover:
  - unrelated_pattern_substitution
  - guaranteed_trade_profitability
registry:
  enabled: true
  canonical_id: pattern.relative_security_strength
  supports_explorer: true
  priority: 10
  properties:
    formula_role: relative_strength
    supports_explorer: true
    source_path: patterns/relative_security_strength.md
    generated_schema_version: registry_ready_v2
---

# Pattern: Relative Security Strength

## Intent

Compare a security against another symbol or index using the `Security` function.

## Natural Language Triggers

- relative strength versus SPY
- compare stock to index
- stock outperforming benchmark
- price divided by SPY is rising
- security relative strength line

## Required Logical Components

- Retrieve benchmark close with `Security("SYMBOL",C)`.
- Calculate ratio of current close to benchmark close.
- Compare ratio against previous ratio or its moving average.
- Ensure target symbol/path exists.

## Formula Building Blocks

```metastock
C / Security("SPY",C)
C / Security("SPY",C) > Ref(C / Security("SPY",C),-1)
C / Security("SPY",C) > Mov(C / Security("SPY",C),20,S)
```

## Example Compositions

```metastock
C / Security("SPY",C) > Ref(C / Security("SPY",C),-1)
C / Security("SPY",C) > Mov(C / Security("SPY",C),20,S)
```

## Default Assumptions

- Default benchmark is not assumed; user should specify symbol.
- Use close `C` unless another field is specified.
- Security symbol must exist in MetaStock.

## Pitfalls

- Do not invent benchmark symbols.
- Do not omit quotes around symbol.
- Do not use online Security calls in automation without confirming data behavior.

## Related functions and concepts

- function.security
- function.ref
- function.mov
- reference.price_fields

## Retrieval keywords

relative strength versus SPY, compare stock to index, stock outperforming benchmark, price divided by SPY is rising, security relative strength line, Security, Ref, Mov.

## Test Queries

- Find stocks outperforming SPY by relative strength
- Find stocks where close divided by benchmark is rising
