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

        ooo=    self.transform.position
        loo=    self.transform.position + np.array([size,0,0])
        olo=    self.transform.position + np.array([0,size,0])
        ool=    self.transform.position + np.array([0,0,size])
        llo=    self.transform.position + np.array([size,size,0])
        lol=    self.transform.position + np.array([size,0,size])
        oll=    self.transform.position + np.array([0,size,size])
        lll=    self.transform.position + np.array([size,size,size])

        self.edges=[
            Edge3D(ooo,loo),
            Edge3D(ooo,olo),
            Edge3D(ooo,ool),
            Edge3D(loo,llo),
            Edge3D(loo,lol),
            Edge3D(olo,llo),
            Edge3D(olo,oll),
            Edge3D(ool,oll),
            Edge3D(ool,lol),
            Edge3D(llo,lll),
            Edge3D(lol,lll),
            Edge3D(oll,lll),
        ]

    
    def draw(self, camera: Camera3D):
        # print(self.edges[0].vertices)
        for edge in self.edges:
            a = camera.Vec2Screen(edge.vertices[0]) 
            b = camera.Vec2Screen(edge.vertices[1]) 
            pygame.draw.line(camera.screen, "white", a,b)