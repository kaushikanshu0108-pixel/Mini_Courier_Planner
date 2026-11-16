"""Unit tests for the Mini-Courier Planner algorithms."""
import unittest

from algorithms.sorting import insertion_sort_parcels, bubble_sort_parcels
from algorithms.knapsack import solve_knapsack
from algorithms.dijkstra import dijkstra, reconstruct_path, all_pairs_shortest_paths
from algorithms.tsp import nearest_neighbor_tsp

SAMPLE_PARCELS = [
    {"id":"P1","weight":5,"priority":3,"deadline":10,"value":50,"destination":"A"},
    {"id":"P2","weight":4,"priority":5,"deadline":8,"value":60,"destination":"B"},
    {"id":"P3","weight":6,"priority":2,"deadline":12,"value":70,"destination":"C"}
]

SAMPLE_GRAPH = {
    "Depot":{"A":4,"B":6},
    "A":{"Depot":4,"B":2,"C":5},
    "B":{"Depot":6,"A":2,"C":3},
    "C":{"A":5,"B":3}
}

class SortingTests(unittest.TestCase):
    def test_insertion_priority(self):
        result = insertion_sort_parcels(SAMPLE_PARCELS, "priority")
        self.assertEqual([p["id"] for p in result], ["P2","P1","P3"])

    def test_bubble_deadline(self):
        result = bubble_sort_parcels(SAMPLE_PARCELS, "deadline")
        self.assertEqual([p["id"] for p in result], ["P2","P1","P3"])

    def test_empty_sort(self):
        self.assertEqual(insertion_sort_parcels([]), [])
        self.assertEqual(bubble_sort_parcels([]), [])

class KnapsackTests(unittest.TestCase):
    def test_capacity_not_exceeded(self):
        selected, weight, value, dp = solve_knapsack(SAMPLE_PARCELS, 10)
        self.assertLessEqual(weight, 10)
        self.assertEqual(value, 130)
        self.assertEqual({p["id"] for p in selected}, {"P2","P3"})

    def test_zero_capacity(self):
        selected, weight, value, dp = solve_knapsack(SAMPLE_PARCELS, 0)
        self.assertEqual((selected, weight, value), ([], 0, 0))

    def test_empty_items(self):
        self.assertEqual(solve_knapsack([], 5)[:3], ([], 0, 0))

class DijkstraTests(unittest.TestCase):
    def test_shortest_distance(self):
        distances, previous = dijkstra(SAMPLE_GRAPH, "Depot")
        self.assertEqual(distances["C"], 9)
        self.assertEqual(reconstruct_path(previous, "Depot", "C"), ["Depot","A","C"])

    def test_unreachable_node(self):
        graph = {"S":{"A":2}, "A":{"S":2}, "X":{}}
        distances, _ = dijkstra(graph, "S")
        self.assertEqual(distances["X"], float("inf"))

    def test_negative_edge_rejected(self):
        with self.assertRaises(ValueError):
            dijkstra({"S":{"A":-1}, "A":{"S":-1}}, "S")

class TSPTests(unittest.TestCase):
    def test_route_visits_each_node_and_returns(self):
        matrix, _ = all_pairs_shortest_paths(SAMPLE_GRAPH, ["Depot","A","B","C"])
        route, distance = nearest_neighbor_tsp(matrix, "Depot")
        self.assertEqual(route[0], "Depot")
        self.assertEqual(route[-1], "Depot")
        self.assertEqual(set(route[:-1]), {"Depot","A","B","C"})
        self.assertGreater(distance, 0)

    def test_single_node(self):
        route, distance = nearest_neighbor_tsp({"Depot":{"Depot":0}}, "Depot")
        self.assertEqual(route, ["Depot"])
        self.assertEqual(distance, 0)

if __name__ == "__main__":
    unittest.main(verbosity=2)
