import pygame
import numpy as np
# from transform import Transform2D
from transform import Transform2D

class Camera():
    def __init__(self, screen):
        pass
    def render(self,element):
        pass
    def ToScreen(self, coordinate, screen):
        pass
    
class Camera2D(Camera):
    def __init__(self, screen, transform = None):
        self.screen = screen
        if transform is None:
            self.transform = Transform2D(np.array([0,0]),0)
        self.transform = transform

    def render(self, element):
        element.draw(self)

    def ToScreen(self, coordinate):
        # 1280 x 720
        size = self.screen.get_size()
        pygX = size[0]/2 + coordinate[0]
        pygY = size[1]/2 - coordinate[1]
        return pygame.Vector2(pygX,pygY)

class Camera3D(Camera):
    def __init__(self, screen):
        pass
    def render(self, element):
        pass