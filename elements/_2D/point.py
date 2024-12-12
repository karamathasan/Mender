from element import Element2D
from physics.transform import Transform2D

import pygame
import numpy as np

from camera import Camera2D

class Point2D(Element2D):
    '''
    Create a Point element that can be also be used for triangulation

    Parameters:
        radius: the radius of the point
        color: the color of the point
        transform: the Transform2D that will be associated with this point
    '''
    def __init__(self, color = "white", transform:Transform2D = None):
        self.color = color
        if transform:
            self.transform = transform
        else:
            self.transform = Transform2D()

    def draw(self, camera: Camera2D):
        originScreen = camera.Vec2Screen(self.transform.position)
        pxRad = 2
        pygame.draw.circle(camera.screen, self.color, originScreen, pxRad)