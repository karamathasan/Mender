import numpy as np
from abc import ABC
from physics.transform import Transform, Transform2D, Transform3D
from physics.entity import Entity, Entity2D, Entity3D

import pygame

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
    def __init__(self, dimensions: tuple, capacity:int = 4, transform: Transform2D = None, parent = None, depth = 1):
        super().__init__(dimensions, capacity, parent)

        self.transform = transform if transform is not None else Transform2D()
        self.children = []
        self.depth = depth
        # self.is_leaf = True

    def add(self, entity: Entity2D):
        if self.is_leaf:
            self.children.append(entity)
            if len(self.children) > self.capacity and self.depth < 3:
                self.split()
                self.is_leaf = False
        else:
            if entity.transform.position[0] >= self.transform.position[0]:
                if entity.transform.position[1] >= self.transform.position[1]:
                    self.children[2].add(entity)
                else:
                    self.children[1].add(entity)
            else:
                if entity.transform.position[1] >= self.transform.position[1]:
                    self.children[3].add(entity)
                else:
                    self.children[0].add(entity)
                    
    def split(self):
        dim = (self.dimensions[0]/2, self.dimensions[1]/2)
        # quadrants are in counterclockwise order from the bottom left
        q1 = QuadTree(dim, self.capacity, Transform2D(self.transform.position + (np.array([-self.dimensions[0]/4, -self.dimensions[1]/4]))), self, self.depth+1)
        q2 = QuadTree(dim, self.capacity, Transform2D(self.transform.position + (np.array([self.dimensions[0]/4, -self.dimensions[1]/4]))), self, self.depth+1)
        q3 = QuadTree(dim, self.capacity, Transform2D(self.transform.position + (np.array([self.dimensions[0]/4, self.dimensions[1]/4]))), self, self.depth+1)
        q4 = QuadTree(dim, self.capacity, Transform2D(self.transform.position + (np.array([-self.dimensions[0]/4, self.dimensions[1]/4]))), self, self.depth+1)
        for child in self.children:
            if q1.bounds(child):
                q1.add(child)
            if q2.bounds(child):
                q2.add(child)
            if q3.bounds(child):
                q3.add(child)
            if q4.bounds(child):
                q4.add(child)
        self.children = [q1,q2,q3,q4]

    def __contains__(self):
        pass

    def bounds(self, child: Entity):
        w,h = self.dimensions
        x,y = self.transform.position
        left_bound = w/2 - x
        right_bound = w/2 + x
        bottom_bound = h/2 - y
        top_bound = h/2 + y

        c_x, c_y = child.transform.position
        return left_bound <= c_x <= right_bound and bottom_bound <= c_y <= top_bound 
    
    def rebound(self):
        # removes children that leave the quad
        if self.is_leaf:
            for i in range(len(self.children)):
                child = self.children[i]
                missing_children = []
                if self.bounds(child):
                    missing_children.append(i)

            rmv_count = 0
            for idx in missing_children:
                self.children.remove(idx - rmv_count)

            if len(self.children) == 0:
                del self

                    

        pass
    
    def draw(self, camera):
        w,h = self.dimensions
        # left = camera.toScreenSpace(self.transform.position[0] - w/2)
        # top = camera.toScreenSpace(self.transform.position[1] + h/2)
        left, top = camera.Vec2Screen(self.transform.position + (np.array([-w/2,h/2])))

        pygame.draw.rect(camera.screen, 'white', pygame.rect.Rect(
            left, top, camera.toScreenSpace(w), camera.toScreenSpace(h)
        ), 2)
        if not self.is_leaf:
            for child in self.children:
                child.draw(camera)
                

class OctTree(SpatialTree):
    pass