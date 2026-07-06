-- ============================================================
-- Function: expand_rag_card_dependencies
--
-- Given seed canonical IDs, recursively expand required concepts.
--
-- Example:
--   select * from public.expand_rag_card_dependencies(
--       array['pattern.breakout', 'pattern.volume_above_average'],
--       array['requires']
--   );
-- ============================================================

create or replace function public.expand_rag_card_dependencies(
    seed_canonical_ids text[],
    allowed_edge_types text[] default array['requires']::text[],
    max_depth int default 5
)
returns table (
    canonical_id text,
    source_path text,
    title text,
    concept_type text,
    card_bucket text,
    depth int,
    dependency_path text[]
)
language sql
stable
as $$
    with recursive expanded as (
        -- Seed nodes
        select
            r.canonical_id,
            r.source_path,
            r.title,
            r.concept_type,
            r.card_bucket,
            0 as depth,
            array[r.canonical_id] as dependency_path
        from public.rag_card_registry r
        where r.canonical_id = any(seed_canonical_ids)
          and r.is_active = true

        union all

        -- Follow active dependency edges
        select
            child.canonical_id,
            child.source_path,
            child.title,
            child.concept_type,
            child.card_bucket,
            parent.depth + 1 as depth,
            parent.dependency_path || child.canonical_id as dependency_path
        from expanded parent
        join public.rag_card_dependencies edge
            on edge.from_canonical_id = parent.canonical_id
           and edge.is_active = true
           and edge.edge_type = any(allowed_edge_types)
        join public.rag_card_registry child
            on child.canonical_id = edge.to_canonical_id
           and child.is_active = true
        where parent.depth < max_depth
          and not child.canonical_id = any(parent.dependency_path)
    )
    select distinct on (canonical_id)
        canonical_id,
        source_path,
        title,
        concept_type,
        card_bucket,
        depth,
        dependency_path
    from expanded
    order by canonical_id, depth;
$$;