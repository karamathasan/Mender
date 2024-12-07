import pygame
import numpy as np

from physics.entity import Entity3D
from physics.transform import Transform3D
from physics.constraints.gravity import Gravity3D
from physics.dynamics import Dynamics3D
from rendering.edge import Edge3D
from camera import Camera3D

class Cube(Entity3D):

    def __init__(self, size, color = "white", mass = 10.0, transform: Transform3D = None, dynamics: Dynamics3D = None, gravity_enabled = True):
        '''
        Parameters:
            size: the side length of the cube
            transform: the cube's transform, which includes its orientation and position
        '''
        self.size = size
        if transform is None:
            self.transform = Transform3D()
        else: self.transform = transform

        s = size * np.sqrt(2)/2
        self.vertices = [
            self.transform.position + np.array([-s,-s,-s]), # 0
            self.transform.position + np.array([s,-s,-s]), # 1

            self.transform.position + np.array([s,-s,s]), # 2
            self.transform.position + np.array([-s,-s,s]), # 3

            self.transform.position + np.array([-s,s,-s]), # 4
            self.transform.position + np.array([s,s,-s]), # 5

            self.transform.position + np.array([s,s,s]), # 6
            self.transform.position + np.array([-s,s,s]), # 7
        ]

        self.edges=[
            Edge3D(self.vertices[0],self.vertices[1]),
            Edge3D(self.vertices[0],self.vertices[4]),
            Edge3D(self.vertices[0],self.vertices[3]),
            Edge3D(self.vertices[1],self.vertices[5]),
            Edge3D(self.vertices[1],self.vertices[2]),
            Edge3D(self.vertices[4],self.vertices[5]),
            Edge3D(self.vertices[4],self.vertices[7]),
            Edge3D(self.vertices[3],self.vertices[7]),
            Edge3D(self.vertices[3],self.vertices[2]),
            Edge3D(self.vertices[5],self.vertices[6]),
            Edge3D(self.vertices[2],self.vertices[6]),
            Edge3D(self.vertices[7],self.vertices[6]),
        ]

    
    def draw(self, camera: Camera3D):
        # print(self.edges[0].vertices)
        for edge in self.edges:
            a = camera.Vec2Screen(edge.vertices[0]) 
            b = camera.Vec2Screen(edge.vertices[1]) 
            pygame.draw.line(camera.screen, "white", a,b)