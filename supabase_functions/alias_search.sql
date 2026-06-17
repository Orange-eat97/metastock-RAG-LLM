-- ============================================================
-- Function: match_rag_card_aliases
--
-- Simple alias matcher for deterministic hints.
-- This is not replacing embeddings or the LLM planner.
-- It is useful for finding candidate canonical concepts.
-- ============================================================

create or replace function public.match_rag_card_aliases(
    query_text text,
    min_weight numeric default 0.5
)
returns table (
    canonical_id text,
    title text,
    concept_type text,
    card_bucket text,
    alias_text text,
    alias_type text,
    weight numeric,
    source_path text
)
language sql
stable
as $$
    select
        r.canonical_id,
        r.title,
        r.concept_type,
        r.card_bucket,
        a.alias_text,
        a.alias_type,
        a.weight,
        r.source_path
    from public.rag_card_aliases a
    join public.rag_card_registry r
        on r.canonical_id = a.canonical_id
    where a.is_active = true
      and r.is_active = true
      and a.weight >= min_weight
      and lower(query_text) like '%' || a.alias_text_norm || '%'
    order by
        a.weight desc,
        r.priority asc,
        r.canonical_id asc;
$$;