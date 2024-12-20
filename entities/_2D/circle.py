from physics.entity import Entity2D
from physics.transform import Transform2D
from physics.dynamics import Dynamics2D
from physics.constraints.gravity import Gravity2D

import pygame
import numpy as np

from camera import Camera2D

class Circle(Entity2D):
    '''
    Create a Circle entity affected by basic physics

    Parameters:
        radius: the radius of the circle
        color: the color of the circle as a string
        mass: the mass of the entity
        transform: the Transform2D that will be associated with this entity
        dynamics: the Dynamics2D that will be associated with this entity
        gravity_enabled: if gravity is enabled on this entity 
    '''
    def __init__(self, radius, color:str = "white", mass = 10.0, transform:Transform2D = None, dynamics:Dynamics2D = None, gravity_enabled = True):
        super().__init__(mass, transform, dynamics, gravity_enabled)
        self.radius = radius
        self.color = color

    def draw(self, camera: Camera2D):
        originScreen = camera.Vec2Screen(self.transform.position)
        pxRad = camera.toScreenSpace(self.radius)
        pygame.draw.circle(camera.screen, self.color, originScreen, pxRad)