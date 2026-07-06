---
type: pattern
card_bucket: patterns
category: bollinger_band_breakout
source: MetaStock Formula Primer / internal project pattern
status: active
priority: 10
aliases:
  - Bollinger Band breakout
  - upper Bollinger Band breakout
  - close above upper Bollinger Band
  - price breaks above upper band
  - lower Bollinger Band breakdown
  - close below lower Bollinger Band
requires:
  - function.bbandtop
  - function.bbandbot
suggests:
  - function.cross
  - reference.price_fields
  - template.explorer_columns_filter
registry:
  enabled: true
  supports_explorer: true
  properties:
    formula_role: volatility_band_breakout
    default_period: 20
    default_method: S
    default_deviations: 2
    default_price_field: C
---

# Pattern: Bollinger Band Breakout

## Intent

Detect stocks where price breaks outside a Bollinger Band envelope.

This pattern is used when the user describes a close above the upper Bollinger Band, a price break above the top band, a close below the lower Bollinger Band, or a lower-band breakdown.

## Natural Language Triggers

- Bollinger Band breakout
- close above upper Bollinger Band
- price breaks above upper band
- upper band breakout
- price outside Bollinger Bands
- close below lower Bollinger Band
- lower band breakdown
- bearish Bollinger Band breakout

## Required Logical Components

1. Choose breakout direction:
   - bullish breakout above the upper band
   - bearish breakdown below the lower band
2. Choose the price field:
   - use close `C` by default for confirmed breakout
   - use high `H` or low `L` only if the user explicitly asks for intrabar breakout
3. Calculate the relevant Bollinger Band:
   - upper band with `BBandTop(C,N,METHOD,DEVIATIONS)`
   - lower band with `BBandBot(C,N,METHOD,DEVIATIONS)`
4. Compare current price against the relevant band.
5. Use `Cross` only when the user asks for the crossing event, not a continuing outside-band condition.

## Formula Building Blocks

Bullish close breakout above upper band:

```metastock
C > BBandTop(C,20,S,2)
```

Bullish crossing event above upper band:

```metastock
Cross(C, BBandTop(C,20,S,2))
```

Bearish close breakdown below lower band:

```metastock
C < BBandBot(C,20,S,2)
```

Bearish crossing event below lower band:

```metastock
Cross(BBandBot(C,20,S,2), C)
```

## Example Compositions

Close above upper Bollinger Band:

```metastock
C > BBandTop(C,20,S,2)
```

Close crosses above upper Bollinger Band:

```metastock
Cross(C, BBandTop(C,20,S,2))
```

Close below lower Bollinger Band:

```metastock
C < BBandBot(C,20,S,2)
```

Explorer columns for upper-band breakout:

```text
Column A: C
Column B: BBandTop(C,20,S,2)
Filter: ColA > ColB
```

## Default Assumptions

- Use close `C` for confirmed Bollinger Band breakouts.
- Use 20 periods if the user does not specify the Bollinger period.
- Use simple moving average method `S` if the user does not specify the method.
- Use 2 standard deviations if the user does not specify deviations.
- Use `Cross` only for event phrasing such as “crosses above” or “breaks through today.”

## Pitfalls

- Do not invent `Bollinger(C,20,2)` or `UpperBand(C,20)`.
- Do not omit the method argument; `BBandTop` and `BBandBot` require data array, periods, method, and deviations.
- Do not use the lower band for bullish upper-band breakout logic.
- Do not use `Cross` for a continuing condition such as “close is above the upper band.”
- Do not use a broad alias such as `breakout` alone; this card should not replace the general `pattern.breakout` card.

## Test Queries

- Find stocks where close is above the upper Bollinger Band
- Find stocks where price crosses above the top Bollinger Band
- Find stocks where close is below the lower Bollinger Band
