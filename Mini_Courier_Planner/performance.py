"""Benchmark sorting algorithms and 0/1 Knapsack on increasing data sizes."""
import csv
import random
import statistics
import time
from pathlib import Path

from algorithms.sorting import insertion_sort_parcels, bubble_sort_parcels
from algorithms.knapsack import solve_knapsack
from algorithms.dijkstra import dijkstra
from algorithms.tsp import nearest_neighbor_tsp

BASE_DIR = Path(__file__).resolve().parent
RESULTS_DIR = BASE_DIR / "results"

def make_parcels(size, seed=42):
    rng = random.Random(seed + size)
    return [
        {
            "id": f"P{i:05}",
            "weight": rng.randint(1, 10),
            "priority": rng.randint(1, 5),
            "deadline": rng.randint(1, 100),
            "value": rng.randint(10, 100),
            "destination": "A"
        }
        for i in range(size)
    ]

def timed_call(function, *args, repeats=3):
    samples = []
    for _ in range(repeats):
        start = time.perf_counter()
        function(*args)
        samples.append(time.perf_counter() - start)
    return statistics.median(samples)

def make_graph(size, seed=7):
    """Create a connected undirected graph with non-negative weights."""
    rng = random.Random(seed + size)
    graph = {f"N{i}": {} for i in range(size)}
    # A chain guarantees connectivity.
    for i in range(size - 1):
        a, b = f"N{i}", f"N{i+1}"
        weight = rng.randint(1, 20)
        graph[a][b] = weight
        graph[b][a] = weight
    # Add a small number of extra edges for a less artificial network.
    extra_edges = min(size * 2, size * (size - 1) // 2)
    for _ in range(extra_edges):
        a_index, b_index = rng.sample(range(size), 2)
        a, b = f"N{a_index}", f"N{b_index}"
        weight = rng.randint(1, 20)
        graph[a][b] = weight
        graph[b][a] = weight
    return graph

def make_distance_matrix(size, seed=11):
    """Create a complete symmetric distance matrix for TSP benchmarking."""
    rng = random.Random(seed + size)
    nodes = [f"N{i}" for i in range(size)]
    matrix = {node: {node: 0} for node in nodes}
    for i in range(size):
        for j in range(i + 1, size):
            distance = rng.randint(1, 100)
            matrix[nodes[i]][nodes[j]] = distance
            matrix[nodes[j]][nodes[i]] = distance
    return matrix

def run_benchmarks():
    RESULTS_DIR.mkdir(exist_ok=True)
    rows = []
    print("\nPERFORMANCE ANALYSIS")
    print("Sorting benchmarks use the same generated input for both algorithms.")
    for size in (10, 100, 500, 1000):
        parcels = make_parcels(size)
        # Bubble sort is quadratic; cap the largest benchmark if the machine is slow.
        insertion_time = timed_call(insertion_sort_parcels, parcels, "priority", repeats=3)
        bubble_time = timed_call(bubble_sort_parcels, parcels, "priority", repeats=3)
        rows.append({"algorithm":"Insertion Sort", "input_size":size, "time_seconds":insertion_time})
        rows.append({"algorithm":"Bubble Sort", "input_size":size, "time_seconds":bubble_time})
        print(f"n={size:4} | Insertion={insertion_time:.6f}s | Bubble={bubble_time:.6f}s")

    for size in (10, 50, 100, 200):
        parcels = make_parcels(size, seed=100)
        capacity = 100
        knapsack_time = timed_call(solve_knapsack, parcels, capacity, repeats=3)
        rows.append({"algorithm":"0/1 Knapsack DP", "input_size":size, "time_seconds":knapsack_time})
        print(f"Knapsack n={size:4}, capacity={capacity} | {knapsack_time:.6f}s")

    # Graph algorithms are measured on increasing graph sizes.
    for size in (10, 50, 100, 200):
        graph = make_graph(size)
        dijkstra_time = timed_call(dijkstra, graph, "N0", repeats=3)
        rows.append({"algorithm":"Dijkstra", "input_size":size, "time_seconds":dijkstra_time})
        matrix = make_distance_matrix(size)
        tsp_time = timed_call(nearest_neighbor_tsp, matrix, "N0", repeats=3)
        rows.append({"algorithm":"Nearest Neighbor TSP", "input_size":size, "time_seconds":tsp_time})
        print(f"Graph size={size:4} | Dijkstra={dijkstra_time:.6f}s | TSP={tsp_time:.6f}s")

    csv_path = RESULTS_DIR / "performance_results.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["algorithm", "input_size", "time_seconds"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nSaved benchmark data to: {csv_path}")

    try:
        import matplotlib.pyplot as plt
        for algorithm in ("Insertion Sort", "Bubble Sort", "0/1 Knapsack DP", "Dijkstra", "Nearest Neighbor TSP"):
            subset = [r for r in rows if r["algorithm"] == algorithm]
            plt.plot(
                [r["input_size"] for r in subset],
                [r["time_seconds"] for r in subset],
                marker="o",
                label=algorithm
            )
        plt.xlabel("Input size (parcels or graph vertices)")
        plt.ylabel("Median execution time (seconds)")
        plt.title("Mini-Courier Planner: Runtime Comparison")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        chart_path = RESULTS_DIR / "runtime_comparison.png"
        plt.savefig(chart_path, dpi=160)
        plt.close()
        print(f"Saved runtime chart to: {chart_path}")
    except ImportError:
        print("Matplotlib is not installed. Install it with: python -m pip install matplotlib")

if __name__ == "__main__":
    run_benchmarks()
