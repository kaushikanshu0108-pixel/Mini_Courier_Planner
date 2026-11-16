"""Nearest Neighbor approximation for a delivery tour."""
import math

def nearest_neighbor_tsp(distance_matrix, start):
    """
    Visit each destination exactly once, then return to start.
    Ties are broken alphabetically for reproducible output.
    Returns route and total distance.
    """
    if start not in distance_matrix:
        raise ValueError(f"Start location {start!r} is not in the distance matrix.")

    nodes = list(distance_matrix.keys())
    unvisited = set(nodes)
    unvisited.discard(start)
    route = [start]
    total_distance = 0
    current = start

    while unvisited:
        reachable = [
            (distance_matrix[current][candidate], candidate)
            for candidate in unvisited
            if not math.isinf(distance_matrix[current][candidate])
        ]
        if not reachable:
            raise ValueError("Some delivery locations are unreachable from the current route.")
        distance, next_node = min(reachable, key=lambda item: (item[0], item[1]))
        total_distance += distance
        route.append(next_node)
        unvisited.remove(next_node)
        current = next_node

    if len(nodes) > 1:
        return_distance = distance_matrix[current][start]
        if math.isinf(return_distance):
            raise ValueError("The route cannot return to the depot.")
        total_distance += return_distance
        route.append(start)

    return route, total_distance
