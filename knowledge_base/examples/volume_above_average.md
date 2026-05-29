---
type: pattern
category: volume
source: MetaStock Formula Primer / internal project pattern
priority: high
status: draft
---

# Volume Above Average

## Purpose

This pattern finds stocks where current volume is above average volume.

It combines the volume field `V` with the moving average function `Mov`.

## Formula pattern

```metastock
V > Mov(V, PERIODS, S)
```

Common default:

```metastock
V > Mov(V,20,S)
```

## Natural language mappings

Use this pattern when the user says:

- volume above average
- high volume
- unusual volume
- volume spike
- current volume greater than 20 day average volume
- trading volume above average
- active stocks by volume

## Explorer examples

### Example 1: Volume above 20 day average

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

### Example 2: Volume 50 percent above average

User request:

```text
Find stocks where volume is at least 50 percent above 20 day average volume
```

Explorer output:

```text
Column A: V
Column B: Mov(V,20,S)
Filter: ColA >= ColB * 1.5
```

### Example 3: Price above MA and volume above average

User request:

```text
Find stocks where close is above the 50 day moving average and volume is above its 20 day average
```

Explorer output:

```text
Column A: C
Column B: Mov(C,50,S)
Column C: V
Column D: Mov(V,20,S)
Filter: ColA > ColB AND ColC > ColD
```

## What not to do

Do not use `C` when the user asks for volume.

Bad:

```metastock
C > Mov(C,20,S)
```

Correct:

```metastock
V > Mov(V,20,S)
```

Do not invent volume functions.

Bad:

```metastock
AverageVolume(20)
```

Correct:

```metastock
Mov(V,20,S)
```

## Assumptions

- If the user says average volume without a period, use 20 periods.
- If the user says volume spike without a threshold, use `V > Mov(V,20,S)` as a conservative first version.
- If the user gives a percentage above average, convert it into a multiplier.

## Retrieval keywords

volume above average, average volume, volume spike, high volume, unusual volume, active volume, V, Mov(V,20,S), trading volume.
