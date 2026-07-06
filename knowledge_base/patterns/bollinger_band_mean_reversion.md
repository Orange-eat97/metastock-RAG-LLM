---
type: pattern
card_bucket: patterns
category: bollinger_band_mean_reversion
source: MetaStock Formula Primer / internal project pattern
status: active
priority: 10
aliases:
  - Bollinger Band mean reversion
  - lower Bollinger Band rebound
  - bounce from lower Bollinger Band
  - close back above lower Bollinger Band
  - upper Bollinger Band reversal
  - close back below upper Bollinger Band
requires:
  - function.bbandtop
  - function.bbandbot
suggests:
  - function.cross
  - function.ref
  - function.rsi
  - reference.price_fields
registry:
  enabled: true
  supports_explorer: true
  properties:
    formula_role: volatility_band_reversion
    default_period: 20
    default_method: S
    default_deviations: 2
    default_price_field: C
---

# Pattern: Bollinger Band Mean Reversion

## Intent

Detect stocks that move outside or touch a Bollinger Band and then revert back toward the band envelope.

This pattern is used when the user describes a bounce from the lower Bollinger Band, a close back above the lower band, a reversal from the upper band, or a close back below the upper band.

## Natural Language Triggers

- Bollinger Band mean reversion
- lower Bollinger Band rebound
- bounce from lower Bollinger Band
- close back above lower Bollinger Band
- price re-enters Bollinger Bands
- upper Bollinger Band reversal
- close back below upper Bollinger Band
- overextended above upper band then reverses

## Required Logical Components

1. Choose reversion direction:
   - bullish reversion from the lower band
   - bearish reversion from the upper band
2. Calculate the relevant Bollinger Band with `BBandBot` or `BBandTop`.
3. Define the re-entry or bounce condition:
   - current close crosses above the lower band, or
   - low touches/falls below lower band and close finishes above it, or
   - current close crosses below the upper band, or
   - high touches/exceeds upper band and close finishes below it.
4. Optionally add confirmation such as RSI oversold recovery or volume confirmation.

## Formula Building Blocks

Bullish lower-band re-entry using `Cross`:

```metastock
Cross(C, BBandBot(C,20,S,2))
```

Bullish lower-band touch and close above:

```metastock
L <= BBandBot(C,20,S,2) AND C > BBandBot(C,20,S,2)
```

Bearish upper-band re-entry using `Cross` reversal:

```metastock
Cross(BBandTop(C,20,S,2), C)
```

Bearish upper-band touch and close below:

```metastock
H >= BBandTop(C,20,S,2) AND C < BBandTop(C,20,S,2)
```

## Example Compositions

Lower-band bounce:

```metastock
L <= BBandBot(C,20,S,2) AND C > BBandBot(C,20,S,2)
```

Lower-band recovery event:

```metastock
Cross(C, BBandBot(C,20,S,2))
```

Lower-band bounce with RSI recovery:

```metastock
L <= BBandBot(C,20,S,2) AND C > BBandBot(C,20,S,2) AND Cross(RSI(14),30)
```

Explorer columns for lower-band bounce:

```text
Column A: C
Column B: L
Column C: BBandBot(C,20,S,2)
Filter: ColB <= ColC AND ColA > ColC
```

## Default Assumptions

- Use close `C` as the Bollinger Band data array.
- Use 20-period simple Bollinger Bands with 2 standard deviations.
- If the user says bounce from lower band, use `L <= BBandBot(...) AND C > BBandBot(...)`.
- If the user says crosses back above lower band, use `Cross(C, BBandBot(...))`.
- If the user says upper-band reversal, use upper-band logic with `H` and `C`.

## Pitfalls

- Do not treat every close below the lower band as a mean-reversion signal; that is an outside-band condition, not necessarily a rebound.
- Do not use `BBandTop` for lower-band bounce logic.
- Do not use `Cross` when the user asks for a touch-and-close condition.
- Do not invent unsupported functions such as `BollingerReversion()`.
- Do not use broad aliases like `reversal` alone because many non-Bollinger patterns use that word.

## Test Queries

- Find stocks bouncing from the lower Bollinger Band
- Find stocks where close crosses back above the lower Bollinger Band
- Find stocks reversing down from the upper Bollinger Band
