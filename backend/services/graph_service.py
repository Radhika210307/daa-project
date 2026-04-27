import heapq
import time
import math
from collections import deque


# ─── Dijkstra ─────────────────────────────────────────────────────────────────

def dijkstra(graph, src, dst):
    dist = {n: math.inf for n in graph.adj}
    prev = {n: None for n in graph.adj}
    dist[src] = 0
    pq = [(0, src)]

    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in graph.adj.get(u, []):
            nd = dist[u] + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))

    path = _reconstruct(prev, src, dst)
    return dist[dst] if dist[dst] != math.inf else -1, path


# ─── Bellman-Ford ─────────────────────────────────────────────────────────────

def bellman_ford(graph, src, dst):
    dist = {n: math.inf for n in graph.adj}
    prev = {n: None for n in graph.adj}
    dist[src] = 0

    edges = []
    for u, neighbors in graph.adj.items():
        for v, w in neighbors:
            edges.append((u, v, w))

    n = graph.num_nodes
    for _ in range(n - 1):
        updated = False
        for u, v, w in edges:
            if dist[u] != math.inf and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u
                updated = True
        if not updated:
            break

    # Negative cycle check
    for u, v, w in edges:
        if dist[u] != math.inf and dist[u] + w < dist[v]:
            return -1, []  # negative cycle detected

    path = _reconstruct(prev, src, dst)
    return dist[dst] if dist[dst] != math.inf else -1, path


# ─── BFS ──────────────────────────────────────────────────────────────────────

def bfs(graph, src, dst):
    visited = set()
    queue = deque([[src]])
    if src == dst:
        return [src]

    while queue:
        path = queue.popleft()
        node = path[-1]
        if node in visited:
            continue
        visited.add(node)
        for neighbor, _ in graph.adj.get(node, []):
            new_path = path + [neighbor]
            if neighbor == dst:
                return new_path
            queue.append(new_path)
    return []


# ─── DFS ──────────────────────────────────────────────────────────────────────

def dfs(graph, src, dst):
    visited = set()
    path = []

    def _dfs(node):
        if node in visited:
            return False
        visited.add(node)
        path.append(node)
        if node == dst:
            return True
        for neighbor, _ in graph.adj.get(node, []):
            if _dfs(neighbor):
                return True
        path.pop()
        return False

    _dfs(src)
    return path


# ─── Prim's MST ───────────────────────────────────────────────────────────────

def prim_mst(graph):
    if not graph.adj:
        return [], 0

    start = next(iter(graph.adj))
    visited = {start}
    edges_heap = []
    total_cost = 0
    mst_edges = []

    for v, w in graph.adj.get(start, []):
        heapq.heappush(edges_heap, (w, start, v))

    while edges_heap and len(visited) < graph.num_nodes:
        w, u, v = heapq.heappop(edges_heap)
        if v in visited:
            continue
        visited.add(v)
        total_cost += w
        mst_edges.append({"from": u, "to": v, "weight": round(w, 2)})
        for neighbor, nw in graph.adj.get(v, []):
            if neighbor not in visited:
                heapq.heappush(edges_heap, (nw, v, neighbor))

    return mst_edges, round(total_cost, 2)


# ─── Floyd-Warshall (all-pairs shortest path) ─────────────────────────────────

def floyd_warshall(graph):
    n = graph.num_nodes
    INF = math.inf
    dist = [[INF] * n for _ in range(n)]

    for i in range(n):
        dist[i][i] = 0
    for u, neighbors in graph.adj.items():
        for v, w in neighbors:
            dist[u][v] = min(dist[u][v], w)
            dist[v][u] = min(dist[v][u], w)

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    # Serialize (replace inf)
    result = []
    for row in dist:
        result.append([round(x, 2) if x != INF else -1 for x in row])
    return result


# ─── Helper ───────────────────────────────────────────────────────────────────

def _reconstruct(prev, src, dst):
    path = []
    cur = dst
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    path.reverse()
    return path if path and path[0] == src else []


# ─── Service Entry Point ───────────────────────────────────────────────────────

def route(graph, src, dst):
    t0 = time.perf_counter()
    d_cost, d_path = dijkstra(graph, src, dst)
    t_dijkstra = (time.perf_counter() - t0) * 1000

    t0 = time.perf_counter()
    b_cost, b_path = bellman_ford(graph, src, dst)
    t_bellman = (time.perf_counter() - t0) * 1000

    t0 = time.perf_counter()
    bfs_path = bfs(graph, src, dst)
    t_bfs = (time.perf_counter() - t0) * 1000

    t0 = time.perf_counter()
    dfs_path = dfs(graph, src, dst)
    t_dfs = (time.perf_counter() - t0) * 1000

    t0 = time.perf_counter()
    mst_edges, mst_cost = prim_mst(graph)
    t_mst = (time.perf_counter() - t0) * 1000

    return {
        "source": src,
        "destination": dst,
        "dijkstra": {
            "path": d_path,
            "cost": round(d_cost, 2) if d_cost != -1 else "unreachable",
            "time_ms": round(t_dijkstra, 4),
        },
        "bellman_ford": {
            "path": b_path,
            "cost": round(b_cost, 2) if b_cost != -1 else "unreachable",
            "time_ms": round(t_bellman, 4),
        },
        "bfs": {
            "path": bfs_path,
            "time_ms": round(t_bfs, 4),
        },
        "dfs": {
            "path": dfs_path,
            "time_ms": round(t_dfs, 4),
        },
        "mst": {
            "edges": mst_edges,
            "total_cost": mst_cost,
            "time_ms": round(t_mst, 4),
        },
        "comparison": {
            "dijkstra_ms": round(t_dijkstra, 4),
            "bellman_ford_ms": round(t_bellman, 4),
            "bfs_ms": round(t_bfs, 4),
            "dfs_ms": round(t_dfs, 4),
            "mst_ms": round(t_mst, 4),
        },
    }
