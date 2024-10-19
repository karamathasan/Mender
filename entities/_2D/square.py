from entity import Entity2D
import pygame.draw as draw
import numpy
from transform import Transform2D

class Square(Entity2D):
    def __init__(self, size, origin, transform: Transform2D):
        '''
        Paramaters:
            size: the side length of the square 
            origin: the origin in 2D of the square
        '''
        self.size = size
        self.origin = origin
        self.transform = transform

    def draw(self):
        draw.rect