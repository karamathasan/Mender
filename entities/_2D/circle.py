from entity import Entity2D
from transform import Transform2D

import pygame
import numpy

class Circle(Entity2D):
    def __init__(self, radius, transform=None, color = "white"):
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

    # def render(self, scene):
    #     origin = pygame.Vector2(self.origin[0], self.origin[1])
    #     pygame.draw.circle(scene.screen, "red", origin, self.radius)

    # def draw(self):
    #     return lambda screen, color, origin, radius : pygame.draw.circle(screen, color, origin, radius)

    def draw(self, camera):
        originScreen = camera.ToScreen(self.transfrom.position)
        pygame.draw.circle(camera.screen, self.color, originScreen, self.radius)