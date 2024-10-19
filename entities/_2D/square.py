from entity import Entity2D
import pygame.draw as draw
import numpy

class Square(Entity2D):

    def __init__(self, size, origin):
        '''
        Paramaters:
            size: the side length of the square 
            origin: the origin in 2D of the square
        '''
    def render(self):
        draw.rect