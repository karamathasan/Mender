import pygame
import numpy as np
from entity import Entity3D
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
        self.vertices = [
            self.transform.position + np.array([size * np.sqrt(2)/2, size * np.sqrt(2)/2, size * np.sqrt(2)/2]),
            self.transform.position + np.array([size * np.sqrt(2)/2, size * np.sqrt(2)/2, size * -np.sqrt(2)/2]),

            self.transform.position + np.array([size * np.sqrt(2)/2, size * -np.sqrt(2)/2, size * np.sqrt(2)/2]),
            self.transform.position + np.array([size * np.sqrt(2)/2, size * -np.sqrt(2)/2, size * -np.sqrt(2)/2]),

            self.transform.position + np.array([size * -np.sqrt(2)/2, size * -np.sqrt(2)/2, size * np.sqrt(2)/2]),
            self.transform.position + np.array([size * -np.sqrt(2)/2, size * -np.sqrt(2)/2, size * -np.sqrt(2)/2]),
        ]

    def draw(self, camera):
        # draw lines between the correct vertices
        pass