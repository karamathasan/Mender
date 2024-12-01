from physics.entity import Entity2D
from physics.transform import Transform2D
from physics.dynamics import Dynamics2D
from physics.constraints.gravity import Gravity2D

import pygame
import numpy as np

class Circle(Entity2D):
    def __init__(self, radius, mass = 10.0, transform:Transform2D = None, dynamics:Dynamics2D = None, gravity_enabled = True,color = "white"):
        '''
        Paramaters:
            radius: the radius of the circle
            origin: the origin in 2D of the circle
        '''
        super().__init__(mass, transform, dynamics, gravity_enabled)
        self.radius = radius
        self.color = color

    def draw(self, camera):
        originScreen = camera.ToScreen(self.transform.position)
        pygame.draw.circle(camera.screen, self.color, originScreen, self.radius)