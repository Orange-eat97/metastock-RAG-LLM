---
type: pattern
card_bucket: patterns
category: volume
source: MetaStock Formula Primer / internal project pattern
priority: high
status: active
functions:
  - Mov
fields:
  - V
keywords:
  - volume above average
  - average volume
  - high volume
  - unusual volume
  - volume spike
  - trading volume
  - active volume
  - V
  - Mov(V,20,S)
---

# Pattern: Volume Above Average

## Intent

Detect stocks where current trading volume is above its average volume.

This pattern is used when the user describes high volume, unusual volume, active volume, or a volume spike.

## Natural Language Triggers

- volume above average
- high volume
- unusual volume
- volume spike
- current volume greater than average volume
- current volume greater than 20 day average volume
- trading volume above average
- active stocks by volume
- volume at least 50 percent above average

## Keywords

- volume above average
- average volume
- high volume
- unusual volume
- volume spike
- active volume
- trading volume
- volume confirmation
- volume greater than average
- volume 50 percent above average
- V
- Mov(V,20,S)
- V > Mov(V,20,S)
- V >= Mov(V,20,S) * 1.5

## Required Logical Components

1. Use volume field `V` as the current volume.
2. Define average volume using `Mov(V,N,S)`.
3. Compare current volume against average volume.

## Optional Confirmation Components

- Percentage threshold above average volume:
  - for example, 50 percent above average means current volume is at least `1.5` times average volume.
- Price confirmation:
  - close above moving average
  - close breakout above prior high
- Trend confirmation:
  - price above moving average
  - short moving average above long moving average
- Breakout confirmation:
  - combine with breakout pattern using `AND`.

## Formula Building Blocks

Average volume:

```metastock
Mov(V,N,S)
```

Default 20-period average volume:

```metastock
Mov(V,20,S)
```

Volume above average:

```metastock
V > Mov(V,20,S)
```

Volume at least 50 percent above average:

```metastock
V >= Mov(V,20,S) * 1.5
```

Volume at least 100 percent above average:

```metastock
V >= Mov(V,20,S) * 2
```

## Composition Guidance

- If the user says average volume without a period, use 20 periods.
- If the user says high volume or unusual volume without a threshold, use `V > Mov(V,20,S)` as a conservative first version.
- If the user gives a percentage above average, convert it into a multiplier.
- If the user asks for price and volume confirmation, combine the price condition and volume condition with `AND`.
- If this pattern is retrieved together with a breakout pattern, use volume above average as a confirmation condition, not as the whole filter.

## Example Compositions

Volume above 20-period average:

```metastock
V > Mov(V,20,S)
```

Volume at least 50 percent above 20-period average:

```metastock
V >= Mov(V,20,S) * 1.5
```

Close above 50-period moving average with volume above average:

```metastock
C > Mov(C,50,S) AND V > Mov(V,20,S)
```

Breakout with volume confirmation:

```metastock
C > Ref(HHV(C,20),-1) AND V > Mov(V,20,S)
```

## Observable Outputs

Useful values to expose as Explorer columns:

- Current volume: `V`
- Average volume: `Mov(V,20,S)`
- Volume ratio: `V / Mov(V,20,S)`
- Close price: `C`
- Moving average of close, if used with a trend condition: `Mov(C,50,S)`

Column selection guidance:

- Include only columns relevant to the final filter.
- For pure volume scans, show current volume and average volume.
- For percentage-above-average scans, consider showing `V / Mov(V,20,S)`.
- For combined price-volume scans, show the major price condition and the volume condition.

## Pitfalls

- Do not use close `C` when the user asks for volume.
- Do not write `C > Mov(C,20,S)` as a substitute for volume above average.
- Do not invent unsupported volume functions such as `AverageVolume(20)`.
- Use `Mov(V,20,S)` for average volume unless the user specifies another period or method.
- Avoid making volume above average the only condition if the user asked for it as confirmation of another pattern.

## Default Assumptions

- If the user says average volume without a period, use 20 periods.
- If the user says volume spike without a threshold, use `V > Mov(V,20,S)`.
- If the user gives a percentage above average, convert it into a multiplier:
  - 50 percent above average means `1.5`
  - 100 percent above average means `2`
- Use simple moving average `S` unless the user specifies another average type.

## Source Notes

- `V` is the MetaStock volume field.
- `Mov(DATA ARRAY, PERIODS, METHOD)` can be applied to `V` to calculate average volume.
