---
canonical_id: reference.logical_operators
title: Logical Operators
type: reference
card_bucket: references
category: logical_operators
source: MetaStock Formula Primer
status: active
priority: 10
supports_explorer: true
aliases:
- text: Logical Operators
  type: exact
  weight: 1.0
- text: comparison operators
  type: synonym
  weight: 0.85
- text: AND OR
  type: abbreviation
  weight: 1.0
- text: greater than less than
  type: synonym
  weight: 0.85
- text: greater than
  type: synonym
  weight: 0.85
- text: above
  type: weak_hint
  weight: 0.6
- text: over
  type: exact
  weight: 1.0
- text: less than
  type: synonym
  weight: 0.85
- text: below
  type: weak_hint
  weight: 0.6
- text: under
  type: exact
  weight: 1.0
- text: at least
  type: synonym
  weight: 0.85
- text: at most
  type: synonym
  weight: 0.85
- text: equal to
  type: synonym
  weight: 0.85
- text: not equal to
  type: synonym
  weight: 0.85
- text: and
  type: exact
  weight: 1.0
- text: or
  type: exact
  weight: 1.0
- text: either
  type: exact
  weight: 1.0
- text: both
  type: exact
  weight: 1.0
- text: all of these conditions
  type: synonym
  weight: 0.85
- text: any of these conditions
  type: synonym
  weight: 0.85
suggests:
- canonical_id: function.if
  rationale: function.if is often useful context for this card but is not always mandatory.
  priority: 40
  properties:
    source: registry_ready_transform
    formula_role: suggests
- canonical_id: template.explorer_columns_filter
  rationale: template.explorer_columns_filter is often useful context for this card but is not always mandatory.
  priority: 40
  properties:
    source: registry_ready_transform
    formula_role: suggests
semantic:
  concept_role: reference
  mechanism: logical_operators
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
  canonical_id: reference.logical_operators
  supports_explorer: true
  priority: 10
  properties:
    source_path: references/logical_operators.md
    generated_schema_version: registry_ready_v2
---

# Logical Operators

## Purpose

This card defines MetaStock comparison operators and logical connectors used in Explorer filters.

Use this card when the RAG system needs to combine multiple conditions, compare price fields, or avoid programming-language syntax.

## Comparison operators

| Meaning | MetaStock operator | Example |
|---|---|---|
| Greater than | `>` | `C > Mov(C,50,S)` |
| Greater than or equal to | `>=` | `RSI(14) >= 50` |
| Less than | `<` | `RSI(14) < 30` |
| Less than or equal to | `<=` | `C <= Mov(C,20,S)` |
| Not equal to | `<>` | `C <> Ref(C,-1)` |
| Equal to | `=` | `C = HHV(C,20)` |

## Logical connectors

Use `AND` when all conditions must be true.

```metastock
C > Mov(C,50,S) AND RSI(14) > 50
```

Use `OR` when any condition may be true.

```metastock
RSI(14) < 30 OR C < Ref(C,-1)
```

Use parentheses when combining `AND` and `OR`.

```metastock
(C > Mov(C,50,S) AND RSI(14) > 50) OR Cross(MACD(), Mov(MACD(),9,E))
```

## Natural language mappings

Use this card when the user says:

- greater than
- above
- over
- less than
- below
- under
- at least
- at most
- equal to
- not equal to
- and
- or
- either
- both
- all of these conditions
- any of these conditions

## Explorer examples

### Example 1: Both conditions required

User request:

```text
Find stocks where close is above the 50 day moving average and RSI is above 50
```

Explorer output:

```text
Column A: C
Column B: Mov(C,50,S)
Column C: RSI(14)
Filter: ColA > ColB AND ColC > 50
```

### Example 2: Either condition allowed

User request:

```text
Find stocks where RSI is below 30 or close is below yesterday's close
```

Explorer output:

```text
Column A: RSI(14)
Column B: C
Column C: Ref(C,-1)
Filter: ColA < 30 OR ColB < ColC
```

## What not to do

Do not use programming operators.

Bad:

```metastock
C > Mov(C,50,S) && RSI(14) > 50
```

Correct:

```metastock
C > Mov(C,50,S) AND RSI(14) > 50
```

Bad:

```metastock
C == HHV(C,20)
```

Correct:

```metastock
C = HHV(C,20)
```

Do not omit parentheses when mixing `AND` and `OR` in a way that may be ambiguous.

## Assumptions

- “Above”, “over”, and “greater than” map to `>`.
- “Below”, “under”, and “less than” map to `<`.
- “At least” maps to `>=`.
- “At most” maps to `<=`.
- Use `AND` for required combined conditions and `OR` for alternatives.

## Related functions and concepts

- If: explicit conditional output
- Explorer Columns and Filter Rules
- Price Fields

## Retrieval keywords

logical operators, comparison operators, AND, OR, greater than, less than, at least, at most, equal to, not equal to, MetaStock operators, no &&, no ==.

## Rules

- Use `AND` when all conditions must be true.
- Use `OR` when any condition may be true.
- Use MetaStock comparison operators: `>`, `>=`, `<`, `<=`, `<>`, and `=`.
- Use parentheses when combining `AND` and `OR` in one filter.
- Do not use programming operators such as `&&`, `||`, or `==`.


## Examples

```metastock
C > Mov(C,50,S) AND RSI(14) > 50
RSI(14) < 30 OR C < Ref(C,-1)
(C > Mov(C,50,S) AND RSI(14) > 50) OR Cross(MACD(), Mov(MACD(),9,E))
```


## What Not To Do

- Do not use `&&` for AND.
- Do not use `||` for OR.
- Do not use `==` for equality; MetaStock uses `=`.
- Do not leave mixed `AND`/`OR` logic ambiguous.

## Test Queries

- Explain Logical Operators for MetaStock Explorer generation
