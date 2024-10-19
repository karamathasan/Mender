from entity import Entity2D
import pygame.draw as draw
import pygame
import numpy

class Circle(Entity2D):

    def __init__(self, radius, origin):
        '''
        Paramaters:
            radius: the radius of the circle
            origin: the origin in 2D of the circle
        '''
        self.radius = radius
        self.origin = origin

    def render(self, screen):
        origin = pygame.Vector2(self.origin[0], self.origin[1])
        print(self.origin)
        print(origin)
        draw.circle(screen, "white", origin, self.radius)