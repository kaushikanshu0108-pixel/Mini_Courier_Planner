"""Mini-Courier Planner: integrated terminal application."""
import json
from pathlib import Path

from algorithms.sorting import insertion_sort_parcels, bubble_sort_parcels
from algorithms.knapsack import solve_knapsack
from algorithms.dijkstra import dijkstra, all_pairs_shortest_paths
from algorithms.tsp import nearest_neighbor_tsp

BASE_DIR = Path(__file__).resolve().parent
PARCEL_FILE = BASE_DIR / "data" / "parcels.json"
LOCATION_FILE = BASE_DIR / "data" / "locations.json"

def load_data():
    with PARCEL_FILE.open(encoding="utf-8") as f:
        parcel_data = json.load(f)
    with LOCATION_FILE.open(encoding="utf-8") as f:
        location_data = json.load(f)
    return parcel_data, location_data

def print_parcels(parcels):
    if not parcels:
        print("No parcels found.")
        return
    print(f"{'ID':<8}{'Weight':>9}{'Priority':>10}{'Deadline':>11}{'Value':>9}{'Destination':>14}")
    print("-" * 61)
    for p in parcels:
        print(f"{p['id']:<8}{p['weight']:>9}{p['priority']:>10}{p['deadline']:>11}{p['value']:>9}{p['destination']:>14}")

def choose_sort(parcels):
    print("\n1. Insertion Sort\n2. Bubble Sort")
    algorithm = input("Choose sorting algorithm: ").strip()
    print("1. Highest priority first\n2. Earliest deadline first")
    criterion = input("Choose sorting criterion: ").strip()
    sort_by = "priority" if criterion == "1" else "deadline" if criterion == "2" else None
    if sort_by is None:
        print("Invalid criterion.")
        return
    if algorithm == "1":
        result = insertion_sort_parcels(parcels, sort_by)
        name = "Insertion Sort"
    elif algorithm == "2":
        result = bubble_sort_parcels(parcels, sort_by)
        name = "Bubble Sort"
    else:
        print("Invalid sorting choice.")
        return
    print(f"\n{name} result ({sort_by}):")
    print_parcels(result)

def display_graph(graph):
    print("\nDELIVERY NETWORK (undirected weighted graph)")
    for node, neighbors in graph.items():
        edges = ", ".join(f"{neighbor} ({weight} km)" for neighbor, weight in neighbors.items())
        print(f"{node}: {edges}")

def run_shortest_paths(graph, depot):
    distances, previous = dijkstra(graph, depot)
    print(f"\nSHORTEST PATHS FROM {depot}")
    for destination in graph:
        if distances[destination] == float("inf"):
            print(f"{destination}: unreachable")
            continue
        path = []
        current = destination
        while current is not None:
            path.append(current)
            current = previous[current]
        path.reverse()
        print(f"{destination}: {' -> '.join(path)} = {distances[destination]} km")

def build_courier_plan(parcels, capacity, graph, depot):
    selected, total_weight, total_value, dp = solve_knapsack(parcels, capacity)
    print("\n========== OPTIMAL PACKING PLAN ==========")
    print_parcels(selected)
    print(f"\nVehicle capacity : {capacity} kg")
    print(f"Selected weight  : {total_weight} kg")
    print(f"Remaining capacity: {capacity - total_weight} kg")
    print(f"Total parcel value: {total_value}")

    destinations = sorted({p["destination"] for p in selected})
    missing = [d for d in destinations if d not in graph]
    if missing:
        print(f"Cannot route: destination(s) missing from graph: {missing}")
        return
    required_nodes = [depot] + [d for d in destinations if d != depot]
    if len(required_nodes) == 1:
        print("\nNo delivery destinations were selected.")
        return

    distance_matrix, path_matrix = all_pairs_shortest_paths(graph, required_nodes)
    route, total_distance = nearest_neighbor_tsp(distance_matrix, depot)

    print("\n========== DELIVERY ROUTE ==========")
    for index in range(len(route) - 1):
        source, destination = route[index], route[index + 1]
        leg_path = path_matrix[source][destination]
        leg_distance = distance_matrix[source][destination]
        print(f"{source} -> {destination}: {' -> '.join(leg_path)} ({leg_distance} km)")
    print(f"\nRoute sequence: {' -> '.join(route)}")
    print(f"Total route distance: {total_distance} km")
    print("\nNote: Nearest Neighbor is an approximation and may not find the globally shortest tour.")

def show_menu():
    print("\n" + "=" * 48)
    print("             MINI-COURIER PLANNER")
    print("     Intelligent Delivery & Route Optimization")
    print("=" * 48)
    print("1. Display all parcels")
    print("2. Prioritize parcels (Insertion/Bubble Sort)")
    print("3. Optimize parcel selection (Knapsack DP)")
    print("4. Display delivery network")
    print("5. Find shortest paths (Dijkstra)")
    print("6. Generate delivery route (TSP)")
    print("7. Display complete courier plan")
    print("8. Run performance analysis")
    print("9. Exit")

def main():
    try:
        parcel_data, location_data = load_data()
        parcels = parcel_data["parcels"]
        capacity = parcel_data["vehicle_capacity"]
        graph = location_data["graph"]
        depot = location_data["depot"]
    except (OSError, json.JSONDecodeError, KeyError) as error:
        print(f"Could not load project data: {error}")
        return

    while True:
        show_menu()
        choice = input("Enter your choice (1-9): ").strip()
        try:
            if choice == "1":
                print_parcels(parcels)
            elif choice == "2":
                choose_sort(parcels)
            elif choice == "3":
                selected, weight, value, dp = solve_knapsack(parcels, capacity)
                print("\nOPTIMAL PARCEL SELECTION")
                print_parcels(selected)
                print(f"\nTotal weight: {weight}/{capacity} kg")
                print(f"Total value: {value}")
                print("\nDP table (rows = parcels considered; columns = capacity 0..W):")
                for row in dp:
                    print(" ".join(f"{cell:4}" for cell in row))
            elif choice == "4":
                display_graph(graph)
            elif choice == "5":
                run_shortest_paths(graph, depot)
            elif choice == "6":
                selected, _, _, _ = solve_knapsack(parcels, capacity)
                destinations = sorted({p["destination"] for p in selected})
                required = [depot] + [d for d in destinations if d != depot]
                if len(required) <= 1:
                    print("No delivery destinations selected.")
                else:
                    matrix, _ = all_pairs_shortest_paths(graph, required)
                    route, distance = nearest_neighbor_tsp(matrix, depot)
                    print(f"\nApproximate route: {' -> '.join(route)}")
                    print(f"Total distance: {distance} km")
            elif choice == "7":
                build_courier_plan(parcels, capacity, graph, depot)
            elif choice == "8":
                from performance import run_benchmarks
                run_benchmarks()
            elif choice == "9":
                print("Thank you for using Mini-Courier Planner.")
                break
            else:
                print("Invalid choice. Enter a number from 1 to 9.")
        except (ValueError, KeyError) as error:
            print(f"Operation could not be completed: {error}")

if __name__ == "__main__":
    main()
