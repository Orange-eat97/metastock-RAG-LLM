---
type: function
function: If
category: logic
source: MetaStock Formula Primer
priority: 10
status: active
aliases:
- conditional
- then else
- binary wave
requires:
- reference.logical_operators
suggests:
- template.explorer_columns_filter
registry:
  supports_explorer: true
  priority: 20
  properties:
    source_notes:
    - Formula Primer: If condition returns THEN value if true, ELSE value otherwise;
        conditions alone imply true/false values.
  enabled: true
---

# If

## Purpose

`If` returns one value when a condition is true and another value when it is false.

In this project, `If` is mainly used for Explorer formulas such as:

- turning a condition into a numeric score
- grading multiple conditions
- preventing division by zero
- choosing one calculated value from two alternatives

For simple Explorer filters, the `If` function is usually unnecessary because a condition by itself already behaves like a true/false signal.

## Syntax

```metastock
If(CONDITION, THEN DATA ARRAY, ELSE DATA ARRAY)
```

## Parameters

| Parameter | Meaning | Example |
|---|---|---|
| CONDITION | Logical comparison | `C > Mov(C,40,S)` |
| THEN DATA ARRAY | Value returned when condition is true | `1` |
| ELSE DATA ARRAY | Value returned when condition is false | `0` |

## Common formulas

Close above 40-period moving average as a 1 or 0:

```metastock
If(C > Mov(C,40,S),1,0)
```

Avoid divide by zero:

```metastock
If(Mov(V,20,S) = 0, 0, V / Mov(V,20,S))
```

Simple grade for two conditions:

```metastock
If(C > Mov(C,50,S),1,0) + If(RSI(14) > 50,1,0)
```

## Natural language mappings

Use this function when the user says:

- if then else
- return 1 if true
- otherwise return 0
- binary signal
- score this condition
- grade the result
- assign one point if condition is true
- avoid divide by zero
- use fallback value

## Explorer column usage

For a grading column:

```text
Column A: If(C > Mov(C,50,S),1,0) + If(RSI(14) > 50,1,0)
Filter: ColA >= 2
```

For a simple filter, prefer the condition directly:

```text
Column A: C
Column B: Mov(C,50,S)
Filter: ColA > ColB
```

## Explorer examples

### Example 1: Score trend and momentum

User request:

```text
Find stocks that pass both trend and momentum, and show a score
```

Explorer output:

```text
Column A: If(C > Mov(C,50,S),1,0) + If(RSI(14) > 50,1,0)
Filter: ColA = 2
```

### Example 2: Volume ratio with zero guard

User request:

```text
Show volume ratio but avoid divide by zero
```

Explorer output:

```text
Column A: If(Mov(V,20,S) = 0, 0, V / Mov(V,20,S))
Filter: ColA > 1
```

## What not to do

Do not wrap every Explorer filter in `If` when the condition is already enough.

Unnecessary:

```metastock
If(C > Mov(C,50,S),1,0) = 1
```

Preferred:

```metastock
C > Mov(C,50,S)
```

Do not use programming syntax such as `if ... then ... else` inside the formula.

Correct:

```metastock
If(C > Mov(C,50,S),1,0)
```

## Assumptions

- A standalone condition can be used as a filter condition.
- `If` is useful when a numeric output is needed, not merely for true/false filtering.
- Use nested `If` sparingly because nested logic can become hard to validate.

## Related functions and concepts

- Logical Operators: `>`, `<`, `=`, `<>`, `AND`, `OR`
- Sum: count true/false conditions over periods
- Max: clamp minimum values
- Min: clamp maximum values

## Retrieval keywords

If, conditional, then else, binary wave, score condition, grade condition, return 1 if true, return 0 if false, avoid divide by zero, If(C > Mov(C,40,S),1,0).

## Valid Examples

```metastock
If(C > Mov(C,40,S), 1, 0)
If(RSI(14) < 30, RSI(14), 0)
```


## Common Mistakes

- Do not omit the false-result argument.
- Do not use programming syntax such as `if condition then`.
- In Explorer filters, a raw condition like `C > Mov(C,40,S)` is usually enough; use `If` when an explicit output value is needed.


## Related Patterns

- pattern.consecutive_condition
- pattern.rsi_recovery


## Test Queries

- Create a binary wave for close above moving average
- Use If to return 1 when RSI is below 30
