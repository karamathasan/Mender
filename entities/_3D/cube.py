import pygame
import numpy as np

from physics.entity import Entity3D
from physics.transform import Transform3D
from physics.constraints.gravity import Gravity3D
from physics.dynamics import Dynamics3D
from rendering.edge import Edge3D
from rendering.quaternion import Quaternion
from camera import Camera3D

class Cube(Entity3D):

    def __init__(self, size, color = "white", mass = 10.0, transform: Transform3D = None, dynamics: Dynamics3D = None, gravity_enabled = True):
        '''
        Parameters:
            size: the side length of the cube
            transform: the cube's transform, which includes its orientation and position
        '''
        super().__init__(mass, transform, dynamics, gravity_enabled)
        self.size = size
        self.color = color


        s = size * np.sqrt(2)/2
        self.vertices = [
            np.array([-s,-s,-s]), # 0
            np.array([s,-s,-s]), # 1

            np.array([s,-s,s]), # 2
            np.array([-s,-s,s]), # 3

            np.array([-s,s,-s]), # 4
            np.array([s,s,-s]), # 5

            np.array([s,s,s]), # 6
            np.array([-s,s,s]), # 7
        ]

        self.edges=[
            Edge3D(self.vertices[0],self.vertices[1],self.transform),
            Edge3D(self.vertices[0],self.vertices[3],self.transform),
            Edge3D(self.vertices[0],self.vertices[4],self.transform),
            Edge3D(self.vertices[1],self.vertices[2],self.transform),
            Edge3D(self.vertices[1],self.vertices[5],self.transform),
            Edge3D(self.vertices[2],self.vertices[3],self.transform),
            Edge3D(self.vertices[2],self.vertices[6],self.transform),
            Edge3D(self.vertices[3],self.vertices[7],self.transform),
            Edge3D(self.vertices[4],self.vertices[5],self.transform),
            Edge3D(self.vertices[4],self.vertices[7],self.transform),
            Edge3D(self.vertices[5],self.vertices[6],self.transform),
            Edge3D(self.vertices[6],self.vertices[7],self.transform)
        ]

    def draw(self, camera: Camera3D):
        for edge in self.edges:
            edge.draw(camera)