"""Dijkstra shortest paths using an adjacency list and a min-heap."""
import heapq
import math

def validate_graph(graph):
    for node, neighbors in graph.items():
        for neighbor, weight in neighbors.items():
            if weight < 0:
                raise ValueError("Dijkstra requires non-negative edge weights.")
            if neighbor not in graph:
                raise ValueError(f"Neighbor {neighbor!r} is missing from graph.")
            if node not in graph[neighbor] or graph[neighbor][node] != weight:
                raise ValueError(f"Graph must be undirected with matching edge {node!r}-{neighbor!r}.")

def dijkstra(graph, start):
    """Return distance and predecessor dictionaries from start."""
    if start not in graph:
        raise ValueError(f"Start node {start!r} is not in the graph.")
    validate_graph(graph)

    distances = {node: math.inf for node in graph}
    previous = {node: None for node in graph}
    distances[start] = 0
    heap = [(0, start)]

    while heap:
        current_distance, current = heapq.heappop(heap)
        if current_distance != distances[current]:
            continue
        for neighbor, weight in graph[current].items():
            new_distance = current_distance + weight
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = current
                heapq.heappush(heap, (new_distance, neighbor))
    return distances, previous

def reconstruct_path(previous, start, destination):
    """Reconstruct a path; return [] if destination is unreachable."""
    path = []
    current = destination
    while current is not None:
        path.append(current)
        if current == start:
            break
        current = previous.get(current)
    if not path or path[-1] != start:
        return []
    return list(reversed(path))

def all_pairs_shortest_paths(graph, required_nodes):
    """Run Dijkstra from each required node and return distance/path matrices."""
    distance_matrix = {}
    path_matrix = {}
    for source in required_nodes:
        distances, previous = dijkstra(graph, source)
        distance_matrix[source] = {}
        path_matrix[source] = {}
        for destination in required_nodes:
            distance_matrix[source][destination] = distances[destination]
            path_matrix[source][destination] = reconstruct_path(previous, source, destination)
    return distance_matrix, path_matrix
