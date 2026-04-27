class Vehicle:
    def __init__(self, id, capacity):
        self.id = id
        self.capacity = float(capacity)
        self.assigned = []
        self.current_load = 0.0

    def can_carry(self, weight):
        return self.current_load + weight <= self.capacity

    def assign(self, delivery):
        self.assigned.append(delivery)
        self.current_load += delivery.weight

    def to_dict(self):
        return {
            "id": self.id,
            "capacity": self.capacity,
            "current_load": self.current_load,
            "assigned": [d.to_dict() for d in self.assigned],
        }

    @staticmethod
    def from_dict(d):
        return Vehicle(id=d.get("id"), capacity=d.get("capacity", 100))
