import pygame
import numpy
from physics.entity import Entity3D
from physics.transform import Transform3D

class Cube(Entity3D):

    def __init__(self, size, transform: Transform3D = None):
        '''
        Parameters:
            size: the side length of the cube
            transform: the cube's transform, which includes its orientation and position
        '''
        self.size = size
        if transform is None:
            self.transform = Transform3D()
        else: self.transform = transform
    # def render(self):
    #     draw.