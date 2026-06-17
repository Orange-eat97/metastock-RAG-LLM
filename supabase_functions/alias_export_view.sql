-- ============================================================
-- Graph DB export: aliases
-- These can either become node properties or separate Alias nodes later.
-- ============================================================

create or replace view public.v_rag_graph_aliases as
select
    alias_id::text as alias_id,
    canonical_id as node_id,
    alias_text,
    alias_text_norm,
    alias_type,
    weight,
    language_code,
    source,
    properties,
    is_active
from public.rag_card_aliases
where is_active = true;