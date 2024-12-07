import pygame
import numpy as np
from physics.transform import Transform2D, Transform3D

class Camera():
    def __init__(self, screen):
        pass

    def render(self, element):
        element.draw(self)

    def Vec2Screen(self, coordinate, screen):
        pass
    
class Camera2D(Camera):
    '''
    Create a generic 2D camera for 2D scenes.
    
    Parameters:
        screen:  Pygame surface, the screen were the camera will output to
        camera_width: the width of the camera in meters (its viewport width is equal to this amount)
        aspect_ratio: the ratio between the width and the height (16/9 by default)
        transform: the Transform2D associated with the camera in worldspace 
    '''
    def __init__(self, screen, camera_width = 30, aspect_ratio: float = 16/9, transform: Transform2D = None):
        self.screen = screen
        self.width = camera_width
        self.aspect = aspect_ratio

        if transform is None:
            self.transform = Transform2D(np.array([0,0]),0)
        else:
            self.transform = transform

    def Vec2Screen(self, vec: np.ndarray):
        assert vec.shape == (2,)
        # 1280 x 720
        size = self.screen.get_size()
        pygX = size[0]/2 + self.toScreenSpace(vec[0])
        pygY = size[1]/2 - self.toScreenSpace(vec[1])
        return pygame.Vector2(pygX,pygY)
    
    def toScreenSpace(self, length: float):
        """
        converts a length from the worldspace coordinate system to the screenspace
        """
        return int(length * self.screen.get_size()[0] / self.width)

class Camera3D(Camera):
    def __init__(self, screen, transform: Transform3D = None, near_clip = 0.1, far_clip = 100):
        self.screen = screen
        if transform is None:
            self.transform = Transform3D(np.array([0,0,0]),np.array([0,1,0]))
        self.transform = transform

# may divide this further into a ray marching and ray tracing camera
class Perspective3D(Camera3D):
    def __init__(self, screen, near_clip = 0.1, far_clip = 100, fov = 54, aspect_ratio: float = 16/9, transform: Transform3D = None):
        self.screen = screen
        self.fov = fov
        self.aspect = aspect_ratio
        
        if transform is None:
            self.transform = Transform3D(np.array([0,0,0]),np.array([0,1,0]))
        self.transform = transform

        # the distance to the plane of projection (the screen) to the location of the camera
        self.projectionDist = self.screen.get_size()[0]/np.tan(fov/2)

    def Vec2Screen(self, coordinate):
        # 1280 x 720
        size = self.screen.get_size()
        pygX = size[0]/2 + coordinate[0]
        pygY = size[1]/2 - coordinate[1]
        return pygame.Vector2(pygX,pygY)

class Orthographic3D(Camera3D):
    def __init__(self, screen, camera_width = 30, aspect_ratio: float = 16/9,transform: Transform3D = None, near_clip = 0.1, far_clip = 100):
        self.screen = screen
        self.width = camera_width
        self.aspect = aspect_ratio

        if transform is None:
            self.transform = Transform3D()
        else: 
            self.transform = transform

    def Vec2Screen(self, vec: np.ndarray):
        assert vec.shape == (3,)
        # 1280 x 720
        size = self.screen.get_size()
        pygX = size[0]/2 + self.toScreenSpace(vec[0])
        pygY = size[1]/2 - self.toScreenSpace(vec[1])
        return pygame.Vector2(pygX,pygY)
    
    def toScreenSpace(self, length: float):
        """
        converts a length from the worldspace coordinate system to the screenspace
        """
        return int(length * self.screen.get_size()[0] / self.width)