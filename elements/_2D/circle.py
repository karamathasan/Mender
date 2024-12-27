from element import Element2D
from physics.transform import Transform2D

import pygame
import numpy

class Circle(Element2D):
    def __init__(self, radius, transform : Transform2D = None, color = "white"):
        '''
        Paramaters:
            radius: the radius of the circle
            origin: the origin in 2D of the circle
            transform: the transform associated with this element
            color: the color of the circle
        '''
        self.radius = radius
        if transform is None:
            self.transform = Transform2D()
        else: self.transform = transform

        self.color = color

    def draw(self, camera):
        originScreen = camera.Vec2Screen(self.transform.position)
        pygame.draw.circle(camera.screen, self.color, originScreen, camera.toScreenSpace(self.radius))