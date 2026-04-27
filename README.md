# LogiOpt — Logistics Network Optimization System

A full-stack academic project implementing core DSA concepts applied to logistics:
Sorting Engines, Graph Routing, Greedy Assignment, Dynamic Programming, and a
complete Pipeline with performance benchmarking.

---

## Project Structure

```
logistics/
├── backend/
│   ├── app.py                      ← Flask entry point
│   ├── models/
│   │   ├── delivery.py             ← DeliveryRequest model
│   │   ├── vehicle.py              ← Vehicle model
│   │   └── graph.py                ← Graph (adjacency list, random generation)
│   ├── services/
│   │   ├── sorting_service.py      ← Merge Sort, Quick Sort, Heap PQ
│   │   ├── graph_service.py        ← Dijkstra, Bellman-Ford, BFS, DFS, Prim MST, Floyd-Warshall
│   │   ├── greedy_service.py       ← Fractional Knapsack, Job Scheduling, Activity Selection
│   │   ├── dp_service.py           ← 0/1 Knapsack, Floyd-Warshall, Multi-Stage DP
│   │   └── pipeline_service.py     ← Full end-to-end workflow
│   ├── routes/
│   │   ├── sorting_routes.py       ← POST /sorting/prioritize
│   │   ├── graph_routes.py         ← POST /graph/route
│   │   └── optimization_routes.py  ← POST /greedy/assign, /dp/optimize, /pipeline/run, GET /benchmark
│   └── utils/
│       ├── data_generator.py       ← Random delivery/graph generators
│       └── performance.py          ← Benchmarking across input sizes
└── frontend/
    └── templates/
        ├── index.html              ← Landing page
        └── dashboard.html          ← Full interactive dashboard
```

---

## Setup & Run

### 1. Install dependencies
```bash
pip install flask flask-cors
```

### 2. Run the server
```bash
cd backend
python app.py
```

### 3. Open browser
```
http://localhost:5000           ← Home page
http://localhost:5000/dashboard ← Dashboard
```

---

## API Endpoints

### POST /sorting/prioritize
**Request:**
```json
{ "count": 15 }
```
**Response:**
```json
{
  "result": {
    "merge_sort": { "sorted_by": "deadline", "result": [...], "time_ms": 0.04 },
    "quick_sort": { "sorted_by": "priority (desc)", "result": [...], "time_ms": 0.02 },
    "heap_sort":  { "sorted_by": "deadline + priority", "result": [...], "time_ms": 0.05 },
    "comparison": { "merge_sort_ms": 0.04, "quick_sort_ms": 0.02, "heap_sort_ms": 0.05 }
  }
}
```

### POST /graph/route
**Request:**
```json
{ "num_nodes": 10, "src": 0, "dst": 9 }
```
**Response:**
```json
{
  "result": {
    "dijkstra":    { "path": [0,3,7,9], "cost": 78.73, "time_ms": 0.08 },
    "bellman_ford":{ "path": [0,3,7,9], "cost": 78.73, "time_ms": 0.12 },
    "bfs":         { "path": [0,2,9],   "time_ms": 0.04 },
    "dfs":         { "path": [0,1,9],   "time_ms": 0.02 },
    "mst":         { "edges": [...], "total_cost": 142.5, "time_ms": 0.06 }
  }
}
```

### POST /greedy/assign
**Request:**
```json
{ "count": 12, "capacity": 500 }
```
**Response:**
```json
{
  "result": {
    "fractional_knapsack": { "assigned": [...], "total_value": 72.4, "count": 8 },
    "job_scheduling":      { "scheduled": [...], "total_profit": 64, "count": 6 },
    "activity_selection":  { "selected": [...], "count": 5 }
  }
}
```

### POST /dp/optimize
**Request:**
```json
{ "count": 10, "capacity": 80, "num_nodes": 8 }
```
**Response:**
```json
{
  "result": {
    "knapsack_01":   { "selected": [...], "optimal_value": 29, "item_count": 4 },
    "floyd_warshall":{ "matrix_src_row": [0,12.1,-1,...], "time_ms": 0.22 },
    "multi_stage":   { "path": [0,3,7], "cost": 45.2 }
  }
}
```

### POST /pipeline/run
**Request:**
```json
{ "count": 10, "num_nodes": 10, "vehicle_count": 3, "capacity": 100 }
```
**Response:** Full workflow result with timing for each module.

### GET /benchmark
Returns performance data across n=100, 500, 1000 for sorting and n=10, 50, 100 for graphs.

---

## Algorithms Implemented

| Module | Algorithm | Complexity |
|--------|-----------|------------|
| Sorting | Merge Sort | O(n log n) |
| Sorting | Quick Sort | O(n log n) avg |
| Sorting | Heap Priority Queue | O(n log n) |
| Graph | Dijkstra | O((V+E) log V) |
| Graph | Bellman-Ford | O(VE) |
| Graph | BFS | O(V+E) |
| Graph | DFS | O(V+E) |
| Graph | Prim's MST | O(E log V) |
| Graph | Floyd-Warshall | O(V³) |
| Greedy | Fractional Knapsack | O(n log n) |
| Greedy | Job Scheduling | O(n²) |
| Greedy | Activity Selection | O(n log n) |
| DP | 0/1 Knapsack | O(nW) |
| DP | Multi-Stage DP | O(V²) |
