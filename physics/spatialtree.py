from abc import ABC
from physics.transform import Transform, Transform2D, Transform3D
"""
Each spatial tree object is actually treated as a node
"""
class SpatialTree(ABC):
    def __init__(self, bounds, transform, capacity, children):
        self.bounds = bounds
        self.transform: Transform = transform
        self.capacity = capacity
        self.children = []
        if children:
            for child in children:
                self.add(child)

    def add(self, element):
        self.children.append(element)
        if len(self.children) > self.capacity:
            self.split()

    def split(self):
        pass

class QuadTree(SpatialTree):
    def __init__(self, bounds, capacity, children):
        super().__init__(bounds, capacity, children)

class OctTree(SpatialTree):
    pass