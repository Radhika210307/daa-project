import random
import math


class Graph:
    def __init__(self, num_nodes=10):
        self.num_nodes = num_nodes
        self.adj = {i: [] for i in range(num_nodes)}  # {node: [(neighbor, weight)]}

    def add_edge(self, u, v, w):
        self.adj[u].append((v, w))
        self.adj[v].append((u, w))

    def to_dict(self):
        return {
            "num_nodes": self.num_nodes,
            "edges": [
                {"from": u, "to": v, "weight": w}
                for u, neighbors in self.adj.items()
                for v, w in neighbors
                if u < v
            ],
        }

    @staticmethod
    def random_graph(num_nodes=10, density=0.4):
        g = Graph(num_nodes)
        for i in range(num_nodes):
            for j in range(i + 1, num_nodes):
                if random.random() < density:
                    w = round(random.uniform(1, 100), 2)
                    g.add_edge(i, j, w)
        # Ensure connectivity via spanning tree
        nodes = list(range(num_nodes))
        random.shuffle(nodes)
        for k in range(len(nodes) - 1):
            u, v = nodes[k], nodes[k + 1]
            # Check if edge already exists
            existing = {nb for nb, _ in g.adj[u]}
            if v not in existing:
                w = round(random.uniform(1, 100), 2)
                g.add_edge(u, v, w)
        return g

    @staticmethod
    def from_dict(d):
        g = Graph(d["num_nodes"])
        for e in d.get("edges", []):
            g.add_edge(e["from"], e["to"], e["weight"])
        return g
