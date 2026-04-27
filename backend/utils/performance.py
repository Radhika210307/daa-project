import time
from utils.data_generator import generate_deliveries, generate_graph
from services import sorting_service, graph_service, greedy_service, dp_service


def benchmark_sorting(sizes=(100, 500, 1000)):
    results = []
    for n in sizes:
        deliveries = generate_deliveries(n)
        _, t_merge = sorting_service.run_merge_sort(deliveries)
        _, t_quick = sorting_service.run_quick_sort(deliveries)
        _, t_heap = sorting_service.run_heap_sort(deliveries)
        results.append({
            "n": n,
            "merge_sort_ms": round(t_merge, 4),
            "quick_sort_ms": round(t_quick, 4),
            "heap_sort_ms": round(t_heap, 4),
        })
    return results


def benchmark_graph(node_counts=(10, 50, 100)):
    results = []
    for n in node_counts:
        g = generate_graph(num_nodes=n, density=0.3)
        src, dst = 0, n - 1

        t0 = time.perf_counter()
        graph_service.dijkstra(g, src, dst)
        t_dij = (time.perf_counter() - t0) * 1000

        t0 = time.perf_counter()
        graph_service.bellman_ford(g, src, dst)
        t_bell = (time.perf_counter() - t0) * 1000

        t0 = time.perf_counter()
        graph_service.prim_mst(g)
        t_mst = (time.perf_counter() - t0) * 1000

        results.append({
            "n": n,
            "dijkstra_ms": round(t_dij, 4),
            "bellman_ford_ms": round(t_bell, 4),
            "mst_ms": round(t_mst, 4),
        })
    return results


def benchmark_greedy_vs_dp(sizes=(10, 50, 100)):
    results = []
    for n in sizes:
        deliveries = generate_deliveries(n)
        g = generate_graph(num_nodes=10)

        t0 = time.perf_counter()
        greedy_service.assign(deliveries, capacity=500)
        t_greedy = (time.perf_counter() - t0) * 1000

        t0 = time.perf_counter()
        dp_service.optimize(deliveries, g, capacity=100)
        t_dp = (time.perf_counter() - t0) * 1000

        results.append({
            "n": n,
            "greedy_ms": round(t_greedy, 4),
            "dp_ms": round(t_dp, 4),
        })
    return results


def run_all():
    return {
        "sorting": benchmark_sorting(),
        "graph": benchmark_graph(),
        "greedy_vs_dp": benchmark_greedy_vs_dp(),
    }
