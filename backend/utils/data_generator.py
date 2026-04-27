import random
import string
from models.delivery import DeliveryRequest
from models.vehicle import Vehicle
from models.graph import Graph


def generate_deliveries(n=10):
    deliveries = []
    for i in range(n):
        d = DeliveryRequest(
            id=f"D{i+1:04d}",
            weight=round(random.uniform(1, 50), 2),
            deadline=random.randint(1, 24),
            priority=random.randint(1, 10),
            location=random.randint(0, 9),
        )
        deliveries.append(d)
    return deliveries


def generate_vehicles(n=3, capacity=200):
    return [Vehicle(id=f"V{i+1:03d}", capacity=capacity) for i in range(n)]


def generate_graph(num_nodes=10, density=0.5):
    return Graph.random_graph(num_nodes=num_nodes, density=density)
