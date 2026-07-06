-- ============================================================
-- View: resolved registry cards
-- Joins graph node table to actual rag_cards source documents.
-- ============================================================

create or replace view public.v_rag_card_registry_resolved as
select
    r.canonical_id,
    r.concept_type,
    r.graph_labels,
    r.source_path,
    r.title as registry_title,
    r.card_bucket as registry_bucket,
    r.supports_explorer,
    r.priority,
    r.external_graph_id,
    r.properties,
    r.is_active,

    c.card_id::text as card_id,
    c.title as card_title,
    c.card_type,
    c.card_bucket,
    c.category,
    c.body_markdown,
    c.content_hash

from public.rag_card_registry r
left join public.rag_cards c
    on c.source_path = r.source_path;