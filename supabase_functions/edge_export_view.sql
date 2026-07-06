-- ============================================================
-- Graph DB export: edges
-- Each row can become a relationship in Neo4j/Kuzu/Memgraph/FalkorDB.
-- ============================================================

create or replace view public.v_rag_graph_edges as
select
    dependency_id::text as edge_id,
    from_canonical_id as from_node_id,
    to_canonical_id as to_node_id,
    edge_type,
    priority,
    rationale,
    properties,
    is_active
from public.rag_card_dependencies
where is_active = true;