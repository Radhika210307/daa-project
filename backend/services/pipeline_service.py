import time
from services import sorting_service, graph_service, greedy_service, dp_service
from utils.data_generator import generate_deliveries, generate_graph


def run_pipeline(deliveries, vehicles, graph, capacity=100):
    results = {}
    pipeline_start = time.perf_counter()

    # Step 1: Sort deliveries
    t0 = time.perf_counter()
    sort_result = sorting_service.prioritize(deliveries)
    results["sorting"] = {
        "time_ms": round((time.perf_counter() - t0) * 1000, 4),
        "data": sort_result,
    }

    # Step 2: Greedy assignment
    t0 = time.perf_counter()
    greedy_result = greedy_service.assign(deliveries, capacity=capacity)
    results["greedy"] = {
        "time_ms": round((time.perf_counter() - t0) * 1000, 4),
        "data": greedy_result,
    }

    # Step 3: DP optimization
    t0 = time.perf_counter()
    src = 0
    dst = graph.num_nodes - 1
    dp_result = dp_service.optimize(deliveries, graph, capacity=capacity, src=src, dst=dst)
    results["dp"] = {
        "time_ms": round((time.perf_counter() - t0) * 1000, 4),
        "data": dp_result,
    }

    # Step 4: Route optimization
    t0 = time.perf_counter()
    route_result = graph_service.route(graph, src, dst)
    results["routing"] = {
        "time_ms": round((time.perf_counter() - t0) * 1000, 4),
        "data": route_result,
    }

    # Step 5: Cost summary
    dijkstra_cost = route_result["dijkstra"]["cost"]
    bellman_cost = route_result["bellman_ford"]["cost"]
    greedy_value = greedy_result["fractional_knapsack"]["total_value"]
    dp_value = dp_result["knapsack_01"]["optimal_value"]

    results["cost_summary"] = {
        "dijkstra_cost": dijkstra_cost,
        "bellman_ford_cost": bellman_cost,
        "greedy_value": greedy_value,
        "dp_value": dp_value,
        "greedy_vs_dp_ratio": round(greedy_value / dp_value, 4) if dp_value else 0,
    }

    total_time = round((time.perf_counter() - pipeline_start) * 1000, 4)
    results["total_pipeline_time_ms"] = total_time
    results["num_deliveries"] = len(deliveries)
    results["num_nodes"] = graph.num_nodes

    return results
