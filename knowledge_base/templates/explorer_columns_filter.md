---
type: template
category: explorer
template: explorer_columns_filter
source: MetaStock Formula Primer II / internal project rules
priority: high
status: draft
registry:
  enabled: false

---
# Explorer Columns and Filter Rules

## Purpose

This card defines how MetaStock Explorer columns and filters should interact.

The Explorer can place formulas in different columns. The filter can reference the last value of those columns using `ColA`, `ColB`, `ColC`, etc.

Use this card when the RAG system needs to decide whether to reference a formula directly or reference an Explorer column.

## Column reference syntax

Use:

```text
ColA
ColB
ColC
ColD
```

to reference Explorer columns.

Example:

```text
Column A: C
Column B: Mov(C,50,S)
Filter: ColA > ColB
```

This means:

```text
Filter close price greater than 50-period simple moving average.
```

## Rules for column references

- Define a column before referencing it.
- Do not reference `ColB` unless Column B is defined.
- Do not reference `ColC` unless Column C is defined.
- Prefer column references when the value is useful for the result table.
- The filter may reference `ColA`, `ColB`, `ColC`, etc.
- Keep column references simple and explicit.
- Do not use natural language inside formulas.

## Important Explorer limitation

Explorer column references such as `ColA` and `ColB` refer to the last value of the column.

They should not be treated like full historical data arrays.

Avoid formulas like:

```metastock
Ref(ColA,-1)
```

Instead, put the historical reference inside the column formula:

```text
Column A: C
Column B: Ref(C,-1)
Filter: ColA > ColB
```

## Correct column-reference examples

### One column

```text
Column A: RSI(14)
Filter: ColA < 30
```

### Two columns

```text
Column A: C
Column B: Mov(C,50,S)
Filter: ColA > ColB
```

### Three columns

```text
Column A: C
Column B: RSI(14)
Column C: Mov(C,50,S)
Filter: ColB < 30 AND ColA > ColC
```

### Crossover using columns

```text
Column A: Mov(C,20,S)
Column B: Mov(C,50,S)
Filter: Cross(ColA, ColB)
```

## Historical reference rule

If the user asks about a previous bar, previous close, yesterday, or one period ago, use `Ref()` inside the column formula.

Good:

```text
Column A: C
Column B: Ref(C,-1)
Filter: ColA > ColB
```

Bad:

```text
Column A: C
Filter: ColA > Ref(ColA,-1)
```

## What not to do

Bad:

```text
Column A: RSI(14)
Filter: ColB < 30
```

Correct:

```text
Column A: RSI(14)
Filter: ColA < 30
```

Bad:

```text
Column A: C
Column B: Mov(C,50,S)
Filter: Ref(ColA,-1) > ColB
```

Correct:

```text
Column A: Ref(C,-1)
Column B: Mov(C,50,S)
Filter: ColA > ColB
```

Bad:

```text
Column A: C
Column C: Mov(C,50,S)
Filter: ColA > ColC
```

Correct:

```text
Column A: C
Column B: Mov(C,50,S)
Filter: ColA > ColB
```

Bad:

```text
Column A: C
Column B: Mov(C,50,S)
Filter: close > ColB
```

Correct:

```text
Column A: C
Column B: Mov(C,50,S)
Filter: ColA > ColB
```

## Validation checklist

Before accepting generated Explorer output, check:

- Every `ColX` reference has a matching `Column X`.
- Columns are sequential where possible: A, B, C, not A, C, E.
- The filter does not call `Ref(ColA,-1)` or similar historical references on Explorer columns.
- The filter does not contain natural language.
- The filter uses `AND` and `OR`, not `&&` or `||`.
- The filter uses `=` for equality, not `==`.
- Function names are supported by the knowledge base.

## Retrieval keywords

Explorer columns, Explorer filter, ColA, ColB, ColC, column reference, filter reference, historical column limitation, MetaStock Explorer columns, result table.
