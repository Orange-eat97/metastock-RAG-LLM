---
canonical_id: reference.formula_variables
title: Formula Variables
type: reference
card_bucket: references
category: formula_variables
source: MetaStock Formula Primer / Formula Primer II
status: active
priority: 10
supports_explorer: true
aliases:
- text: Formula Variables
  type: exact
  weight: 1.0
- text: variable definitions
  type: synonym
  weight: 0.85
- text: temporary variable
  type: synonym
  weight: 0.85
- text: assignment operator
  type: synonym
  weight: 0.85
- text: variable
  type: exact
  weight: 1.0
- text: define MA first
  type: synonym
  weight: 0.85
- text: reusable calculation
  type: synonym
  weight: 0.85
- text: simplify formula
  type: synonym
  weight: 0.85
- text: repeated expression
  type: synonym
  weight: 0.85
- text: formula too long
  type: synonym
  weight: 0.85
- text: assign value
  type: synonym
  weight: 0.85
- text: use intermediate value
  type: synonym
  weight: 0.85
suggests:
- canonical_id: reference.explorer_environment_limitations
  rationale: reference.explorer_environment_limitations is often useful context for this card but is not always mandatory.
  priority: 40
  properties:
    source: registry_ready_transform
    formula_role: suggests
semantic:
  concept_role: reference
  mechanism: formula_variables
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
  canonical_id: reference.formula_variables
  supports_explorer: true
  priority: 10
  properties:
    source_path: references/formula_variables.md
    generated_schema_version: registry_ready_v2
---

# Formula Variables

## Purpose

This card explains MetaStock variable definitions, used to make long formulas easier to read and reuse.

In this project, variables are useful for complex formulas, but Explorer generation should still prefer simple column formulas unless variables materially reduce repeated calculations.

## Syntax

Variable assignment uses `:=` and a semicolon.

```metastock
VariableName:=Formula;
FinalExpression
```

Example:

```metastock
MA:=Mov(C,50,S);
C > MA
```

## Naming rules

- Variable names must start with a letter.
- Variable names may include numbers.
- Keep variable names short and meaningful.
- Avoid spaces in variable names.

## Common formulas

Moving average variable:

```metastock
MA50:=Mov(C,50,S);
C > MA50
```

Volume ratio variable:

```metastock
AvgVol:=Mov(V,20,S);
V / AvgVol
```

MACD signal variables:

```metastock
M:=MACD();
Sig:=Mov(M,9,E);
Cross(M,Sig)
```

## Natural language mappings

Use this card when the user says:

- variable
- temporary variable
- define MA first
- reusable calculation
- simplify formula
- repeated expression
- formula too long
- assign value
- use intermediate value

## Explorer usage guidance

For simple Explorer outputs, prefer columns over variables:

```text
Column A: C
Column B: Mov(C,50,S)
Filter: ColA > ColB
```

For complex single-column calculations, variables can be used inside a column formula:

```text
Column A: MA50:=Mov(C,50,S); C / MA50
Filter: ColA > 1
```

## What not to do

Do not use Python-style assignment.

Bad:

```metastock
MA50 = Mov(C,50,S)
C > MA50
```

Correct:

```metastock
MA50:=Mov(C,50,S);
C > MA50
```

Do not overuse variables in generated Explorer filters when columns are clearer for the result table.

## Assumptions

- Use variables only when they simplify repeated calculations.
- For result-table values, Explorer columns are usually more useful than hidden variables.
- Keep variable formulas within MetaStock environment limits.

## Related functions and concepts

- Explorer Columns and Filter Rules
- MACD: reusable signal-line construction
- ATR: custom true range construction
- If: complex conditional values

## Retrieval keywords

MetaStock variables, variable assignment, temporary variable, :=, semicolon, reusable formula, formula too long, define MA, MA50:=Mov(C,50,S), intermediate calculation.

## Rules

- Variable assignments use `:=`.
- End variable assignment lines with semicolons.
- The final plotted or filtered expression should not end with an unnecessary semicolon.
- Use variables to simplify complex repeated formulas.
- Keep Explorer formulas concise and avoid more variables than necessary.


## Examples

```metastock
MA:=Mov(C,50,S);
C > MA

Upper:=BBandTop(C,20,S,2);
Lower:=BBandBot(C,20,S,2);
Upper - Lower
```


## What Not To Do

- Do not use `=` for variable assignment.
- Do not forget semicolons after intermediate variable definitions.
- Do not end the final expression with a semicolon if MetaStock expects a final output expression.
- Do not create variable names that start with numbers.

## Test Queries

- Explain Formula Variables for MetaStock Explorer generation
