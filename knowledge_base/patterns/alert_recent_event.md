---
canonical_id: pattern.alert_recent_event
title: 'Pattern: Recent Event Alert Window'
type: pattern
card_bucket: patterns
category: event_window
source: MetaStock Formula Primer / Formula Primer II / internal project pattern
status: active
priority: 10
supports_explorer: true
functions:
- Alert
- Cross
- Ref
- HHV
- Mov
aliases:
- text: 'Pattern: Recent Event Alert Window'
  type: synonym
  weight: 0.85
- text: Recent Event Alert Window
  type: exact
  weight: 1.0
- text: recent crossover within 5 bars
  type: phrase
  weight: 0.9
- text: event occurred within last 3 bars
  type: synonym
  weight: 0.85
- text: breakout in recent periods
  type: phrase
  weight: 0.9
- text: Alert function recent signal
  type: synonym
  weight: 0.85
- text: signal happened within N days
  type: synonym
  weight: 0.85
requires:
- canonical_id: function.alert
  rationale: This card usually needs function.alert for correct formula generation.
  priority: 10
  properties:
    source: registry_ready_transform
    formula_role: requires
suggests:
- canonical_id: function.cross
  rationale: function.cross is often useful context for this card but is not always mandatory.
  priority: 40
  properties:
    source: registry_ready_transform
    formula_role: suggests
- canonical_id: function.ref
  rationale: function.ref is often useful context for this card but is not always mandatory.
  priority: 40
  properties:
    source: registry_ready_transform
    formula_role: suggests
- canonical_id: function.hhv
  rationale: function.hhv is often useful context for this card but is not always mandatory.
  priority: 40
  properties:
    source: registry_ready_transform
    formula_role: suggests
- canonical_id: function.mov
  rationale: function.mov is often useful context for this card but is not always mandatory.
  priority: 40
  properties:
    source: registry_ready_transform
    formula_role: suggests
semantic:
  concept_role: pattern
  mechanism: event_window
  market_object: price
  directions_supported:
  - bullish
  - bearish
  operations_supported:
  - event_window
  required_components:
  - alert
  does_not_cover:
  - unrelated_pattern_substitution
  - guaranteed_trade_profitability
registry:
  enabled: true
  canonical_id: pattern.alert_recent_event
  supports_explorer: true
  priority: 10
  properties:
    formula_role: event_window
    supports_explorer: true
    source_path: patterns/alert_recent_event.md
    generated_schema_version: registry_ready_v2
---

# Pattern: Recent Event Alert Window

## Intent

Detect securities where an event occurred within a recent window, using `Alert(EXPRESSION,N)` to keep the condition true.

## Natural Language Triggers

- recent crossover within 5 bars
- event occurred within last 3 bars
- breakout in recent periods
- Alert function recent signal
- signal happened within N days

## Required Logical Components

- Define the event expression, such as a Cross or breakout.
- Choose a lookback window in periods.
- Wrap the event with `Alert(event,N)`.
- Use only when user wants recent event, not necessarily current-bar event.

## Formula Building Blocks

```metastock
Alert(Cross(C,Mov(C,50,S)),5)
Alert(C > Ref(HHV(C,20),-1),3)
Alert(Cross(RSI(14),30),5)
```

## Example Compositions

```metastock
Alert(Cross(C,Mov(C,50,S)),5)
Alert(C > Ref(HHV(C,20),-1),3)
```

## Default Assumptions

- Default recent window is 5 periods if user says recent without a number.
- Alert extends true result for N periods.
- Use Cross directly for current-bar event.

## Pitfalls

- Do not use Alert when the user wants the event today only.
- Do not pass natural language into Alert.
- Do not confuse Alert with Expert Advisor notification text.

## Related functions and concepts

- function.alert
- function.cross
- function.ref
- function.hhv
- function.mov

## Retrieval keywords

recent crossover within 5 bars, event occurred within last 3 bars, breakout in recent periods, Alert function recent signal, signal happened within N days, Alert, Cross, Ref, HHV, Mov.

## Test Queries

- Find stocks where price crossed above 50 MA within the last 5 bars
- Find recent breakout within 3 days
