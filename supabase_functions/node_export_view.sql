-- ============================================================
-- Graph DB export: nodes
-- Each row can become a node in Neo4j/Kuzu/Memgraph/FalkorDB.
-- ============================================================

create or replace view public.v_rag_graph_nodes as
select
    canonical_id as node_id,
    concept_type,
    graph_labels,
    title,
    source_path,
    card_bucket,
    supports_explorer,
    priority,
    properties,
    is_active
from public.rag_card_registry
where is_active = true;