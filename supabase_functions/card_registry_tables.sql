-- ============================================================
-- RAG Knowledge Graph Registry
-- Supabase/Postgres version
--
-- Graph mapping:
--   rag_card_registry      = nodes
--   rag_card_aliases       = alias labels / matching hints
--   rag_card_dependencies  = edges
--   rag_cards              = source documents
--   rag_card_embeddings    = vector layer
--
-- Designed so it can later be projected/exported into:
--   Neo4j, Kuzu, Memgraph, FalkorDB, etc.
-- ============================================================


-- ------------------------------------------------------------
-- 1. Node table: canonical concepts
-- ------------------------------------------------------------

create table if not exists public.rag_card_registry (
    canonical_id text primary key,

    -- Stable graph label / node category.
    -- Examples:
    --   function
    --   pattern
    --   field
    --   explorer_rule
    --   reference
    --   example
    --   pitfall
    concept_type text not null,

    -- Optional graph labels for future graph DB export.
    -- Example: ["Concept", "Function", "ExplorerSupported"]
    graph_labels text[] not null default array[]::text[],

    -- Link to existing rag_cards by source_path.
    -- We deliberately avoid a hard FK here because existing rag_cards.source_path
    -- may not have a unique constraint yet.
    source_path text not null,

    title text not null,

    -- Should usually match rag_cards.card_bucket.
    -- Examples: functions, patterns, references, templates, examples, pitfalls
    card_bucket text not null,

    -- Whether this concept can be used in Explorer generation.
    supports_explorer boolean not null default true,

    -- Lower number = higher priority when forced into context.
    priority int not null default 100,

    -- Stable external graph id placeholder for future migration.
    -- Example: Neo4j node id, Kuzu internal id, etc.
    external_graph_id text,

    -- Free-form graph/node properties.
    -- Keep anything non-relational here.
    -- Example:
    -- {
    --   "syntax": "Mov(DATA ARRAY, PERIODS, METHOD)",
    --   "default_period": 20,
    --   "formula_role": "volume_confirmation"
    -- }
    properties jsonb not null default '{}'::jsonb,

    is_active boolean not null default true,

    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),

    constraint rag_card_registry_concept_type_check
        check (
            concept_type in (
                'function',
                'pattern',
                'field',
                'explorer_rule',
                'reference',
                'example',
                'pitfall'
            )
        )
);


-- ------------------------------------------------------------
-- 2. Alias table: natural-language labels / matching hints
-- ------------------------------------------------------------

create table if not exists public.rag_card_aliases (
    alias_id bigserial primary key,

    canonical_id text not null
        references public.rag_card_registry(canonical_id)
        on delete cascade,

    -- Natural language phrase.
    -- Examples:
    --   moving average
    --   volume spike
    --   new 20 day low
    alias_text text not null,

    -- Normalized lowercase alias for matching and uniqueness.
    alias_text_norm text generated always as (lower(trim(alias_text))) stored,

    -- Alias type:
    --   exact          = very strong direct synonym
    --   synonym        = common equivalent
    --   phrase         = longer phrase users may type
    --   abbreviation   = RSI, MA, SMA, EMA, etc.
    --   weak_hint      = useful but ambiguous
    alias_type text not null default 'phrase',

    -- Matching weight.
    -- 1.0 = strong match
    -- lower = weaker / more ambiguous
    weight numeric not null default 1.0,

    -- For later multilingual support.
    language_code text not null default 'en',

    -- Useful later if aliases come from cards, user logs, LLM generation, etc.
    source text not null default 'manual',

    properties jsonb not null default '{}'::jsonb,

    is_active boolean not null default true,

    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),

    constraint rag_card_aliases_alias_type_check
        check (
            alias_type in (
                'exact',
                'synonym',
                'phrase',
                'abbreviation',
                'weak_hint'
            )
        ),

    constraint rag_card_aliases_weight_check
        check (weight > 0),

    constraint rag_card_aliases_unique
        unique (canonical_id, alias_text_norm, language_code)
);


-- ------------------------------------------------------------
-- 3. Edge table: concept dependencies / relationships
-- ------------------------------------------------------------

create table if not exists public.rag_card_dependencies (
    dependency_id bigserial primary key,

    -- Source node.
    -- Example: pattern.breakout
    from_canonical_id text not null
        references public.rag_card_registry(canonical_id)
        on delete cascade,

    -- Target node.
    -- Example: function.hhv
    to_canonical_id text not null
        references public.rag_card_registry(canonical_id)
        on delete cascade,

    -- Graph edge type.
    -- Keep these uppercase-ish logically, but lowercase in DB for ease.
    -- Examples:
    --   requires
    --   suggests
    --   conflicts_with
    --   forbids
    --   similar_to
    --   expands_to
    edge_type text not null default 'requires',

    -- Lower number = more important edge when expanding context.
    priority int not null default 100,

    -- Future graph DB relationship id placeholder.
    external_graph_edge_id text,

    -- Why this edge exists.
    -- Example:
    --   "Volume above average requires Mov(V,period,S)"
    rationale text,

    -- Free-form relationship properties.
    -- Example:
    -- {
    --   "formula_role": "dependency",
    --   "default_usage": "Mov(V,20,S)"
    -- }
    properties jsonb not null default '{}'::jsonb,

    is_active boolean not null default true,

    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),

    constraint rag_card_dependencies_edge_type_check
        check (
            edge_type in (
                'requires',
                'suggests',
                'conflicts_with',
                'forbids',
                'similar_to',
                'expands_to'
            )
        ),

    constraint rag_card_dependencies_no_self_edge
        check (from_canonical_id <> to_canonical_id),

    constraint rag_card_dependencies_unique
        unique (from_canonical_id, to_canonical_id, edge_type)
);


-- ------------------------------------------------------------
-- 4. Updated-at trigger helper
-- ------------------------------------------------------------

create or replace function public.set_updated_at()
returns trigger
language plpgsql
as $$
begin
    new.updated_at = now();
    return new;
end;
$$;


drop trigger if exists trg_rag_card_registry_updated_at
on public.rag_card_registry;

create trigger trg_rag_card_registry_updated_at
before update on public.rag_card_registry
for each row
execute function public.set_updated_at();


drop trigger if exists trg_rag_card_aliases_updated_at
on public.rag_card_aliases;

create trigger trg_rag_card_aliases_updated_at
before update on public.rag_card_aliases
for each row
execute function public.set_updated_at();


drop trigger if exists trg_rag_card_dependencies_updated_at
on public.rag_card_dependencies;

create trigger trg_rag_card_dependencies_updated_at
before update on public.rag_card_dependencies
for each row
execute function public.set_updated_at();


-- ------------------------------------------------------------
-- 5. Indexes
-- ------------------------------------------------------------

create index if not exists idx_rag_card_registry_source_path
    on public.rag_card_registry(source_path);

create index if not exists idx_rag_card_registry_concept_type
    on public.rag_card_registry(concept_type);

create index if not exists idx_rag_card_registry_card_bucket
    on public.rag_card_registry(card_bucket);

create index if not exists idx_rag_card_registry_active
    on public.rag_card_registry(is_active);

create index if not exists idx_rag_card_registry_graph_labels_gin
    on public.rag_card_registry using gin (graph_labels);

create index if not exists idx_rag_card_registry_properties_gin
    on public.rag_card_registry using gin (properties);


create index if not exists idx_rag_card_aliases_canonical_id
    on public.rag_card_aliases(canonical_id);

create index if not exists idx_rag_card_aliases_alias_text_norm
    on public.rag_card_aliases(alias_text_norm);

create index if not exists idx_rag_card_aliases_active
    on public.rag_card_aliases(is_active);

create index if not exists idx_rag_card_aliases_properties_gin
    on public.rag_card_aliases using gin (properties);


create index if not exists idx_rag_card_dependencies_from
    on public.rag_card_dependencies(from_canonical_id);

create index if not exists idx_rag_card_dependencies_to
    on public.rag_card_dependencies(to_canonical_id);

create index if not exists idx_rag_card_dependencies_edge_type
    on public.rag_card_dependencies(edge_type);

create index if not exists idx_rag_card_dependencies_active
    on public.rag_card_dependencies(is_active);

create index if not exists idx_rag_card_dependencies_properties_gin
    on public.rag_card_dependencies using gin (properties);