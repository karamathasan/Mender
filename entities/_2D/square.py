from physics.entity import Entity2D
from physics.transform import Transform2D
from physics.dynamics import Dynamics2D
from camera import Camera2D

import pygame
import numpy as np

class Square(Entity2D):
    def __init__(self, size, color: str = "white", mass = 10.0, transform : Transform2D = None, dynamics:Dynamics2D = None, gravity_enabled = True):
        '''
        Parameters:
            size: the side length of the square 
            color: the color of the square as a string
            mass: the mass of the entity
            transform: the Transform2D that will be associated with this entity
            dynamics: the Dynamics2D that will be associated with this entity
            gravity_enabled: if gravity is enabled on this entity 
        '''
        super().__init__(mass, transform, dynamics, gravity_enabled)
        self.size = size 
        self.color = color

        self.vertices = [
            np.array([-self.size/2, -self.size/2]),
            np.array([self.size/2, -self.size/2]),
            np.array([self.size/2, self.size/2]),
            np.array([-self.size/2, self.size/2])
        ]

    def draw(self, camera: Camera2D):
        screenVertices = []
        rotmat = np.array(
            [[np.cos(self.transform.orientation), -np.sin(self.transform.orientation)],
             [np.sin(self.transform.orientation), np.cos(self.transform.orientation)]]
        )
        for v in self.vertices:
            screenVertices.append(camera.Vec2Screen(v @ rotmat))
        pygame.draw.polygon(camera.screen, self.color, screenVertices)