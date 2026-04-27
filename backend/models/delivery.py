import random
import time


class DeliveryRequest:
    def __init__(self, id, weight, deadline, priority, location):
        self.id = id
        self.weight = float(weight)
        self.deadline = int(deadline)
        self.priority = int(priority)
        self.location = int(location)

    def to_dict(self):
        return {
            "id": self.id,
            "weight": self.weight,
            "deadline": self.deadline,
            "priority": self.priority,
            "location": self.location,
        }

    @staticmethod
    def from_dict(d):
        return DeliveryRequest(
            id=d.get("id", f"D{random.randint(1000,9999)}"),
            weight=d.get("weight", random.uniform(1, 50)),
            deadline=d.get("deadline", random.randint(1, 24)),
            priority=d.get("priority", random.randint(1, 10)),
            location=d.get("location", random.randint(0, 9)),
        )
