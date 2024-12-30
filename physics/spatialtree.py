import numpy as np
from abc import ABC
from physics.transform import Transform, Transform2D, Transform3D
from entity import Entity2D, Entity3D

class SpatialTree(ABC):
    def __init__(self, dimensions: tuple, capacity, parent):
        self.dimensions = dimensions
        self.capacity = capacity
        self.children = []
        self.parent = parent

        """
        A each tree should decide how to add in their elements.
        essentially, when we add new elements to a fresh tree, they get subdivided into smaller tree after 
        the tree reaches its capacity
        """

    def add(self, element):
        pass

    def split(self):
        pass

    def __contains__(self):
        pass

    def getNearest(self, element):
        pass

"""
A quadtree should have 4 quadrant attributes. this way, we can properly add values to the right subtrees

"""
class QuadTree(SpatialTree):
    def __init__(self, dimensions: tuple, capacity, transform: Transform2D, parent):
        super().__init__(dimensions, capacity)
        if transform:
            self.transform = transform
        else:
            self.transform = Transform2D()

        self.children = []

    def add(self, entity: Entity2D):
        self.children.append(entity)
        if len(self.children) > self.capacity:
            self.split()

    def split(self):
        dim = (self.dimensions[0]//2, self.dimensions[1]//2)
        # quadrants are in counterclockwise order from the bottom left
        q1 = QuadTree(dim, self.capacity, self.transform.position + np.array([-self.dimensions[0]//2, -self.dimensions[1]//2]), self)
        q2 = QuadTree(dim, self.capacity, self.transform.position + np.array([self.dimensions[0]//2, -self.dimensions[1]//2]), self)
        q3 = QuadTree(dim, self.capacity, self.transform.position + np.array([self.dimensions[0]//2, self.dimensions[1]//2]), self)
        q4 = QuadTree(dim, self.capacity, self.transform.position + np.array([-self.dimensions[0]//2, self.dimensions[1]//2]), self)
        for child in self.children:
            position = child.transform.position
            if position[0] >= self.transform.position[0]:
                if position[1] >= self.transform.position[1]:
                    pass
                else:
                    pass
            else:
                if position[1] >= self.transform.position[1]:
                    pass 
                else:
                    pass

    def __contains__(self):
        pass
                

class OctTree(SpatialTree):
    pass