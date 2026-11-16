# Mini-Courier Planner

A Python terminal application for a courier-planning prototype. It combines:
- Insertion Sort and Bubble Sort for parcel prioritization
- 0/1 Knapsack Dynamic Programming for vehicle packing
- Dijkstra's algorithm for shortest paths
- Nearest Neighbor TSP approximation for delivery ordering
- Runtime benchmarking and unit tests

## Requirements
- Python 3.9 or newer
- Matplotlib (only required for runtime chart generation)

## Setup (Windows, VS Code)
1. Open this folder in VS Code.
2. Open Terminal > New Terminal.
3. Create a virtual environment:
   `py -m venv .venv`
4. Activate it in PowerShell:
   `.\.venv\Scripts\Activate.ps1`
   If activation is blocked, use Command Prompt terminal and run:
   `.venv\Scripts\activate.bat`
5. Install chart dependency:
   `py -m pip install -r requirements.txt`

## Run the application
`py main.py`

## Run tests
`py -m unittest tests -v`

## Run performance benchmarks
`py performance.py`

Or select option 8 from the main menu.

## Data files
- `data/parcels.json`: vehicle capacity and parcel records
- `data/locations.json`: undirected weighted graph and depot

All graph edge weights must be non-negative and listed in both directions with equal values. Parcel weights and vehicle capacity must be non-negative integers for the current Knapsack implementation.

## Important interpretation
The Knapsack algorithm selects parcels based on maximum total value subject to vehicle capacity. Sorting is a separate prioritization display and does not force the Knapsack selection.

The route planner runs Dijkstra from each required location to build shortest-path distances, then applies Nearest Neighbor to those distances. The TSP result is an approximation, not a guarantee of the globally optimal tour.

## Complexity
- Insertion Sort: O(n^2) worst case; O(n) best case
- Bubble Sort: O(n^2) worst case; O(n) best case with early stopping
- 0/1 Knapsack: O(nW) time and O(nW) space in this table-based implementation
- Dijkstra with binary heap: O((V+E) log V) per source
- All-pairs distances by repeated Dijkstra: O(V(V+E) log V)
- Nearest Neighbor over a distance matrix: O(k^2)

## Submission
Include the full source folder, generated CSV/chart, screenshots of actual execution, and completed report. Do not submit invented benchmark results; run the benchmark on the submission machine and include the generated outputs.
