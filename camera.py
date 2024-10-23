import pygame
import numpy as np
from physics.transform import Transform2D, Transform3D

class Camera():
    def __init__(self, screen):
        pass

    def render(self, element):
        element.draw(self)

    def ToScreen(self, coordinate, screen):
        pass
    
class Camera2D(Camera):
    def __init__(self, screen, transform: Transform2D = None):
        self.screen = screen
        if transform is None:
            self.transform = Transform2D(np.array([0,0]),0)
        else:
            self.transform = transform

    def ToScreen(self, coordinate):
        # 1280 x 720
        size = self.screen.get_size()
        pygX = size[0]/2 + coordinate[0]
        pygY = size[1]/2 - coordinate[1]
        return pygame.Vector2(pygX,pygY)

class Camera3D(Camera):
    def __init__(self, screen, transform: Transform3D = None, near_clip = 0.1, far_clip = 100):
        self.screen = screen
        if transform is None:
            self.transform = Transform3D(np.array([0,0,0]),np.array([0,1,0]))
        self.transform = transform

# may divide this further into a ray marching and ray tracing camera
class Perspective3D(Camera3D):
    def __init__(self, screen, transform: Transform3D = None, near_clip = 0.1, far_clip = 100, fov = 54):
        self.screen = screen
        if transform is None:
            self.transform = Transform3D(np.array([0,0,0]),np.array([0,1,0]))
        self.transform = transform

        # the distance to the plane of projection (the screen) to the location of the camera
        self.projectionDist = self.screen.get_size()[0]/np.tan(fov/2)

    def ToScreen(self, coordinate):
        # 1280 x 720
        size = self.screen.get_size()
        pygX = size[0]/2 + coordinate[0]
        pygY = size[1]/2 - coordinate[1]
        return pygame.Vector2(pygX,pygY)

class Orthographic3D(Camera3D):
    def __init__(self, screen, transform: Transform3D = None, near_clip = 0.1, far_clip = 100):
        self.screen = screen
        if transform is None:
            self.transform = Transform3D(np.array([0,0,0]),np.array([0,1,0]))
        else: 
            self.transform = transform

    def ToScreen(self, coordinate):
        # 1280 x 720
        diff = coordinate - self.transform.position 
        dist = np.dot(self.transform.orientation, np.linalg.norm(diff)) 

        projection = coordinate - dist * self.transform.orientation - self.transform.position
        size = self.screen.get_size()
        pygX = size[0]/2 + projection[0]
        pygY = size[1]/2 - projection[1]
        return pygame.Vector2(pygX,pygY)