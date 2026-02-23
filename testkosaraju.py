"""Kosaraju's Algorithm for finding Strongly Connected Components (SCCs)

This module implements Kosaraju's algorithm to find all strongly connected components
in a directed graph. A strongly connected component is a maximal set of vertices where
every vertex is reachable from every other vertex.

Time Complexity: O(V + E) where V is vertices and E is edges
Space Complexity: O(V)
"""

from typing import List, Set, Dict


def kosaraju(graph: Dict[int, List[int]]) -> List[List[int]]:
    """
    Find all strongly connected components in a directed graph using Kosaraju's algorithm.
    
    Args:
        graph: Dictionary where key is vertex and value is list of adjacent vertices
        
    Returns:
        List of lists, where each inner list contains vertices of one SCC
    """
    if not graph:
        return []
    
    # Step 1: Get all vertices and fill stack with vertices in order of their finish time
    visited = set()
    stack = []
    
    def dfs_fill(vertex: int) -> None:
        """DFS to fill stack with vertices in decreasing order of finish time."""
        visited.add(vertex)
        for neighbor in graph.get(vertex, []):
            if neighbor not in visited:
                dfs_fill(neighbor)
        stack.append(vertex)
    
    # Fill stack with all vertices
    for vertex in graph:
        if vertex not in visited:
            dfs_fill(vertex)
    
    # Step 2: Create transpose of the graph
    transpose = {vertex: [] for vertex in graph}
    for vertex in graph:
        for neighbor in graph.get(vertex, []):
            transpose[neighbor].append(vertex)
    
    # Step 3: Do DFS on transpose graph in order of decreasing finish time
    visited.clear()
    sccs = []
    
    def dfs_collect(vertex: int, component: List[int]) -> None:
        """DFS to collect vertices in a strongly connected component."""
        visited.add(vertex)
        component.append(vertex)
        for neighbor in transpose.get(vertex, []):
            if neighbor not in visited:
                dfs_collect(neighbor, component)
    
    # Process vertices in order from stack (decreasing finish time)
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            component = []
            dfs_collect(vertex, component)
            sccs.append(sorted(component))
    
    return sccs


if __name__ == "__main__":
    # Example usage
    graph = {
        0: [1],
        1: [2],
        2: [0, 3],
        3: [1, 4],
        4: [3, 5],
        5: [2, 6],
        6: [5],
        7: [6, 7]
    }
    
    print("Graph:")
    for vertex, neighbors in sorted(graph.items()):
        print(f"  {vertex} -> {neighbors}")
    
    sccs = kosaraju(graph)
    print(f"\nStrongly Connected Components: {sccs}")
    print(f"Number of SCCs: {len(sccs)}")
