---
type: pattern
card_bucket: patterns
category: momentum_reversal
source: MetaStock Formula Primer / internal project pattern
priority: 10
status: active
functions:
- RSI
- Cross
- Ref
- Sum
aliases:
- RSI recovery
- RSI rebound
- oversold recovery
- RSI crosses above 30
requires:
- function.rsi
suggests:
- function.cross
- function.ref
- pattern.consecutive_condition
registry:
  supports_explorer: true
  priority: 10
  enabled: true
  properties: {}
---

# Pattern: RSI Recovery

## Intent

Detect stocks where RSI is recovering from an oversold condition or improving after weak momentum.

This pattern is used when the user describes RSI rebound, RSI recovery, oversold bounce, or RSI crossing back above a threshold.

## Natural Language Triggers

- RSI recovery
- RSI rebound
- oversold recovery
- RSI crosses above 30
- RSI turns up from oversold
- RSI rising from low levels
- RSI improving
- momentum recovery
- RSI was below 30 and is now above 30

## Keywords

- RSI recovery
- RSI rebound
- oversold bounce
- RSI crosses above 30
- Cross(RSI(14),30)
- RSI rising
- RSI improving
- momentum reversal

## Required Logical Components

1. Define RSI period, usually `RSI(14)`.
2. Define recovery threshold, usually `30` for oversold recovery.
3. Choose strict event or looser improvement:
   - strict event: `Cross(RSI(14),30)`
   - rising condition: `RSI(14) > Ref(RSI(14),-1)`
   - above threshold after oversold: `RSI(14) > 30 AND Ref(RSI(14),-1) <= 30`

## Formula Building Blocks

RSI crosses above 30:

```metastock
Cross(RSI(14),30)
```

RSI rising:

```metastock
RSI(14) > Ref(RSI(14),-1)
```

RSI above 30 and rising:

```metastock
RSI(14) > 30 AND RSI(14) > Ref(RSI(14),-1)
```

## Composition Guidance

- If the user says “crosses above 30”, use `Cross(RSI(14),30)`.
- If the user says “recovering” without specifying an exact cross, use RSI above 30 and rising.
- If the user asks for oversold only, use `RSI(14) < 30`, not recovery.
- Combine with trend or volume confirmation using `AND`.

## Example Compositions

RSI strict recovery:

```metastock
Cross(RSI(14),30)
```

RSI recovering with price above 50 MA:

```metastock
RSI(14) > 30 AND RSI(14) > Ref(RSI(14),-1) AND C > Mov(C,50,S)
```

## Observable Outputs

Useful Explorer columns:

- RSI value: `RSI(14)`
- Previous RSI value: `Ref(RSI(14),-1)`
- Close price, if trend confirmation is used: `C`
- Moving average, if used: `Mov(C,50,S)`

## Explorer examples

### Example 1: RSI crosses above 30

User request:

```text
Find stocks where RSI crosses above 30
```

Explorer output:

```text
Column A: RSI(14)
Filter: Cross(ColA, 30)
```

### Example 2: RSI recovery with trend confirmation

User request:

```text
Find stocks where RSI is recovering and close is above the 50 day moving average
```

Explorer output:

```text
Column A: RSI(14)
Column B: Ref(RSI(14),-1)
Column C: C
Column D: Mov(C,50,S)
Filter: ColA > 30 AND ColA > ColB AND ColC > ColD
```

## Pitfalls

- Do not interpret “oversold” as recovery. Oversold alone means `RSI(14) < 30`.
- Do not use `Cross` for a continuing condition such as “RSI is above 30”.
- Do not write `RSI > 30`; use `RSI(14) > 30`.

## Default Assumptions

- RSI period defaults to 14.
- Oversold recovery threshold defaults to 30.
- Recovery means above threshold and rising when the user does not specify a crossing event.

## Related functions and concepts

- RSI: momentum indicator
- Cross: threshold cross
- Ref: previous RSI comparison
- Mov: trend confirmation

## Retrieval keywords

RSI recovery, RSI rebound, oversold recovery, RSI crosses above 30, RSI rising, RSI improving, Cross(RSI(14),30), RSI(14) > Ref(RSI(14),-1).

## Test Queries

- Find stocks where RSI crosses back above 30
- Find stocks recovering from oversold RSI with price above the 50 day moving average
