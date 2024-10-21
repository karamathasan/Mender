from element import Element2D
from physics.transform import Transform2D

import pygame
import numpy

class Circle(Element2D):
    def __init__(self, radius, transform : Transform2D = None, color = "white", filled = True):
        '''
        Paramaters:
            radius: the radius of the circle
            origin: the origin in 2D of the circle
        '''
        self.radius = radius
        if transform is None:
            self.transfrom = Transform2D()
        else: self.transfrom = transform

        self.color = color

    def draw(self, camera):
        originScreen = camera.ToScreen(self.transfrom.position)
        pygame.draw.circle(camera.screen, self.color, originScreen, self.radius)