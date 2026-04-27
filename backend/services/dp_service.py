import time
import math
import copy
from services.graph_service import floyd_warshall


# ─── 0/1 Knapsack ─────────────────────────────────────────────────────────────

def knapsack_01(deliveries, capacity_int):
    n = len(deliveries)
    W = int(capacity_int)
    weights = [int(math.ceil(d.weight)) for d in deliveries]
    values = [d.priority for d in deliveries]

    dp = [[0] * (W + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(W + 1):
            dp[i][w] = dp[i - 1][w]
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i][w], dp[i - 1][w - weights[i - 1]] + values[i - 1])

    # Traceback
    selected = []
    w = W
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected.append(deliveries[i - 1].to_dict())
            w -= weights[i - 1]

    # Return abbreviated DP table (last row only for large inputs)
    table_preview = dp[n][:min(W + 1, 20)]

    return {
        "selected": selected,
        "optimal_value": dp[n][W],
        "item_count": len(selected),
        "dp_table_last_row_preview": table_preview,
    }


# ─── Multi-Stage Cost Minimization ────────────────────────────────────────────

def multi_stage_dp(graph, src, dst):
    """Stage-based DP for cost minimization across the graph."""
    n = graph.num_nodes
    INF = math.inf

    dist = [INF] * n
    prev = [-1] * n
    dist[src] = 0

    # Topological relaxation using DP (forward pass)
    for _ in range(n - 1):
        new_dist = dist[:]
        for u in range(n):
            if dist[u] == INF:
                continue
            for v, w in graph.adj.get(u, []):
                if dist[u] + w < new_dist[v]:
                    new_dist[v] = dist[u] + w
                    prev[v] = u
        dist = new_dist

    # Reconstruct path
    path = []
    cur = dst
    while cur != -1:
        path.append(cur)
        cur = prev[cur]
        if cur == src:
            path.append(src)
            break
    path.reverse()

    cost = round(dist[dst], 2) if dist[dst] != INF else -1
    return path if path and path[0] == src else [], cost


# ─── Service Entry Point ───────────────────────────────────────────────────────

def optimize(deliveries, graph, capacity=100, src=0, dst=None):
    data = copy.deepcopy(deliveries)
    if dst is None:
        dst = graph.num_nodes - 1

    t0 = time.perf_counter()
    ks_result = knapsack_01(data, capacity)
    t_ks = (time.perf_counter() - t0) * 1000

    t0 = time.perf_counter()
    fw_matrix = floyd_warshall(graph)
    t_fw = (time.perf_counter() - t0) * 1000

    t0 = time.perf_counter()
    ms_path, ms_cost = multi_stage_dp(graph, src, dst)
    t_ms = (time.perf_counter() - t0) * 1000

    fw_src_row = fw_matrix[src] if src < len(fw_matrix) else []

    return {
        "knapsack_01": {**ks_result, "time_ms": round(t_ks, 4)},
        "floyd_warshall": {
            "matrix_src_row": fw_src_row,
            "src": src,
            "note": "Full all-pairs matrix available; showing src row for brevity",
            "time_ms": round(t_fw, 4),
        },
        "multi_stage": {
            "path": ms_path,
            "cost": ms_cost,
            "src": src,
            "dst": dst,
            "time_ms": round(t_ms, 4),
        },
        "comparison": {
            "knapsack_ms": round(t_ks, 4),
            "floyd_warshall_ms": round(t_fw, 4),
            "multi_stage_ms": round(t_ms, 4),
        },
    }
