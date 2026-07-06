---
canonical_id: function.input
title: Input
type: function
card_bucket: functions
category: indicator_builder_only
source: generated_curated_from_primer
status: active
priority: 10
supports_explorer: false
function: Input
aliases:
- text: Input
  type: exact
  weight: 1.0
- text: input prompt
  type: phrase
  weight: 0.95
- text: parameter prompt
  type: phrase
  weight: 0.9
- text: custom indicator input
  type: phrase
  weight: 0.9
suggests:
- canonical_id: reference.input_limitations
  rationale: Input is not directly supported in Explorer formulas and needs limitation context.
  priority: 30
  properties:
    formula_role: environment_limitation
semantic:
  concept_role: function
  mechanism: indicator_builder_only
  market_object: price
  outputs:
  - indicator_series
  supports_conditions:
  - threshold_comparison
  - crossover
  - state_filter
  does_not_cover:
  - complete_trading_pattern_by_itself
registry:
  enabled: true
  canonical_id: function.input
  supports_explorer: false
  priority: 10
  properties:
    formula_role: indicator_builder_only
    source_path: functions/input.md
    curation_level: upgraded_to_curated_quality
---

# Input

## Purpose

`Input` creates a prompt for a custom indicator. It is useful in Indicator Builder formulas but should not be generated directly in MetaStock Explorer filters. For Explorer generation, replace inputs with fixed constants or use a predefined referenced indicator with default inputs.

## Syntax

```metastock
Input("PROMPT TEXT", MINIMUM VALUE, MAXIMUM VALUE, DEFAULT VALUE)
```

## Parameters

| Parameter | Meaning | Common values |
|---|---|---|
| `"PROMPT TEXT"` | Text shown to the user. | `"periods"` |
| MINIMUM VALUE | Smallest accepted value. | `1` |
| MAXIMUM VALUE | Largest accepted value. | `200` |
| DEFAULT VALUE | Default prompt value. | `14` |

## Default interpretation

Do not use `Input()` in generated Explorer output. If a user asks for configurable periods in an Explorer, choose a fixed value and list it as an assumption, or ask for the value.

## Common formulas

```metastock
Input("time periods",2,200,14)
periods:=Input("time periods",2,200,14);
Mov(C,periods,S)
```

## Natural language mappings

Use this function when the user says:

- input prompt
- custom parameter
- ask me for periods
- configurable indicator
- user input value

## Explorer column usage

Explorer formulas should use fixed constants instead of `Input()`. This card exists mainly to prevent invalid Explorer generation.

## Explorer examples

### Example 1: Explorer-safe replacement

User request:

```text
Find stocks above a user-defined moving average period
```

Explorer output:

```text
Column A: C
Column B: Mov(C,50,S)
Filter: ColA > ColB
```
Notes:

```text
Assumption: user-defined period was not supplied, so use fixed default 50 or ask for clarification.
```

## Filter-only usage

If the user only needs a pass/fail condition and does not need to inspect intermediate values, the function may be used directly in the Filter. For this project, prefer columns when the value helps the result table or when a pattern has multiple logical components.

## Valid Examples

```metastock
Input("time periods",2,200,14)
periods:=Input("time periods",2,200,14);
```

## Common Mistakes

- Bad Explorer output: `Column A: Mov(C,Input("period",1,200,50),S)`. Correct: use a fixed period such as `Mov(C,50,S)` or ask the user for the period.
- Bad: using Input in System Tester or Explorer as if it were universally supported.
- Bad: omitting min, max, or default arguments.

## Assumptions

- Input is for Custom Indicator Builder.
- Explorer generation should use constants, not prompts.
- If an indicator with Input is referenced by Fml, default input values are used.

## Related Patterns

- reference.input_limitations
- function.fml

## Related functions and concepts

- Explorer columns and filters
- Price fields such as `C`, `H`, `L`, `O`, and `V`
- `Cross` when the user asks for a crossing event
- `Ref` when the user asks for previous-bar or prior-event logic



## Retrieval keywords

Input, input prompt, custom indicator input, configurable period.

## Test Queries

- Can I use Input in an Explorer formula?
