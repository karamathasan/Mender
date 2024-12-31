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
        self.is_leaf = True # this may be unnecessary

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
        if self.is_leaf:
            self.children.append(entity)
            if len(self.children) > self.capacity:
                self.split()
                self.is_leaf = False
        else:
            if entity.transform.position[0] >= self.transform.position[0]:
                if entity.transform.position[1] >= self.transform.position[1]:
                    self.children[3].add(entity)
                else:
                    self.children[2].add(entity)
            else:
                if entity.transform.position[1] >= self.transform.position[1]:
                    self.children[4].add(entity)
                else:
                    self.children[1].add(entity)
                    
    def split(self):
        dim = (self.dimensions[0]//2, self.dimensions[1]//2)
        # quadrants are in counterclockwise order from the bottom left
        q1 = QuadTree(dim, self.capacity, self.transform.position + np.array([-self.dimensions[0]//2, -self.dimensions[1]//2]), self)
        q2 = QuadTree(dim, self.capacity, self.transform.position + np.array([self.dimensions[0]//2, -self.dimensions[1]//2]), self)
        q3 = QuadTree(dim, self.capacity, self.transform.position + np.array([self.dimensions[0]//2, self.dimensions[1]//2]), self)
        q4 = QuadTree(dim, self.capacity, self.transform.position + np.array([-self.dimensions[0]//2, self.dimensions[1]//2]), self)
        for child in self.children:
            if child.transform.position[0] >= self.transform.position[0]:
                if child.transform.position[1] >= self.transform.position[1]:
                    q3.add(child)
                else:
                    q2.add(child)
            else:
                if child.transform.position[1] >= self.transform.position[1]:
                    q4.add(child)
                else:
                    q1.add(child)
        self.children = [q1,q2,q3,q4]

    def __contains__(self):
        pass
                

class OctTree(SpatialTree):
    pass