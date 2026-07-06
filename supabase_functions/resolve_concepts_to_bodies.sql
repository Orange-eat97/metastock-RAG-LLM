-- ============================================================
-- Function: resolve_rag_registry_cards
--
-- Expands dependencies, then returns actual resolved rag_cards.
-- This is useful for Python context_builder.
-- ============================================================

create or replace function public.resolve_rag_registry_cards(
    seed_canonical_ids text[],
    allowed_edge_types text[] default array['requires']::text[],
    max_depth int default 5
)
returns table (
    canonical_id text,
    source_path text,
    registry_title text,
    concept_type text,
    registry_bucket text,
    depth int,
    priority int,
    card_id text,
    card_title text,
    card_type text,
    card_bucket text,
    category text,
    body_markdown text,
    content_hash text
)
language sql
stable
as $$
    with expanded as (
        select *
        from public.expand_rag_card_dependencies(
            seed_canonical_ids,
            allowed_edge_types,
            max_depth
        )
    )
    select
        r.canonical_id,
        r.source_path,
        r.registry_title,
        r.concept_type,
        r.registry_bucket,
        e.depth,
        r.priority,
        r.card_id,
        r.card_title,
        r.card_type,
        r.card_bucket,
        r.category,
        r.body_markdown,
        r.content_hash
    from expanded e
    join public.v_rag_card_registry_resolved r
        on r.canonical_id = e.canonical_id
    where r.is_active = true
    order by
        e.depth asc,
        r.priority asc,
        r.canonical_id asc;
$$;