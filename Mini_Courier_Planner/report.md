# Mini-Courier Planner – Project Report

**Course:** Design & Analysis of Algorithms (ETCCDA302)  
**Project:** Mini-Courier Planner  
**Student:** [Enter your name]  
**Roll Number:** [Enter your roll number]  
**Programme:** B.Tech CSE / Specialization  
**University:** K.R. Mangalam University  

## 1. Introduction
The Mini-Courier Planner is a Python prototype that demonstrates how algorithmic techniques can support parcel selection and delivery-route planning.

## 2. Problem Statement
Given a set of parcels, a vehicle capacity, delivery destinations and a weighted road network, prioritize parcels, select a high-value feasible parcel set, calculate shortest paths and generate an approximate route visiting the selected destinations.

## 3. Objectives
- Prioritize parcels by priority or deadline.
- Select parcels without exceeding vehicle capacity.
- Calculate shortest paths in a weighted graph.
- Generate an approximate delivery tour.
- Measure algorithm execution time on increasing input sizes.

## 4. System Design
Describe the input JSON files, terminal menu, algorithm modules and final outputs. Insert your own architecture diagram.

## 5. Dataset Description
Explain the fields in `data/parcels.json` and the adjacency-list representation in `data/locations.json`. State that the supplied records are illustrative sample data.

## 6. Algorithm Selection and Complexity
| Algorithm | Purpose | Time complexity |
|---|---|---|
| Insertion Sort | Parcel priority/deadline ordering | O(n^2) worst, O(n) best |
| Bubble Sort | Parcel priority/deadline ordering | O(n^2) worst, O(n) best with early stop |
| 0/1 Knapsack DP | Parcel selection | O(nW) |
| Dijkstra with heap | One-source shortest paths | O((V+E) log V) |
| Nearest Neighbor | Approximate delivery tour | O(k^2) with distance matrix |

## 7. Implementation
Describe each module: `sorting.py`, `knapsack.py`, `dijkstra.py`, `tsp.py`, `main.py`, and `performance.py`. Include selected code snippets and screenshots.

## 8. Sample Input and Output
Paste output captured from your own run of `py main.py`, including sorting, Knapsack, Dijkstra and the complete courier plan.

## 9. Performance Analysis
Run `py performance.py`. Insert the generated `results/performance_results.csv` values and `results/runtime_comparison.png`. Discuss how the measured runtime changes with input size. Measurements depend on the computer and Python environment.

## 10. Testing
Run `py -m unittest tests -v`. Record actual test results and explain any failed test and its correction.

## 11. Results and Discussion
Discuss selected parcel value and weight, shortest paths, route sequence, total route distance and measured runtime.

## 12. Limitations
- Nearest Neighbor is a heuristic and does not guarantee an optimal TSP tour.
- The sample graph is a simplified undirected network.
- The prototype does not model live traffic, vehicle fleets or time-window constraints.
- The current Knapsack implementation uses integer weights.

## 13. Future Enhancements
- Add multiple vehicles and delivery trips.
- Add real map data and traffic-aware weights.
- Add delivery time windows.
- Compare Nearest Neighbor with other route heuristics.
- Add a graphical interface or database.

## 14. Conclusion
Summarize how sorting, dynamic programming, graph algorithms and approximation techniques were integrated into one courier-planning prototype.

## 15. References
- Course notes and lab material for Design & Analysis of Algorithms.
- Python documentation: https://docs.python.org/3/
- Matplotlib documentation: https://matplotlib.org/stable/
