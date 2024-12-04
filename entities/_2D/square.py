from physics.entity import Entity2D
from physics.transform import Transform2D
from physics.dynamics import Dynamics2D
from camera import Camera2D

import pygame
import numpy as np

class Square(Entity2D):
    def __init__(self, size, mass = 10.0, transform : Transform2D = None, dynamics:Dynamics2D = None, gravity_enabled = True, color = "white"):
        '''
        Parameters:
            size: the side length of the square 
            origin: the origin in 2D of the square
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