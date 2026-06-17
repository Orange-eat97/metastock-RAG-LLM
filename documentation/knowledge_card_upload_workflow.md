# Knowledge Card Upload Workflow

This guide explains how to add a new MetaStock RAG knowledge card after the registry/dependency workflow upgrade.

A knowledge card now has two roles:

```text
1. RAG document: stored in rag_cards and embedded into rag_card_embeddings.
2. Planning graph node: registered in rag_card_registry, linked through aliases and dependency edges.
```

## 1. Create or edit a markdown card

Place the card under `knowledge_base/` using the correct bucket folder:

```text
knowledge_base/
  functions/
  patterns/
  references/
  templates/
  examples/
  pitfalls/
```

Example path:

```text
knowledge_base/patterns/new_low.md
```

## 2. Card quality requirements

Every card should be useful for both semantic retrieval and formula generation. A good card must make the following clear:

```text
[ ] What concept this card represents.
[ ] What user phrases should retrieve this card.
[ ] What MetaStock syntax or formula pattern is valid.
[ ] What dependencies must be retrieved with this card.
[ ] What assumptions are being made.
[ ] What mistakes the LLM must avoid.
[ ] What dry-run query should prove the card works.
```

### 2.1 Required sections for pattern cards

Pattern cards should include these sections:

```markdown
# Pattern: <Name>

## Intent
Describe the trading condition in plain English.

## Natural Language Triggers
- phrases users may type
- synonyms
- common variants

## Required Logical Components
- the exact logical parts needed for the pattern

## Formula Building Blocks
```metastock
MetaStock snippets needed to build the pattern
```

## Example Compositions
```metastock
A complete valid Explorer filter example
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

Pattern-card quality rule:

```text
A pattern card should describe a reusable trading idea, not just one formula.
```

Example: `Pattern: Volume Above Average` is good because it maps many user phrasings into one reusable idea.

### 2.2 Required sections for function cards

Function cards should include these sections:

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

Function-card quality rule:

```text
A function card should teach the LLM how to use the function correctly, not merely define it.
```

### 2.3 Required sections for reference/template cards

Reference/template cards should include:

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
```

Reference/template quality rule:

```text
Reference/template cards should be stable base context. They should not depend on one specific user query.
```

### 2.4 Alias quality requirements

Aliases should be specific enough to avoid false positives.

Good aliases:

```yaml
aliases:
  - volume above average
  - above average volume
  - volume spike
  - new 20 day low
  - crosses above
```

Bad aliases:

```yaml
aliases:
  - low
  - high
  - average
  - price
  - trend
```

Why: broad aliases cause unrelated cards to be force-retrieved.

Abbreviations such as `MA`, `RSI`, `HHV`, and `LLV` are allowed, but they should use `alias_type: abbreviation` through the sync script defaults or registry logic so token-boundary matching prevents false hits like `making` → `MA`.

### 2.5 Dependency quality requirements

Use dependency edges carefully:

```text
requires      = must be included for correct generation
suggests      = often useful, but not always necessary
forbids       = should not be used with this concept
conflicts_with = semantically conflicts with this concept
similar_to    = related concept, not required
expands_to    = example/template expands to another concept
```

Examples:

```yaml
requires:
  - function.llv
  - function.ref
```

for a `Pattern: New Low` card.

```yaml
suggests:
  - function.mov
```

for `function.cross`, because a crossover often uses moving averages, but `Cross` can compare other arrays too.

Dependency rule:

```text
Do not put a card in requires unless the formula is usually wrong without it.
```

## 3. Use registry-aware frontmatter

Use canonical IDs for registry dependencies. Canonical IDs should match existing `rag_cards.card_id` style, for example:

```text
function.mov
function.ref
pattern.breakout
pattern.volume_above_average
```

Example pattern card:

```md
---
type: pattern
category: lowest_low
source: manual
status: active
priority: 10

aliases:
  - new low
  - new 20 day low
  - making a new low
  - break below previous low

requires:
  - function.llv
  - function.ref

registry:
  enabled: true
  supports_explorer: true
  properties:
    formula_role: price_breakdown_or_new_low
    default_period: 20
---

# Pattern: New Low

## Intent
Find securities making a new low over a lookback period.

## Natural Language Triggers
- new low
- new 20 day low
- making a new low
- break below previous low

## Required Logical Components
- identify the lowest low over the lookback period
- compare the current close or low against the previous lookback low
- exclude the current bar when the user asks for previous low

## Formula Building Blocks
```metastock
Ref(LLV(L,20),-1)
```

## Example Compositions
```metastock
C < Ref(LLV(L,20),-1)
```

## Default Assumptions
- lookback period defaults to 20 if user does not specify one
- use `L` for lowest-low calculation
- use `Ref(...,-1)` to exclude the current bar for previous-low logic

## Pitfalls
Do not use `HHV` for new-low logic. Do not use `LLV(L,20)` directly when the user asks for the previous low, because that includes the current bar.

## Test Queries
- Find stocks making a new 20 day low
- Find stocks breaking below the previous 20 day low
```

## 4. Frontmatter fields that matter

Minimum useful fields:

```yaml
type: pattern | function | reference | template | example | pitfall
category: short_category_name
source: manual | primer | primer_ii | etc
status: active
priority: 10
aliases:
  - phrase users may type
requires:
  - canonical.id
suggests:
  - canonical.id
registry:
  enabled: true
  supports_explorer: true
  properties: {}
```

Dependency keys supported by the sync script:

```yaml
requires:
suggests:
forbids:
conflicts_with:
similar_to:
expands_to:
```

## 5. Run a dry run first

From the repo root:

```powershell
python scripts/sync_cards_to_supabase.py --knowledge-dir knowledge_base --dry-run
```

Check that the preview includes:

```text
rag_cards row
rag_card_embeddings row
rag_card_registry row
rag_card_aliases rows
rag_card_dependencies rows
```

## 6. Upload cards, embeddings, and registry metadata

```powershell
python scripts/sync_cards_to_supabase.py --knowledge-dir knowledge_base
```

This syncs:

```text
rag_cards
rag_card_embeddings
rag_card_registry
rag_card_aliases
rag_card_dependencies
```

## 7. Useful command variants

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

## 8. Validate in Supabase

Check that the registry node resolves to an actual card:

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
where canonical_id = 'pattern.new_low';
```

Check dependency expansion:

```sql
select *
from public.expand_rag_card_dependencies(
    array['pattern.new_low'],
    array['requires'],
    5
);
```

Expected:

```text
pattern.new_low
function.llv
function.ref
```

Check alias matching:

```sql
select *
from public.match_rag_card_aliases(
    'Find stocks making a new 20 day low',
    0.5
);
```

## 9. Run a retrieval dry run

```powershell
python -m src.generate_explorer "Find stocks making a new 20 day low" --dry-run
```

Positive result:

```text
Seed canonical IDs:
- pattern.new_low

Registry-resolved forced cards:
- Pattern: New Low
- LLV
- Ref
```

## 10. Checklist before committing a new card

```text
[ ] Card is in the correct knowledge_base folder.
[ ] Frontmatter has type/category/status/priority.
[ ] Card has the required sections for its card type.
[ ] Aliases are specific, not overly broad.
[ ] Dependencies use canonical IDs like function.llv, not display titles like LLV.
[ ] requires/suggests choices are justified.
[ ] Formula examples are valid MetaStock syntax.
[ ] Pitfalls include common invalid formulas or wrong assumptions.
[ ] At least one test query is listed in the card.
[ ] Dry run prints expected registry rows.
[ ] Supabase registry validation returns OK.
[ ] Dependency expansion returns expected cards.
[ ] Retrieval dry-run retrieves the expected cards.
```
