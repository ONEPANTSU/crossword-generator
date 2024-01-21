from dataclasses import dataclass


@dataclass
class Point:
    x: int
    y: int

    def __hash__(self):
        return hash(self.x) ^ hash(self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y