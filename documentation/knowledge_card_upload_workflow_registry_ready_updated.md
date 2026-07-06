# Knowledge Card Upload Workflow — Registry-Ready Version

This workflow describes how to create, upload, and register MetaStock RAG knowledge cards so that each card works as both:

1. a RAG document stored in `rag_cards` and embedded into `rag_card_embeddings`; and
2. a planning graph node registered in `rag_card_registry`, searchable through `rag_card_aliases`, and expandable through `rag_card_dependencies`.

The important change is that every generated knowledge card must now contain enough machine-readable metadata for registry, alias, and dependency sync. Do **not** rely on the card title to infer aliases or dependencies.

---

## 1. Required folder layout

Place cards under `knowledge_base/` using the correct bucket folder:

```text
knowledge_base/
  functions/
  patterns/
  references/
  templates/
  examples/
  pitfalls/
```

Example paths:

```text
knowledge_base/functions/macd.md
knowledge_base/patterns/bollinger_band_squeeze.md
knowledge_base/references/logical_operators.md
```

The `source_path` stored in Supabase should be relative to `knowledge_base/`:

```text
functions/macd.md
patterns/bollinger_band_squeeze.md
references/logical_operators.md
```

---

## 2. Canonical ID rules

Every card must have a stable `canonical_id` in frontmatter.

Use these prefixes:

```text
function.<name>
pattern.<name>
reference.<name>
template.<name>
example.<name>
pitfall.<name>
```

Examples:

```text
function.macd
function.atr
function.bbandtop
pattern.macd_crossover
pattern.bollinger_band_squeeze
reference.logical_operators
```

Rules:

```text
[ ] Use lowercase.
[ ] Use underscores, not spaces or hyphens.
[ ] Use canonical IDs in dependencies, never display titles.
[ ] Do not rename canonical IDs after upload unless you also migrate aliases, dependencies, embeddings, and tests.
```

---

## 3. Required frontmatter schema

Every generated card must start with YAML frontmatter.

### 3.1 Minimum required fields

```yaml
---
canonical_id: function.macd
title: MACD
type: function
card_bucket: functions
category: momentum
source: generated
status: active
priority: 10
supports_explorer: true
---
```

Field meanings:

| Field | Required | Purpose |
|---|---:|---|
| `canonical_id` | yes | Primary registry key in `rag_card_registry`. |
| `title` | yes | Human-readable card title. |
| `type` | yes | One of `function`, `pattern`, `reference`, `template`, `example`, `pitfall`. |
| `card_bucket` | yes | One of `functions`, `patterns`, `references`, `templates`, `examples`, `pitfalls`. |
| `category` | yes | Short category used for filtering and debugging. |
| `source` | yes | `manual`, `generated`, `primer`, `primer_ii`, etc. |
| `status` | yes | Usually `active`. |
| `priority` | yes | Retrieval/planning priority. Lower means more important. |
| `supports_explorer` | yes | Whether this card is relevant to MetaStock Explorer generation. |

---

## 4. Alias metadata requirements

Aliases tell the query decomposer how users may refer to this card.

### 4.1 Allowed alias types

The current database constraint allows only:

```text
exact
synonym
phrase
abbreviation
weak_hint
```

Do **not** generate unsupported alias types such as:

```text
title
primary
keyword
trigger
related_term
```

### 4.2 Required alias format

Use object-style aliases so the sync script can directly upsert `rag_card_aliases`.

```yaml
aliases:
  - text: MACD
    type: abbreviation
    weight: 1.0
  - text: moving average convergence divergence
    type: exact
    weight: 1.0
  - text: MACD line
    type: phrase
    weight: 0.9
  - text: signal line
    type: weak_hint
    weight: 0.65
```

### 4.3 Alias type guide

| Alias type | Use when | Example |
|---|---|---|
| `exact` | The phrase directly names the concept. | `moving average convergence divergence` |
| `abbreviation` | The phrase is a ticker-like/function abbreviation. | `MACD`, `ATR`, `RSI` |
| `phrase` | The phrase is a user query phrase strongly pointing to this card. | `MACD crosses above signal line` |
| `synonym` | The phrase is a semantic equivalent. | `above average volume` for volume-above-average |
| `weak_hint` | The phrase is related but insufficient alone. | `signal line`, `upper band` |

### 4.4 Alias quality rules

Good aliases are specific:

```yaml
aliases:
  - text: MACD crossover
    type: exact
    weight: 1.0
  - text: MACD crosses above signal line
    type: phrase
    weight: 0.95
  - text: bullish MACD cross
    type: phrase
    weight: 0.9
```

Bad aliases are too broad:

```yaml
aliases:
  - text: cross
    type: exact
    weight: 1.0
  - text: signal
    type: exact
    weight: 1.0
  - text: trend
    type: exact
    weight: 1.0
```

Why: broad aliases cause unrelated cards to be force-retrieved.

Use broad words only as `weak_hint` with lower weight, and only when they are useful in combination with other terms.

---

## 5. Dependency metadata requirements

Dependencies tell the registry graph which cards should be retrieved together.

### 5.1 Supported dependency keys

```yaml
requires:
suggests:
conflicts_with:
forbids:
similar_to:
expands_to:
```

For current query decomposition expansion, the main runtime edges are:

```text
requires
suggests
```

Other edge types can be stored for future filtering, reranking, or validation, but they may not be expanded by default.

### 5.2 Required dependency format

Use object-style dependencies when possible.

```yaml
requires:
  - canonical_id: function.macd
    rationale: MACD crossover requires the MACD function or indicator concept.
    properties:
      formula_role: indicator_series
  - canonical_id: function.cross
    rationale: MACD crossover requires Cross to detect the crossing event.
    properties:
      formula_role: crossing_event

suggests:
  - canonical_id: function.mov
    rationale: MACD signal-line examples often use moving-average smoothing.
    properties:
      formula_role: signal_smoothing
```

Simple list format is allowed only when no rationale is available:

```yaml
requires:
  - function.macd
  - function.cross
```

The sync script should normalize both formats into `rag_card_dependencies`.

### 5.3 Dependency edge rules

Use `requires` only when the card is usually wrong or incomplete without that dependency.

Examples:

```yaml
# Good: MACD crossover pattern needs MACD and Cross.
requires:
  - canonical_id: function.macd
  - canonical_id: function.cross
```

```yaml
# Good: Bollinger squeeze pattern needs Bollinger band functions.
requires:
  - canonical_id: function.bbandtop
  - canonical_id: function.bbandbot
```

```yaml
# Good: Cross often uses Mov, but can also compare RSI, MACD, constants, etc.
suggests:
  - canonical_id: function.mov
```

Do not overuse `requires`. Too many required edges bloats the prompt and can retrieve irrelevant context.

---

## 6. Semantic coverage metadata

The query decomposition coverage verifier uses actual card evidence from `rag_cards`, so the body must clearly explain what the card covers and what it does not cover.

Add a compact `semantic` block in frontmatter for machine readability.

### 6.1 Function card semantic block

```yaml
semantic:
  concept_role: function
  mechanism: indicator_calculation
  market_object: price
  outputs:
    - indicator_series
  supports_conditions:
    - threshold_comparison
    - crossover
  does_not_cover:
    - trading_pattern_by_itself
```

### 6.2 Pattern card semantic block

```yaml
semantic:
  concept_role: pattern
  mechanism: volatility_squeeze
  market_object: price
  directions_supported:
    - bullish
    - bearish
  operations_supported:
    - squeeze_detection
    - breakout_confirmation
  required_components:
    - band_width_compression
    - price_breakout_optional
  does_not_cover:
    - simple_moving_average_crossover
    - inter_bar_gap
```

This helps avoid bad substitutions such as:

```text
gap up → pattern.breakout
ATR trailing stop → function.mov
Bollinger squeeze → pattern.breakout only
MACD → function.cross only
```

---

## 7. Required body sections

The card body must be useful for formula generation and coverage verification.

### 7.1 Pattern cards

```markdown
# Pattern: <Name>

## Intent
Describe the trading condition in plain English.

## Natural Language Triggers
- phrases users may type
- synonyms
- common variants

## Required Logical Components
- exact logical pieces needed for the pattern

## Formula Building Blocks
```metastock
MetaStock snippets needed to build the pattern
```

## Example Compositions
```metastock
Complete valid Explorer filter examples
```

## Default Assumptions
- default period
- default price field
- whether current bar is included or excluded

## Pitfalls
- invalid syntax
- future-looking mistakes
- ambiguous interpretations

## Test Queries
- user query that should retrieve this card
```

Pattern-card rule:

```text
A pattern card must describe a reusable trading idea, not just one formula.
```

### 7.2 Function cards

```markdown
# <Function Name>

## Purpose
What the function does.

## Syntax
```metastock
FunctionName(ARGUMENTS)
```

## Parameters
- argument name and meaning

## Valid Examples
```metastock
Valid MetaStock formulas
```

## Common Mistakes
- invalid argument order
- wrong data array
- wrong period usage

## Related Patterns
- pattern cards that commonly require this function

## Test Queries
- user query that should retrieve this card
```

Function-card rule:

```text
A function card must teach correct MetaStock usage, not merely define the function.
```

### 7.3 Reference/template cards

```markdown
# <Reference or Template Name>

## Purpose
What global rule this card provides.

## Rules
- mandatory constraints
- syntax rules
- output formatting requirements

## Examples
```metastock
Valid usage examples
```

## What Not To Do
- invalid output shapes
- invalid formula references

## Test Queries
- user query that should retrieve this card
```

Reference/template rule:

```text
Reference/template cards should be stable base context and should not depend on one specific user query.
```

---

## 8. Complete examples

### 8.1 Function card example: MACD

```md
---
canonical_id: function.macd
title: MACD
type: function
card_bucket: functions
category: momentum
source: generated
status: active
priority: 10
supports_explorer: true

aliases:
  - text: MACD
    type: abbreviation
    weight: 1.0
  - text: moving average convergence divergence
    type: exact
    weight: 1.0
  - text: MACD line
    type: phrase
    weight: 0.9
  - text: MACD histogram
    type: phrase
    weight: 0.85
  - text: signal line
    type: weak_hint
    weight: 0.65

suggests:
  - canonical_id: function.mov
    rationale: MACD signal-line examples often use moving-average smoothing.
    properties:
      formula_role: signal_smoothing

semantic:
  concept_role: function
  mechanism: momentum_indicator
  market_object: price
  outputs:
    - macd_series
  supports_conditions:
    - threshold_comparison
    - crossover
  does_not_cover:
    - crossing_event_by_itself
---

# MACD

## Purpose
Explain what MACD measures and when it is used.

## Syntax
```metastock
MACD()
```

## Parameters
Describe whether MetaStock MACD uses default parameters or explicit variants.

## Valid Examples
```metastock
MACD() > 0
Cross(MACD(), Mov(MACD(),9,E))
```

## Common Mistakes
Do not write `MACD` without parentheses. Do not treat `Cross` as a replacement for the MACD function.

## Related Patterns
- pattern.macd_crossover

## Test Queries
- Find stocks where MACD crosses above its signal line
```

### 8.2 Pattern card example: MACD Crossover

```md
---
canonical_id: pattern.macd_crossover
title: Pattern: MACD Crossover
type: pattern
card_bucket: patterns
category: momentum_crossover
source: generated
status: active
priority: 10
supports_explorer: true

aliases:
  - text: MACD crossover
    type: exact
    weight: 1.0
  - text: MACD crosses above signal line
    type: phrase
    weight: 0.95
  - text: bullish MACD cross
    type: phrase
    weight: 0.9
  - text: MACD bearish cross
    type: phrase
    weight: 0.9

requires:
  - canonical_id: function.macd
    rationale: The pattern requires the MACD indicator series.
    properties:
      formula_role: indicator_series
  - canonical_id: function.cross
    rationale: The pattern requires Cross to detect the crossover event.
    properties:
      formula_role: crossing_event
suggests:
  - canonical_id: function.mov
    rationale: The MACD signal line is commonly represented with smoothing.
    properties:
      formula_role: signal_line

semantic:
  concept_role: pattern
  mechanism: indicator_crossover
  market_object: price
  operations_supported:
    - macd_cross_above_signal
    - macd_cross_below_signal
  required_components:
    - macd_series
    - signal_line
    - crossing_event
  does_not_cover:
    - simple_price_moving_average_cross
---

# Pattern: MACD Crossover

## Intent
Find securities where MACD crosses above or below its signal line.

## Natural Language Triggers
- MACD crossover
- MACD crosses above signal line
- bullish MACD cross
- MACD crosses below signal line

## Required Logical Components
- calculate or reference the MACD series
- calculate or reference the signal line
- detect the crossing event using Cross

## Formula Building Blocks
```metastock
MACD()
Mov(MACD(),9,E)
Cross(MACD(), Mov(MACD(),9,E))
```

## Example Compositions
```metastock
Cross(MACD(), Mov(MACD(),9,E))
```

## Default Assumptions
- bullish cross means MACD crosses above the signal line
- bearish cross means signal line crosses above MACD

## Pitfalls
Do not use `MACD > signal line` when the user asks for a crossing event. Do not use `Cross` alone without the MACD series.

## Test Queries
- Find stocks where MACD crosses above its signal line
```

---

## 9. OpenAI card-generation prompt requirements

When asking OpenAI to generate cards, the prompt must require the registry-ready frontmatter.

Use this instruction block:

```text
Generate MetaStock RAG knowledge cards as Markdown files.

Every card must include YAML frontmatter with:
- canonical_id
- title
- type
- card_bucket
- category
- source
- status
- priority
- supports_explorer
- aliases as objects with text/type/weight
- requires/suggests/conflicts_with/forbids as canonical-ID dependency objects when applicable
- semantic block describing mechanism, market_object, operations_supported, required_components, and does_not_cover

Allowed alias_type values only:
- exact
- synonym
- phrase
- abbreviation
- weak_hint

Do not use alias_type values such as title, primary, keyword, trigger, or related_term.

Dependencies must use canonical IDs like function.mov, function.ref, pattern.breakout.
Do not use display titles such as Mov, Ref, or Pattern: Breakout in dependencies.

Pattern cards must explicitly include requires dependencies for functions that are usually necessary for correct formula generation.
Function cards should use suggests, not requires, for optional helper functions.

Each card body must include the required sections for its type and at least one dry-run Test Query.
```

---

## 10. Upload workflow

### 10.1 Dry run

```powershell
python scripts/sync_cards_to_supabase.py --knowledge-dir knowledge_base --dry-run
```

The preview must include:

```text
rag_cards row
rag_card_embeddings row
rag_card_registry row
rag_card_aliases rows
rag_card_dependencies rows
```

### 10.2 Apply

```powershell
python scripts/sync_cards_to_supabase.py --knowledge-dir knowledge_base
```

This should sync:

```text
rag_cards
rag_card_embeddings
rag_card_registry
rag_card_aliases
rag_card_dependencies
```

### 10.3 Useful command variants

Skip embeddings:

```powershell
python scripts/sync_cards_to_supabase.py --knowledge-dir knowledge_base --no-embed
```

Force embedding regeneration:

```powershell
python scripts/sync_cards_to_supabase.py --knowledge-dir knowledge_base --force-embed
```

Only update registry metadata:

```powershell
python scripts/sync_cards_to_supabase.py --knowledge-dir knowledge_base --registry-only
```

Skip registry metadata:

```powershell
python scripts/sync_cards_to_supabase.py --knowledge-dir knowledge_base --no-registry
```


### 10.4 Standalone registry graph sync commands

Use this standalone script when card content and embeddings have already been synced into `rag_cards` / `rag_card_embeddings`, and you only need to sync the planning graph metadata:

```text
rag_card_registry
rag_card_aliases
rag_card_dependencies
```

Script path:

```text
scripts/sync_registry_graph_from_cards.py
```

This script assumes the cards already follow the registry-ready frontmatter format described in this document. It should not infer aliases or dependencies from titles alone.

#### 10.4.1 One-time Supabase indexes

Run once in Supabase SQL Editor so alias and dependency upserts are idempotent:

```sql
create unique index if not exists uq_rag_card_aliases_canonical_alias
on public.rag_card_aliases (
    canonical_id,
    alias_text
);

create unique index if not exists uq_rag_card_dependencies_from_to_type
on public.rag_card_dependencies (
    from_canonical_id,
    to_canonical_id,
    edge_type
);
```

#### 10.4.2 Dry run registry graph sync

Dry run is the default when `--apply` is not provided:

```powershell
python .\scripts\sync_registry_graph_from_cards.py --knowledge-dir .\knowledge_base
```

Verbose dry run:

```powershell
python .\scripts\sync_registry_graph_from_cards.py --knowledge-dir .\knowledge_base --verbose
```

#### 10.4.3 Apply registry graph sync

```powershell
python .\scripts\sync_registry_graph_from_cards.py --knowledge-dir .\knowledge_base --apply
```

#### 10.4.4 Require matching `rag_cards` rows

Use this when every registry node must point to an already-uploaded card row:

```powershell
python .\scripts\sync_registry_graph_from_cards.py --knowledge-dir .\knowledge_base --apply --require-rag-cards
```

#### 10.4.5 Fail on missing dependency targets

Use this when dependency targets must already exist in `rag_card_registry`:

```powershell
python .\scripts\sync_registry_graph_from_cards.py --knowledge-dir .\knowledge_base --apply --fail-missing-dependency-targets
```

### 10.5 Recommended sync order

Use the combined sync script when it already supports the full workflow. Use the standalone registry graph script when you intentionally separate card/embedding sync from registry graph sync.

Recommended order:

```text
1. Generate registry-ready knowledge cards.
2. Sync card content and embeddings into rag_cards / rag_card_embeddings.
3. Run sync_registry_graph_from_cards.py dry run.
4. Review registry rows, alias rows, and dependency rows.
5. Run sync_registry_graph_from_cards.py --apply.
6. Run duplicate and consistency checks.
7. Run query decomposition dry-run tests.
```

### 10.6 Duplicate and consistency checks

#### 10.6.1 Check duplicate source paths in registry

```sql
select
    source_path,
    count(*) as registry_count,
    array_agg(canonical_id order by canonical_id) as canonical_ids
from public.rag_card_registry
group by source_path
having count(*) > 1
order by registry_count desc, source_path;
```

#### 10.6.2 Check aliases shared by multiple canonical IDs

```sql
select
    lower(alias_text) as normalized_alias,
    count(distinct canonical_id) as concept_count,
    array_agg(distinct canonical_id order by canonical_id) as canonical_ids
from public.rag_card_aliases
where is_active = true
group by lower(alias_text)
having count(distinct canonical_id) > 1
order by concept_count desc, normalized_alias;
```

Shared aliases are not always wrong. Review broad collisions such as `cross`, `trend`, `high`, `low`, `average`, `signal`, or `band` because they can force-retrieve unrelated cards.

#### 10.6.3 Check missing dependency targets

```sql
select
    d.from_canonical_id,
    d.edge_type,
    d.to_canonical_id,
    d.priority,
    d.rationale
from public.rag_card_dependencies d
left join public.rag_card_registry r
    on r.canonical_id = d.to_canonical_id
where r.canonical_id is null
order by d.from_canonical_id, d.edge_type, d.to_canonical_id;
```

#### 10.6.4 Check registry rows that do not resolve to cards

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
where card_id is null
order by canonical_id;
```

#### 10.6.5 Check alias types against the current database constraint

```sql
select
    conname,
    pg_get_constraintdef(oid) as constraint_definition
from pg_constraint
where conrelid = 'public.rag_card_aliases'::regclass
  and conname = 'rag_card_aliases_alias_type_check';
```

Expected allowed values:

```text
exact
synonym
phrase
abbreviation
weak_hint
```

---

## 11. Supabase validation queries

### 11.1 Registry row resolves to a card

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
where canonical_id = 'pattern.macd_crossover';
```

### 11.2 Alias rows use only allowed alias types

```sql
select distinct alias_type
from public.rag_card_aliases
order by alias_type;
```

Expected allowed values only:

```text
exact
synonym
phrase
abbreviation
weak_hint
```

### 11.3 Alias matching works

```sql
select *
from public.match_rag_card_aliases(
    'Find stocks where MACD crosses above its signal line',
    0.5
);
```

Expected result includes:

```text
pattern.macd_crossover
function.macd
function.cross
```

### 11.4 Dependency expansion works

```sql
select *
from public.expand_rag_card_dependencies(
    array['pattern.macd_crossover'],
    array['requires', 'suggests'],
    5
);
```

Expected result includes:

```text
pattern.macd_crossover
function.macd
function.cross
function.mov
```

---

## 12. Retrieval dry-run validation

Run representative queries after upload:

```powershell
python -m src.generate_explorer "Find stocks where MACD crosses above its signal line" --dry-run
python -m src.generate_explorer "Find stocks with a Bollinger Band squeeze breakout" --dry-run
python -m src.generate_explorer "Find stocks where close is above a 2 ATR trailing stop" --dry-run
```

Expected behavior after the relevant cards exist:

```text
[ ] The planner should stop suggesting cards that now exist.
[ ] The planner should resolve the new canonical IDs.
[ ] Dependencies should force-include required function cards.
[ ] Retrieval queries should not use missing-concept raw text when a card is still missing.
```

---

## 13. Checklist before committing new cards

```text
[ ] Card is in the correct knowledge_base folder.
[ ] Frontmatter includes canonical_id/title/type/card_bucket/category/source/status/priority/supports_explorer.
[ ] Aliases are object-style with text/type/weight.
[ ] Alias types use only exact/synonym/phrase/abbreviation/weak_hint.
[ ] Aliases are specific and not overly broad.
[ ] Dependencies use canonical IDs, not display titles.
[ ] requires/suggests choices are justified with rationale when possible.
[ ] semantic block states what the card covers and does not cover.
[ ] Formula examples are valid MetaStock syntax.
[ ] Pitfalls include common invalid formulas or wrong assumptions.
[ ] At least one Test Query is listed.
[ ] Dry run prints expected registry rows, alias rows, and dependency rows.
[ ] Supabase registry validation returns OK.
[ ] Dependency expansion returns expected cards.
[ ] Retrieval dry-run retrieves expected cards and stops suggesting cards that now exist.
```

---

## 14. Summary of what card generation must now produce

Each generated card must include enough information to fill these tables:

### `rag_card_registry`

```text
canonical_id
title
concept_type
card_bucket
source_path
is_active
```

### `rag_card_aliases`

```text
canonical_id
alias_text
alias_type
weight
is_active
```

Allowed `alias_type` values:

```text
exact
synonym
phrase
abbreviation
weak_hint
```

### `rag_card_dependencies`

```text
from_canonical_id
to_canonical_id
edge_type
priority
rationale
properties
is_active
```

This is why all future knowledge-card generation must include registry-ready frontmatter, not just natural-language titles and body text.
