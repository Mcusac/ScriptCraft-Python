"""Auto-generated package exports."""


from .import_graph import (
    ImportGraphBuildResult,
    TreeEdge,
    bounded_bfs_tree_edges,
    build_internal_import_graph,
    direct_inbound,
    direct_outbound,
    iter_tree_lines,
    resolve_target_module,
    transitive_closure,
)

from .reachability import (
    compute_incoming_counts,
    induced_subgraph,
    orphan_cascade_waves,
    reachable_from_entrypoints,
)

from .scc import (
    find_cycles,
    find_strongly_connected_components,
)

__all__ = [
    "ImportGraphBuildResult",
    "TreeEdge",
    "bounded_bfs_tree_edges",
    "build_internal_import_graph",
    "compute_incoming_counts",
    "direct_inbound",
    "direct_outbound",
    "find_cycles",
    "find_strongly_connected_components",
    "induced_subgraph",
    "iter_tree_lines",
    "orphan_cascade_waves",
    "reachable_from_entrypoints",
    "resolve_target_module",
    "transitive_closure",
]
