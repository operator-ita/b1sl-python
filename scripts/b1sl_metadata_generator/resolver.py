"""
sap_metadata_generator.resolver
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Handles dependency resolution and topological sorting.
"""
from __future__ import annotations

import sys
from collections import deque
from pathlib import Path
from typing import TYPE_CHECKING

# Add current directory to path if not present (for standalone script imports)
_current_dir = str(Path(__file__).resolve().parent)
if _current_dir not in sys.path:
    sys.path.insert(0, _current_dir)

if TYPE_CHECKING:
    try:
        from scripts.sap_metadata_generator.parser import ParsedMetadata
    except ImportError:
        from parser import ParsedMetadata


def build_dependency_graph(metadata: ParsedMetadata) -> dict[str, set[str]]:
    graph: dict[str, set[str]] = {}

    for name, entity in metadata.entities.items():
        deps: set[str] = set()
        for prop in entity.properties:
            clean_type = prop.edm_type.split(".")[-1]
            if clean_type in metadata.complex_types or clean_type in metadata.enums:
                deps.add(clean_type)
        for nav in entity.nav_properties:
            if nav.target_type in metadata.entities:
                deps.add(nav.target_type)
        graph[name] = deps

    for name, ct in metadata.complex_types.items():
        deps: set[str] = set()
        for prop in ct.properties:
            clean_type = prop.edm_type.split(".")[-1]
            if clean_type in metadata.complex_types or clean_type in metadata.enums:
                deps.add(clean_type)
        graph[name] = deps

    for name in metadata.enums:
        graph[name] = set()

    return graph


def detect_cycles(graph: dict[str, set[str]]) -> list[list[str]]:
    visited: set[str] = set()
    in_stack: set[str] = set()
    cycles: list[list[str]] = []

    def dfs(node: str, path: list[str]) -> None:
        visited.add(node)
        in_stack.add(node)

        for neighbor in graph.get(node, set()):
            if neighbor not in visited:
                dfs(neighbor, path + [neighbor])
            elif neighbor in in_stack:
                try:
                    idx = path.index(neighbor)
                    cycles.append(path[idx:] + [neighbor])
                except ValueError:
                    pass

        in_stack.discard(node)

    for node in graph:
        if node not in visited:
            dfs(node, [node])

    return cycles


def topological_sort(graph: dict[str, set[str]]) -> list[str]:
    in_degree = {node: 0 for node in graph}
    for node, deps in graph.items():
        for dep in deps:
            if dep in in_degree:
                in_degree[dep] += 1

    queue = deque([n for n, d in in_degree.items() if d == 0])
    sorted_nodes = []

    while queue:
        node = queue.popleft()
        sorted_nodes.append(node)
        for neighbor in graph.get(node, set()):
            if neighbor in in_degree:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

    # Remaining nodes are part of cycles
    cyclic_nodes = set(graph.keys()) - set(sorted_nodes)
    sorted_nodes.extend(cyclic_nodes)

    return sorted_nodes
