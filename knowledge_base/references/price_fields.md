---
type: reference
category: price_fields
source: MetaStock Formula Primer
priority: high
status: patched
---

# Price Fields

## Purpose

This card defines the standard MetaStock price and volume field abbreviations.

It helps the RAG system convert natural language price terms such as “close”, “high”, “low”, and “volume” into valid MetaStock formula keywords.

## Field mappings

| Natural language | MetaStock keyword | Abbreviation |
|---|---|---|
| Open | Open | O |
| High | High | H |
| Low | Low | L |
| Close | Close | C |
| Volume | Volume | V |
| Open Interest | Open Interest | OI |

The abbreviated form is preferred for generated Explorer formulas.

## Formula mappings

```text
close = C
closing price = C
last price = C
price = C, unless another price field is specified
open = O
opening price = O
high = H
highest price of current bar = H
low = L
lowest price of current bar = L
volume = V
trading volume = V
open interest = OI
```

## Natural language mappings

Use this card when the user says:

- close
- closing price
- last price
- price
- stock price
- current price
- open
- opening price
- high
- highest price
- low
- lowest price
- volume
- trading volume
- average volume
- volume above average
- volume above average volume
- price field
- OHLC
- OHLCV
- close above moving average
- close below moving average
- high breaks previous high
- low breaks previous low
- close makes new high
- close makes new low

## Default interpretation

If the user says “price” without specifying open, high, low, or close, use close:

```metastock
C
```

If the user says “volume”, use:

```metastock
V
```

If the user says “high”, use:

```metastock
H
```

If the user says “low”, use:

```metastock
L
```

## Common formulas

Close price:

```metastock
C
```

Volume:

```metastock
V
```

Daily range:

```metastock
H - L
```

Close above open:

```metastock
C > O
```

Close above previous close:

```metastock
C > Ref(C,-1)
```

Volume above previous volume:

```metastock
V > Ref(V,-1)
```

## Explorer examples

### Example 1: Close above open

User request:

```text
Find stocks where close is above open
```

Explorer output:

```text
Column A: C
Column B: O
Filter: ColA > ColB
```

### Example 2: Volume above previous volume

User request:

```text
Find stocks where volume is above yesterday volume
```

Explorer output:

```text
Column A: V
Column B: Ref(V,-1)
Filter: ColA > ColB
```

### Example 3: Close above moving average

User request:

```text
Find stocks where close is above 50 day moving average
```

Explorer output:

```text
Column A: C
Column B: Mov(C,50,S)
Filter: ColA > ColB
```

Notes:

```text
Close is mapped to C.
50 day moving average is mapped to Mov(C,50,S).
```

### Example 4: Volume above average volume

User request:

```text
Find stocks where volume is above 20 day average volume
```

Explorer output:

```text
Column A: V
Column B: Mov(V,20,S)
Filter: ColA > ColB
```

Notes:

```text
Volume is mapped to V.
20 day average volume is mapped to Mov(V,20,S).
```

## Good outputs

Good:

```metastock
C
```

Good:

```metastock
V
```

Good:

```metastock
C > O
```

Good:

```text
Column A: C
Column B: Mov(C,50,S)
Filter: ColA > ColB
```

Good:

```text
Column A: V
Column B: Mov(V,20,S)
Filter: ColA > ColB
```

## What not to do

Do not use natural language price names inside generated formulas.

Bad:

```metastock
close > moving average(close, 50)
```

Correct:

```metastock
C > Mov(C,50,S)
```

Do not invent object-style field names.

Bad:

```metastock
price.close
```

Correct:

```metastock
C
```

Do not write volume as a lowercase natural-language word inside formulas.

Bad:

```metastock
volume > Mov(volume,20,S)
```

Correct:

```metastock
V > Mov(V,20,S)
```

Do not assume “price” means high or low unless the user says so.

Bad:

```text
User says: price above moving average
Output: H > Mov(H,50,S)
```

Correct:

```text
User says: price above moving average
Output: C > Mov(C,50,S)
```

## Assumptions

- If the user says price without specifying open, high, low, or close, use close `C`.
- If the user says close or closing price, use `C`.
- If the user says volume or trading volume, use `V`.
- If the user says current high, use `H`.
- If the user says current low, use `L`.
- Prefer abbreviations `O`, `H`, `L`, `C`, `V`, and `OI` in generated formulas.

## Related functions and concepts

Useful related cards:

- Mov: moving average of price or volume
- Ref: previous bar reference
- HHV: highest high/value over a period
- LLV: lowest low/value over a period
- Cross: crossover detection

## Retrieval keywords

Open, O, High, H, Low, L, Close, C, Volume, V, Open Interest, OI, price field, closing price, trading volume, OHLC, OHLCV, close above moving average, price above moving average, volume above average volume, high breakout, low breakdown, MetaStock price field, Explorer price field.
