---
type: function
function: Ref
category: time_reference
source: MetaStock Formula Primer
priority: high
status: draft
---

# Ref

## Purpose

`Ref` references a value from a different bar or period.

In this project, `Ref` is mainly used for Explorer filters such as:

- close higher than previous close
- volume increased from yesterday
- price above the high from 10 periods ago
- compare current value with previous value
- detect rising or falling values

## Syntax

```metastock
Ref(DATA ARRAY, PERIODS)
```

## Parameters

| Parameter | Meaning | Example |
|---|---|---|
| DATA ARRAY | Data series to reference | C, H, L, V, RSI(14), Mov(C,50,S) |
| PERIODS | Offset from current bar | -1 for previous bar, -5 for five bars ago |

## Direction rule

For most normal Explorer filters, use negative references to look backwards:

```metastock
Ref(C,-1)
```

This means the previous period’s close.

Avoid positive references in the Explorer because they refer to future data relative to the exploration date.

## Common formulas

Previous close:

```metastock
Ref(C,-1)
```

Close higher than previous close:

```metastock
C > Ref(C,-1)
```

Volume higher than previous volume:

```metastock
V > Ref(V,-1)
```

Moving average rising:

```metastock
Mov(C,20,S) > Ref(Mov(C,20,S),-1)
```

RSI rising:

```metastock
RSI(14) > Ref(RSI(14),-1)
```

## Natural language mappings

Use this function when the user says:

- previous close
- yesterday’s close
- last period
- one bar ago
- 5 bars ago
- compared with previous day
- higher than yesterday
- lower than yesterday
- rising
- falling
- increasing
- decreasing
- from previous bar

## Explorer column usage

Close higher than previous close:

```text
Column A: C
Column B: Ref(C,-1)
Filter: ColA > ColB
```

Moving average rising:

```text
Column A: Mov(C,20,S)
Column B: Ref(Mov(C,20,S),-1)
Filter: ColA > ColB
```

## Explorer examples

### Example 1: Close higher than yesterday

User request:

```text
Find stocks where close is higher than yesterday's close
```

Explorer output:

```text
Column A: C
Column B: Ref(C,-1)
Filter: ColA > ColB
```

### Example 2: Volume increased from previous bar

User request:

```text
Find stocks where volume increased from the previous day
```

Explorer output:

```text
Column A: V
Column B: Ref(V,-1)
Filter: ColA > ColB
```

### Example 3: Rising moving average

User request:

```text
Find stocks where the 20 day moving average is rising
```

Explorer output:

```text
Column A: Mov(C,20,S)
Column B: Ref(Mov(C,20,S),-1)
Filter: ColA > ColB
```

## Good outputs

Good:

```metastock
C > Ref(C,-1)
```

Good:

```metastock
Mov(C,20,S) > Ref(Mov(C,20,S),-1)
```

## What not to do

Do not use positive references for normal Explorer scans.

Bad:

```metastock
C > Ref(C,1)
```

Better for previous close comparison:

```metastock
C > Ref(C,-1)
```

Do not invent function names.

Bad:

```metastock
Previous(C)
```

Correct:

```metastock
Ref(C,-1)
```

Do not use natural language inside formulas.

Bad:

```metastock
C > yesterday close
```

Correct:

```metastock
C > Ref(C,-1)
```

## Assumptions

- “Previous”, “yesterday”, and “one bar ago” usually mean `Ref(DATA ARRAY,-1)`.
- For Explorer filters, avoid future references unless the user explicitly asks for a theoretical calculation and knows the limitation.
- Use `Ref` with indicators as well as price fields when checking if an indicator is rising or falling.

## Related functions and concepts

- Mov: rising/falling moving average
- ROC: rate of change
- HHV: highest high over lookback
- LLV: lowest low over lookback

## Retrieval keywords

Ref, reference, previous close, yesterday close, previous bar, one bar ago, bars ago, rising, falling, increasing, decreasing, historical value.
