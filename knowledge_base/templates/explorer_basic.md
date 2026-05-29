---
type: template
category: explorer
template: explorer_basic
source: MetaStock Formula Primer II / internal project rules
priority: high
status: draft
---

# Explorer Basic Output Template

## Purpose

This card defines the basic shape of the MetaStock Explorer output that the RAG system should generate.

Use this card when the user asks for a stock scan, screener, exploration, or filter condition.

The goal is to convert a natural-language request into:

```text
Column A: <formula>
Column B: <formula>
Column C: <formula>
Filter: <condition>
```

## Preferred output format

Use this structure:

```text
Column A: <formula>
Column B: <formula>
Column C: <formula>
Filter: <condition using ColA, ColB, ColC when helpful>
```

The exact number of columns depends on the user request.

If only one formula is needed, one column is enough:

```text
Column A: RSI(14)
Filter: ColA < 30
```

If the user wants multiple calculated values, define multiple columns:

```text
Column A: C
Column B: RSI(14)
Column C: Mov(C,50,S)
Filter: ColB < 30 AND ColA > ColC
```

## Basic examples

### RSI below 30

User request:

```text
Find stocks where RSI is below 30
```

Explorer output:

```text
Column A: RSI(14)
Filter: ColA < 30
```

### Close above 50-period moving average

User request:

```text
Find stocks where close is above the 50 day moving average
```

Explorer output:

```text
Column A: C
Column B: Mov(C,50,S)
Filter: ColA > ColB
```

### RSI below 30 and close above 50-period moving average

User request:

```text
Find stocks where RSI is below 30 and close is above 50 day moving average
```

Explorer output:

```text
Column A: C
Column B: RSI(14)
Column C: Mov(C,50,S)
Filter: ColB < 30 AND ColA > ColC
```

### Moving average crossover

User request:

```text
Find stocks where the 20 day moving average crosses above the 50 day moving average
```

Explorer output:

```text
Column A: Mov(C,20,S)
Column B: Mov(C,50,S)
Filter: Cross(ColA, ColB)
```

### Volume above average volume

User request:

```text
Find stocks where volume is above the 20 day average volume
```

Explorer output:

```text
Column A: V
Column B: Mov(V,20,S)
Filter: ColA > ColB
```

## Output rules

- Prefer simple formulas that are likely to run.
- Define columns that help the user inspect the result table.
- Define columns before referencing them in the filter.
- Use `AND` for multiple required conditions.
- Use `OR` for alternative conditions.
- Use parentheses when combining `AND` and `OR`.
- Do not use programming operators such as `&&`, `||`, or `==`.
- Do not use natural language inside formulas.
- Do not invent unsupported functions.
- If the user does not specify a common default, use the project default from the relevant function card.

## What not to do

Bad:

```text
Filter: close > moving average 50
```

Correct:

```text
Column A: C
Column B: Mov(C,50,S)
Filter: ColA > ColB
```

Bad:

```text
Column A: RSI
Filter: ColA < 30
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
Filter: ColA > moving average
```

Correct:

```text
Column A: C
Column B: Mov(C,50,S)
Filter: ColA > ColB
```

## Assumptions

- If the user says RSI without a period, use RSI(14).
- If the user says moving average without a method, use simple moving average `S`.
- If the user says close price, use `C`.
- If the user says volume, use `V`.
- If a calculated value is useful for the result table, define it as a column.

## Retrieval keywords

Explorer, exploration, stock scan, stock screener, filter, columns, result table, MetaStock Explorer, natural language to Explorer, generate Explorer formula.
