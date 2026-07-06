# MetaStock Knowledge Base — Current Inclusion and Upload Documentation

Date: 2026-07-06
Project: `metastock-RAG-LLM`
Knowledge root: `knowledge_base/`

## 1. Current status summary

The knowledge base has been expanded from the earlier small MVP card set into a registry-ready MetaStock RAG knowledge base.

Current registry-enabled card set:

| Item | Count |
|---|---:|
| Registry-enabled cards | 91 |
| Function cards | 44 |
| Pattern cards | 34 |
| Reference cards | 13 |
| Force-retrieval template cards | 2 |
| Alias rows planned by dry run | 545 |
| Dependency edges planned by dry run | 208 before missing-target filtering |

The two template cards below are intentionally excluded from registry graph sync because they are handled as force-retrieval/base-context items:

```text
knowledge_base/templates/explorer_basic.md
knowledge_base/templates/explorer_columns_filter.md
```

They should remain in the local knowledge base and RAG context, but they do not need entries in:

```text
rag_card_registry
rag_card_aliases
rag_card_dependencies
```

## 2. What has been included in the knowledge base

The current knowledge base contains three registry-enabled buckets:

```text
knowledge_base/functions/
knowledge_base/patterns/
knowledge_base/references/
```

It also contains a force-retrieval template bucket:

```text
knowledge_base/templates/
```

The knowledge base now covers:

1. Core MetaStock formula functions.
2. Momentum indicators.
3. Moving averages and trend filters.
4. Highest/lowest lookback functions.
5. Time-reference and event-reference functions.
6. Bollinger Band functions and patterns.
7. Volatility, ATR, standard deviation, and trailing-stop patterns.
8. Stochastic, Williams %R, ADX, PDI/MDI, Aroon, RVI indicators.
9. ZigZag, Peak/Trough, divergence, and repaint-warning references.
10. Candlestick reversal function references and Explorer load-record warnings.
11. Explorer-specific limitations and formula-generation constraints.
12. System Tester vs Explorer limitations.
13. External formula references through `Fml`, `FmlVar`, and `Security`.
14. Commentary-only functions such as `WriteIf` and `WriteVal`, marked as knowledge/reference support rather than normal Explorer scan functions where applicable.

## 3. Registry-ready metadata included in each registry-enabled card

Each registry-enabled card is expected to contain frontmatter for:

```yaml
canonical_id: <stable canonical id>
title: <human-readable title>
type: function | pattern | reference | template | example | pitfall
card_bucket: functions | patterns | references | templates | examples | pitfalls
category: <debug/filter category>
source: generated | primer | primer_ii | manual | internal
status: active
priority: <integer priority>
supports_explorer: true | false
```

Each registry-enabled card also includes:

```yaml
aliases:
  - text: <user phrase>
    type: exact | synonym | phrase | abbreviation | weak_hint
    weight: <0.0 to 1.0>

requires:
  - canonical_id: <canonical id>
    rationale: <why this dependency is needed>
    priority: <integer>
    properties: {}

suggests:
  - canonical_id: <canonical id>
    rationale: <why this related card is useful>
    priority: <integer>
    properties: {}

semantic:
  concept_role: function | pattern | reference | template
  mechanism: <what this card does>
  market_object: <price/volume/indicator/explorer/etc.>
  outputs: []
  supports_conditions: []
  operations_supported: []
  required_components: []
  does_not_cover: []
```

Supported dependency edge types are:

```text
requires
suggests
conflicts_with
forbids
similar_to
expands_to
```

## 4. Supabase tables covered

The current upload/sync design separates the main RAG document upload from the registry graph upload.

### 4.1 RAG document layer

These rows are managed by the card upload/embedding workflow:

```text
rag_cards
rag_card_embeddings
```

Each card body is stored as a RAG document, and embeddings are stored separately for retrieval.

### 4.2 Registry graph layer

These rows are managed by `sync_registry_graph_from_cards.py`:

```text
rag_card_registry
rag_card_aliases
rag_card_dependencies
```

The registry graph lets the planner:

1. Resolve canonical IDs.
2. Match user phrases through aliases.
3. Expand related cards through `requires` and `suggests` edges.

## 5. Registry graph sync script currently used

Current script:

```text
scripts/sync_registry_graph_from_cards.py
```

Purpose:

```text
Read registry-ready markdown frontmatter and sync:
- rag_card_registry
- rag_card_aliases
- rag_card_dependencies
```

It does not upload card body markdown, embeddings, or semantic profiles.

It upserts with these conflict keys:

```text
rag_card_registry: canonical_id
rag_card_aliases: canonical_id, alias_text
rag_card_dependencies: from_canonical_id, to_canonical_id, edge_type
```

Dry run:

```powershell
python scripts/sync_registry_graph_from_cards.py --knowledge-dir knowledge_base
```

Apply:

```powershell
python scripts/sync_registry_graph_from_cards.py --knowledge-dir knowledge_base --apply
```

Apply with RAG-card existence check:

```powershell
python scripts/sync_registry_graph_from_cards.py --knowledge-dir knowledge_base --apply --require-rag-cards
```

Do not use `--fail-missing-dependency-targets` while the two templates are intentionally skipped, unless all template dependency edges have first been removed or those template nodes have been registered.

## 6. Registry-enabled function cards included

Total: 44

```text
function.abs                 functions/abs.md
function.adx                 functions/adx.md
function.alert               functions/alert.md
function.aroondown           functions/aroondown.md
function.aroonup             functions/aroonup.md
function.atan                functions/atan.md
function.atr                 functions/atr.md
function.barssince           functions/barssince.md
function.bbandbot            functions/bbandbot.md
function.bbandtop            functions/bbandtop.md
function.cos                 functions/cos.md
function.cum                 functions/cum.md
function.divergence          functions/divergence.md
function.fml                 functions/fml.md
function.fmlvar              functions/fmlvar.md
function.if                  functions/if.md
function.input               functions/input.md
function.macd                functions/macd.md
function.max                 functions/max.md
function.mdi                 functions/mdi.md
function.min                 functions/min.md
function.pdi                 functions/pdi.md
function.peak                functions/peak.md
function.peakbars            functions/peakbars.md
function.roc                 functions/roc.md
function.round               functions/round.md
function.rvi                 functions/rvi.md
function.security            functions/security.md
function.sin                 functions/sin.md
function.sqrt                functions/sqrt.md
function.stdev               functions/stdev.md
function.stoch               functions/stoch.md
function.stochmomentum       functions/stochmomentum.md
function.sum                 functions/sum.md
function.trough              functions/trough.md
function.troughbars          functions/troughbars.md
function.typical             functions/typical.md
function.valuewhen           functions/valuewhen.md
function.var                 functions/var.md
function.wilders             functions/wilders.md
function.willr               functions/willr.md
function.writeif             functions/writeif.md
function.writeval            functions/writeval.md
function.zig                 functions/zig.md
```

## 7. Registry-enabled pattern cards included

Total: 34

```text
pattern.adx_trend_strength             patterns/adx_trend_strength.md
pattern.alert_recent_event             patterns/alert_recent_event.md
pattern.aroon_trend                    patterns/aroon_trend.md
pattern.atr_trailing_stop              patterns/atr_trailing_stop.md
pattern.bearish_candlestick_reversal   patterns/bearish_candlestick_reversal.md
pattern.big_white_black_candle         patterns/big_white_black_candle.md
pattern.bollinger_band_breakout        patterns/bollinger_band_breakout.md
pattern.bollinger_band_mean_reversion  patterns/bollinger_band_mean_reversion.md
pattern.bollinger_band_squeeze         patterns/bollinger_band_squeeze.md
pattern.bullish_candlestick_reversal   patterns/bullish_candlestick_reversal.md
pattern.consecutive_condition          patterns/consecutive_condition.md
pattern.dark_cloud_cover               patterns/dark_cloud_cover.md
pattern.harami                         patterns/harami.md
pattern.harami_cross                   patterns/harami_cross.md
pattern.higher_timeframe_approximation patterns/higher_timeframe_approximation.md
pattern.logical_switch_state_machine   patterns/logical_switch_state_machine.md
pattern.ma_crossover                   patterns/ma_crossover.md
pattern.ma_support_bounce              patterns/ma_support_bounce.md
pattern.macd_crossover                 patterns/macd_crossover.md
pattern.macd_divergence                patterns/macd_divergence.md
pattern.peak_trough_breakout           patterns/peak_trough_breakout.md
pattern.pivot_high_low                 patterns/pivot_high_low.md
pattern.pivot_points                   patterns/pivot_points.md
pattern.profit_target_stop             patterns/profit_target_stop.md
pattern.relative_security_strength     patterns/relative_security_strength.md
pattern.rsi_divergence                 patterns/rsi_divergence.md
pattern.rsi_recovery                   patterns/rsi_recovery.md
pattern.standard_deviation_breakout    patterns/standard_deviation_breakout.md
pattern.stochastic_oversold_recovery   patterns/stochastic_oversold_recovery.md
pattern.time_based_exit                patterns/time_based_exit.md
pattern.volatility_contraction         patterns/volatility_contraction.md
pattern.volatility_expansion           patterns/volatility_expansion.md
pattern.williams_r_recovery            patterns/williams_r_recovery.md
pattern.zigzag_swing_reversal          patterns/zigzag_swing_reversal.md
```

## 8. Registry-enabled reference cards included

Total: 13

```text
reference.candlestick_exploration_load_records   references/candlestick_exploration_load_records.md
reference.candlestick_functions                  references/candlestick_functions.md
reference.commentary_writeif_writeval            references/commentary_writeif_writeval.md
reference.explorer_environment_limitations       references/explorer_environment_limitations.md
reference.formula_reference_external_dependencies references/formula_reference_external_dependencies.md
reference.formula_variables                      references/formula_variables.md
reference.higher_timeframe_explorer_limitations  references/higher_timeframe_explorer_limitations.md
reference.input_limitations                      references/input_limitations.md
reference.logical_operators                      references/logical_operators.md
reference.lookahead_future_reference_pitfalls    references/lookahead_future_reference_pitfalls.md
reference.prev_usage_and_circular_logic          references/prev_usage_and_circular_logic.md
reference.system_tester_vs_explorer_limits       references/system_tester_vs_explorer_limits.md
reference.zigzag_based_function_repaint_pitfall  references/zigzag_based_function_repaint_pitfall.md
```

## 9. Force-retrieval template cards retained locally but skipped from registry

Total: 2

```text
template.explorer_basic           templates/explorer_basic.md
template.explorer_columns_filter  templates/explorer_columns_filter.md
```

These are still important for generation because they define output shape and column/filter rules, but they are retrieved by deterministic force-retrieval logic rather than alias/dependency graph expansion.

The key rules they provide are:

1. Use `Column A`, `Column B`, etc. before referencing `ColA`, `ColB`, etc.
2. Do not reference undefined columns.
3. Do not use `Ref(ColA,-1)` because Explorer column references are last-value references, not historical arrays.
4. Use `AND`, `OR`, and `=` rather than programming operators such as `&&`, `||`, or `==`.
5. Do not place natural language inside formulas.

## 10. Main dependency graph coverage

The dependency graph includes `requires` and `suggests` edges that allow important cards to retrieve their supporting syntax.

Examples:

```text
pattern.macd_crossover
  requires function.macd
  requires function.mov
  requires function.cross

pattern.bollinger_band_squeeze
  requires function.bbandtop
  requires function.bbandbot
  suggests function.mov
  suggests pattern.bollinger_band_breakout

pattern.atr_trailing_stop
  requires function.atr
  suggests function.hhv
  suggests function.llv

pattern.rsi_divergence
  requires function.rsi
  suggests function.divergence
  suggests function.llv
  suggests function.valuewhen

pattern.ma_crossover
  requires function.mov
  requires function.cross

pattern.consecutive_condition
  requires function.sum
  suggests function.ref
```

Some planned dependency edges point to the skipped template cards. If those templates are not present in `rag_card_registry`, the registry script should warn and skip those dependency edges during apply. This is acceptable because templates are force-retrieval items.

## 11. What this enables in retrieval/generation

The current knowledge base supports four layers of context:

1. **Exact syntax cards**: functions such as `Mov`, `RSI`, `Cross`, `Ref`, `HHV`, `LLV`, `MACD`, `ATR`, `Stoch`, `ADX`, `Security`, `Fml`, etc.
2. **Reusable trading pattern cards**: breakout, moving-average crossover, Bollinger squeeze, ATR trailing stop, RSI divergence, MACD divergence, candlestick reversals, volatility expansion/contraction, etc.
3. **Reference/constraint cards**: Explorer environment limitations, lookahead/future-reference pitfalls, System Tester vs Explorer limits, Input limitations, ZigZag repaint pitfalls, formula variables.
4. **Force-retrieved output templates**: Explorer output shape and column/filter rules.

This should allow the planner to resolve user queries into canonical concepts, retrieve required syntax, include constraint cards, and prevent common formula-generation mistakes.

## 12. Recommended validation after upload

### 12.1 Registry row resolves to card

```sql
select
    canonical_id,
    source_path,
    registry_title,
    card_title,
    case
        when card_id is null then 'MISSING rag_cards MATCH'
        else 'OK'
    end as status
from public.v_rag_card_registry_resolved
where canonical_id in (
    'function.macd',
    'pattern.macd_crossover',
    'pattern.bollinger_band_squeeze',
    'pattern.atr_trailing_stop',
    'reference.explorer_environment_limitations'
);
```

### 12.2 Alias types are valid

```sql
select distinct alias_type
from public.rag_card_aliases
order by alias_type;
```

Expected:

```text
abbreviation
exact
phrase
synonym
weak_hint
```

### 12.3 Alias matching works

```sql
select *
from public.match_rag_card_aliases(
    'Find stocks where MACD crosses above its signal line',
    0.5
);
```

Expected to include:

```text
pattern.macd_crossover
function.macd
function.cross
```

### 12.4 Dependency expansion works

```sql
select *
from public.expand_rag_card_dependencies(
    array['pattern.macd_crossover'],
    array['requires', 'suggests'],
    5
);
```

Expected to include:

```text
pattern.macd_crossover
function.macd
function.cross
function.mov
```

### 12.5 Retrieval dry-run checks

```powershell
python -m src.generate_explorer "Find stocks where MACD crosses above its signal line" --dry-run
python -m src.generate_explorer "Find stocks with a Bollinger Band squeeze breakout" --dry-run
python -m src.generate_explorer "Find stocks where close is above a 2 ATR trailing stop" --dry-run
python -m src.generate_explorer "Find stocks making a new 20 day high with volume above average" --dry-run
```

Expected behavior:

```text
- Existing canonical IDs are resolved instead of being suggested as missing cards.
- Required function cards are force-included through dependency expansion.
- Explorer templates are included by deterministic force retrieval.
- The final prompt contains syntax cards, pattern cards, reference/constraint cards, and Explorer output rules.
```

## 13. Current caveats

1. The two template cards are intentionally skipped from registry. Any dependency edge pointing to `template.explorer_columns_filter` will be skipped unless a registry node is created for that template.
2. The registry graph script upserts rows but does not delete stale aliases/dependencies. If a card’s aliases or dependencies are changed, delete old rows for that `canonical_id` before re-running `--apply`.
3. The semantic frontmatter is stored in card metadata. There is no required `rag_card_semantic_profiles` table in the current workflow.
4. Generated and upgraded cards should still be tested through retrieval dry-runs and MetaStock formula acceptance checks.
5. Some advanced cards, especially `Zig`, `Peak`, `Trough`, and `Divergence`, include repaint/uncertainty caveats and should be used carefully in Explorer filters.

## 14. Practical next step

After templates are marked with:

```yaml
registry:
  enabled: false
```

run:

```powershell
python scripts/sync_registry_graph_from_cards.py --knowledge-dir knowledge_base
```

Then, if errors are zero:

```powershell
python scripts/sync_registry_graph_from_cards.py --knowledge-dir knowledge_base --apply --require-rag-cards
```

If dependency warnings appear only for skipped template nodes, this is acceptable under the current force-retrieval design.
