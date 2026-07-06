---
canonical_id: function.writeif
title: WriteIf
type: function
card_bucket: functions
category: expert_commentary
source: MetaStock Formula Primer
status: active
priority: 10
supports_explorer: false
function: WriteIf
aliases:
- text: WriteIf
  type: exact
  weight: 1.0
- text: WriteIf commentary
  type: synonym
  weight: 0.85
- text: Expert Advisor conditional text
  type: synonym
  weight: 0.85
- text: commentary true false text
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
  - boolean_or_conditional_value
  supports_conditions:
  - threshold_comparison
  - crossover
  - state_filter
  does_not_cover:
  - complete_trading_pattern_by_itself
registry:
  enabled: true
  canonical_id: function.writeif
  supports_explorer: false
  priority: 10
  properties:
    formula_role: expert_commentary
    supports_explorer: false
    source_path: functions/writeif.md
    generated_schema_version: registry_ready_v2
---

# WriteIf

## Purpose

`WriteIf` displays conditional text in Expert Advisor commentary. It is not valid for this project’s Explorer formula output.

## Syntax

```metastock
WriteIf(EXPRESSION, "TRUE TEXT", "FALSE TEXT")
```

## Parameters

- `EXPRESSION`: Condition to evaluate
- `"TRUE TEXT"`: Text displayed when true
- `"FALSE TEXT"`: Text displayed when false

## Valid Examples

```metastock
WriteIf(RSI(14)>70,"RSI is overbought","RSI is not overbought")
```

## Common Mistakes

- Do not use `WriteIf` in Explorer filters.
- Do not expect it to return a numeric scan condition.
- Do not omit quotation marks around text arguments.

## Related Patterns

- None yet.

## Natural Language Mappings

Use this function when the user says:

- WriteIf commentary
- Expert Advisor conditional text
- commentary true false text

## Assumptions

- Use this function only when the user request explicitly maps to this concept.

## Retrieval keywords

WriteIf commentary, Expert Advisor conditional text, commentary true false text, WriteIf, WriteIf(EXPRESSION, "TRUE TEXT", "FALSE TEXT").

## Test Queries

- Find stocks using WriteIf
