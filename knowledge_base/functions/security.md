---
canonical_id: function.security
title: Security
type: function
card_bucket: functions
category: cross_security_reference
source: generated_curated_from_primer
status: active
priority: 10
supports_explorer: true
function: Security
aliases:
- text: Security
  type: exact
  weight: 1.0
- text: Security function
  type: phrase
  weight: 0.95
- text: relative strength versus index
  type: phrase
  weight: 0.9
- text: compare with another symbol
  type: phrase
  weight: 0.9
- text: external security data
  type: phrase
  weight: 0.85
suggests:
- canonical_id: function.roc
  rationale: Relative security strength often compares rate of change between two securities.
  priority: 30
  properties:
    formula_role: relative_strength_metric
semantic:
  concept_role: function
  mechanism: cross_security_reference
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
  canonical_id: function.security
  supports_explorer: true
  priority: 10
  properties:
    formula_role: cross_security_reference
    source_path: functions/security.md
    curation_level: upgraded_to_curated_quality
---

# Security

## Purpose

`Security` returns a data array from another security. It can reference a symbol in the same folder, an online symbol with `ONLINE:`, or a full local path. In Explorer generation it is useful for relative-strength comparisons, index comparisons, or custom index formulas, but it depends on local data availability and exact symbol paths.

## Syntax

```metastock
Security("SYMBOL", DATA ARRAY)
```

## Parameters

| Parameter | Meaning | Common values |
|---|---|---|
| `"SYMBOL"` | Symbol, online symbol, or full data path. Must be quoted. | `"SPY"`, `"ONLINE:IBM"` |
| DATA ARRAY | Field or formula to retrieve from that security. | `C`, `V`, `ROC(C,20,%)` |

## Default interpretation

If the user compares a stock to an index but does not provide a symbol, ask for the benchmark symbol. If a symbol is provided, use `Security("SYMBOL",C)` for benchmark close by default.

## Common formulas

```metastock
Security("SPY",C)
Security("ONLINE:IBM",C)
C / Security("SPY",C)
ROC(C,20,%) > ROC(Security("SPY",C),20,%)
```

## Natural language mappings

Use this function when the user says:

- Security function
- benchmark symbol
- compare to SPY
- relative strength versus index
- external security
- another stock close
- market index close

## Explorer column usage

Use Security in columns only when the user provides a symbol or benchmark. Do not invent benchmark tickers. The formula can fail if the symbol path is unavailable.

## Explorer examples

### Example 1: Relative strength versus SPY

User request:

```text
Find stocks outperforming SPY over 20 days
```

Explorer output:

```text
Column A: ROC(C,20,%)
Column B: ROC(Security("SPY",C),20,%)
Filter: ColA > ColB
```
### Example 2: Close above benchmark close

User request:

```text
Find stocks where close is above IBM close from the same folder
```

Explorer output:

```text
Column A: C
Column B: Security("IBM",C)
Filter: ColA > ColB
```

## Filter-only usage

If the user only needs a pass/fail condition and does not need to inspect intermediate values, the function may be used directly in the Filter. For this project, prefer columns when the value helps the result table or when a pattern has multiple logical components.

## Valid Examples

```metastock
Security("IBM",C)
Security("ONLINE:IBM",C)
ROC(C,20,%) > ROC(Security("SPY",C),20,%)
```

## Common Mistakes

- Bad: `Security(SPY,C)` without quotes. Correct: `Security("SPY",C)`.
- Bad: inventing a benchmark symbol when the user did not provide one.
- Bad: using a local full path that may not exist on the user machine.
- Bad: assuming Security works if the required data is missing.

## Assumptions

- The symbol must be available in MetaStock data.
- Unqualified symbols are looked up relative to the base security data folder.
- Use close `C` for benchmark price unless another field is specified.

## Related Patterns

- pattern.relative_security_strength

## Related functions and concepts

- Explorer columns and filters
- Price fields such as `C`, `H`, `L`, `O`, and `V`
- `Cross` when the user asks for a crossing event
- `Ref` when the user asks for previous-bar or prior-event logic



## Retrieval keywords

Security, relative strength, benchmark, external symbol, ONLINE.

## Test Queries

- Find stocks outperforming SPY over 20 days
