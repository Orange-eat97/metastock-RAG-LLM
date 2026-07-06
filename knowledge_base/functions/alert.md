---
canonical_id: function.alert
title: Alert
type: function
card_bucket: functions
category: event_window
source: MetaStock Formula Primer
status: active
priority: 10
supports_explorer: true
function: Alert
aliases:
- text: Alert
  type: exact
  weight: 1.0
- text: alert within last N bars
  type: synonym
  weight: 0.85
- text: recent crossover
  type: phrase
  weight: 0.9
- text: event occurred within 5 bars
  type: synonym
  weight: 0.85
- text: Alert function
  type: synonym
  weight: 0.85
- text: signal in recent periods
  type: synonym
  weight: 0.85
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
semantic:
  concept_role: function
  mechanism: event_window
  market_object: price
  outputs:
  - boolean_or_conditional_value
  supports_conditions:
  - threshold_comparison
  - crossover
  - state_filter
  does_not_cover:
  - complete_trading_pattern_by_itself
registry:
  enabled: true
  canonical_id: function.alert
  supports_explorer: true
  priority: 10
  properties:
    formula_role: event_window
    supports_explorer: true
    source_path: functions/alert.md
    generated_schema_version: registry_ready_v2
---

# Alert

## Purpose

`Alert` keeps an expression true for a specified number of periods after it occurs. In Explorer generation it is useful for recent-event scans such as a crossover within the last 5 bars.

## Syntax

```metastock
Alert(EXPRESSION, PERIODS)
```

## Parameters

- `EXPRESSION`: Condition or event to extend
- `PERIODS`: Number of periods to keep the result true

## Valid Examples

```metastock
Alert(Cross(RSI(14),70),5)
Alert(Cross(C,Mov(C,50,S)),3)
Alert(C > Ref(HHV(C,20),-1),5)
```

## Common Mistakes

- Do not confuse `Alert` with Expert Advisor pop-up alerts only; here it extends a true condition.
- Do not use `Alert` when the user asks for an event only on the current bar.
- Do not pass natural language as the expression.

## Related Patterns

- pattern.alert_recent_event

## Natural Language Mappings

Use this function when the user says:

- alert within last N bars
- recent crossover
- event occurred within 5 bars
- Alert function
- signal in recent periods

## Assumptions

- Use this function only when the user request explicitly maps to this concept.

## Retrieval keywords

alert within last N bars, recent crossover, event occurred within 5 bars, Alert function, signal in recent periods, Alert, Alert(EXPRESSION, PERIODS).

## Test Queries

- Find stocks using Alert
