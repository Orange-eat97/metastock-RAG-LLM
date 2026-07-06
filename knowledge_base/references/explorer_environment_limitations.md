---
type: reference
card_bucket: references
category: explorer_environment_limitations
source: MetaStock Formula Primer II / internal project rules
priority: 10
status: active
aliases:
- Explorer limitations
- ColA historical limitation
- no OPT in Explorer
- no simulation functions in Explorer
forbids:
- function.input
suggests:
- template.explorer_columns_filter
registry:
  supports_explorer: true
  priority: 5
  enabled: true
  properties: {}
---

# Explorer Environment Limitations

## Purpose

This card defines constraints that matter when generating formulas for MetaStock Explorer rather than Indicator Builder or System Tester.

Use this card to prevent formulas that are valid in another MetaStock tool but invalid or misleading in Explorer.

## Important Explorer limitation

Explorer formulas are evaluated as of the exploration date. They should not reference values after that date.

Explorer columns can be referenced in the filter with `ColA`, `ColB`, etc., but those references are last-value references, not full historical data arrays.

Bad:

```metastock
Ref(ColA,-1)
```

Correct:

```text
Column A: C
Column B: Ref(C,-1)
Filter: ColA > ColB
```

## Tool-specific rules

### Indicator Builder

- `Input()` prompts are only for custom indicators.
- A custom indicator can have a limited number of input prompts.
- Other formulas can reference indicators with `Fml()` or `FmlVar()`.

### Explorer

- Use columns for inspectable output values.
- Use the filter to include or reject securities.
- Avoid historical references to `ColA`, `ColB`, etc.
- Prefer direct formulas or columns over interactive prompts.

### System Tester

- `OPT` variables are only defined in System Tester.
- Simulation functions are System Tester-specific.
- Simulation functions should not be used in Explorer generation.

## Natural language mappings

Use this card when the user says:

- Explorer limitation
- why ColA failed
- Ref ColA
- historical column reference
- OPT variable
- optimization variable
- simulation function
- system tester only
- input prompt
- formula works in indicator but not Explorer

## Validation checklist

Reject or repair generated Explorer output if:

- the filter contains `Ref(ColA,-1)` or similar historical `ColX` references
- the formula uses `OPT1`, `OPT2`, or other optimization variables
- the formula uses `Simulation.` functions
- the formula uses `Input()` in an Explorer formula
- the formula references a column that is not defined
- the formula uses future references such as `Ref(C,1)` for normal scans

## Explorer examples

### Correct previous-close comparison

```text
Column A: C
Column B: Ref(C,-1)
Filter: ColA > ColB
```

### Correct rising moving average comparison

```text
Column A: Mov(C,20,S)
Column B: Ref(Mov(C,20,S),-1)
Filter: ColA > ColB
```

## What not to do

Bad:

```text
Column A: C
Filter: ColA > Ref(ColA,-1)
```

Bad:

```metastock
OPT1 > 10
```

Bad:

```metastock
Simulation.LongPositionCount = 1
```

Bad:

```metastock
Input("periods",1,200,14)
```

## Assumptions

- The current project output target is Explorer unless the user explicitly asks for Indicator Builder, System Tester, or Expert Advisor.
- For Explorer scans, avoid future references and tool-specific functions from other MetaStock environments.

## Related functions and concepts

- Explorer Columns and Filter Rules
- Ref: historical data references
- Formula Variables
- Input Prompt Limitations

## Retrieval keywords

Explorer limitations, ColA historical limitation, Ref(ColA,-1), OPT only System Tester, Simulation functions, Input not Explorer, MetaStock environment, Explorer columns last value, no future data, validation checklist.

## Rules

- Explorer filters should evaluate conditions at the exploration date.
- Do not use positive `Ref()` offsets for normal historical scans because they imply future references.
- Do not use System Tester-only `Simulation.*` functions in Explorer formulas.
- Do not use `OPT` variables in Explorer formulas.
- Do not apply historical functions such as `Ref()` to `ColA` or `ColB`; put the historical reference inside the column formula instead.


## Examples

```text
Column A: C
Column B: Ref(C,-1)
Filter: ColA > ColB

Column A: BBandTop(C,20,S,2)
Column B: BBandBot(C,20,S,2)
Column C: BBandTop(C,20,S,2) - BBandBot(C,20,S,2)
```


## What Not To Do

- Do not write `Ref(ColA,-1)` in an Explorer filter.
- Do not use `Simulation.LongPositionCount` in Explorer.
- Do not use `OPT1` in Explorer.
- Do not reference values after the exploration date.
