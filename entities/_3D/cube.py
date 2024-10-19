from entity import Entity2D
import pygame.draw as draw
import numpy

class Square(Entity2D):

    def __init__(self, size, transform):
        '''
        Paramaters:
            size: the side length of the cube
            transform: the cube's transform, which includes its orientation and position
        '''
    # def render(self):
    #     draw.