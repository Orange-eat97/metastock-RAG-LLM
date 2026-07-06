---
canonical_id: function.writeval
title: WriteVal
type: function
card_bucket: functions
category: expert_commentary
source: MetaStock Formula Primer
status: active
priority: 10
supports_explorer: false
function: WriteVal
aliases:
- text: WriteVal
  type: exact
  weight: 1.0
- text: WriteVal commentary
  type: synonym
  weight: 0.85
- text: Expert Advisor value text
  type: synonym
  weight: 0.85
- text: commentary numeric value
  type: synonym
  weight: 0.85
suggests:
- canonical_id: reference.commentary_writeif_writeval
  rationale: reference.commentary_writeif_writeval is often useful context for this card but is not always mandatory.
  priority: 40
  properties:
    source: registry_ready_transform
    formula_role: suggests
semantic:
  concept_role: function
  mechanism: expert_commentary
  market_object: price
  outputs:
  - numeric_value
  supports_conditions:
  - threshold_comparison
  - crossover
  - state_filter
  does_not_cover:
  - complete_trading_pattern_by_itself
registry:
  enabled: true
  canonical_id: function.writeval
  supports_explorer: false
  priority: 10
  properties:
    formula_role: expert_commentary
    supports_explorer: false
    source_path: functions/writeval.md
    generated_schema_version: registry_ready_v2
---

# WriteVal

## Purpose

`WriteVal` displays a numeric value as text in Expert Advisor commentary. It is not valid for this project’s Explorer formula output.

## Syntax

```metastock
WriteVal(DATA ARRAY)
```

## Parameters

- `DATA ARRAY`: Numeric value or formula to display as text

## Valid Examples

```metastock
WriteVal(C)
WriteVal(Mov(C,40,S))
```

## Common Mistakes

- Do not use `WriteVal` in Explorer filters.
- Do not expect it to return a numeric scan condition.
- Do not pass natural language as a formula.

## Related Patterns

- None yet.

## Natural Language Mappings

Use this function when the user says:

- WriteVal commentary
- Expert Advisor value text
- commentary numeric value

## Assumptions

- Use this function only when the user request explicitly maps to this concept.

## Retrieval keywords

WriteVal commentary, Expert Advisor value text, commentary numeric value, WriteVal, WriteVal(DATA ARRAY).

## Test Queries

- Find stocks using WriteVal
