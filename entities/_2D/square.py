from physics.entity import Entity2D
from physics.transform import Transform2D
from physics.dynamics import Dynamics2D
from camera import Camera2D

import pygame
import numpy as np

class Square(Entity2D):
    def __init__(self, size, color = "white", mass = 10.0, transform : Transform2D = None, dynamics:Dynamics2D = None, gravity_enabled = True):
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

    def draw(self, camera: Camera2D):
        originScreen = camera.Vec2Screen(self.transform.position)
        pygame.draw.rect(camera.screen, self.color, pygame.rect.Rect(
                originScreen[0],
                originScreen[1],
                camera.toScreenSpace(self.size),
                camera.toScreenSpace(self.size)
            ))