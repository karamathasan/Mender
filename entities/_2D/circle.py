from physics.entity import Entity2D
from physics.transform import Transform2D
from physics.dynamics import Dynamics2D
from physics.constraints.gravity import Gravity2D

import pygame
import numpy as np

class Circle(Entity2D):
    def __init__(self, radius, transform:Transform2D = None, dynamics:Dynamics2D = None, color = "white"):
        '''
        Paramaters:
            radius: the radius of the circle
            origin: the origin in 2D of the circle
        '''
        super().__init__(transform, dynamics)
        self.radius = radius
        self.color = color
        self.applyConstraint(Gravity2D())

    def draw(self, camera):
        originScreen = camera.ToScreen(self.transform.position)
        pygame.draw.circle(camera.screen, self.color, originScreen, self.radius)