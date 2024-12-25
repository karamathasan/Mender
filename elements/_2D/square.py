import pygame
import numpy as np
from element import Element2D
from physics.transform import Transform2D

class Square(Element2D):
    def __init__(self, size, color: str = "white", transform : Transform2D = None,):
        '''
        Paramaters:
            size: the side length of the square 
            origin: the origin in 2D of the square
        '''
        self.size = size 
        self.color = color
        self.transform = transform if transform else Transform2D()
        self.vertices = [
            np.array([-self.size/2, -self.size/2]),
            np.array([self.size/2, -self.size/2]),
            np.array([self.size/2, self.size/2]),
            np.array([-self.size/2, self.size/2])
        ]
        self.color = color

    def draw(self, camera):
        screenVertices = []
        rotmat = np.array(
            [[np.cos(self.transform.orientation), -np.sin(self.transform.orientation)],
             [np.sin(self.transform.orientation), np.cos(self.transform.orientation)]]
        )
        for v in self.vertices:
            screenVertices.append(camera.Vec2Screen(v @ rotmat + self.transform.position))
        pygame.draw.polygon(camera.screen, self.color, screenVertices)