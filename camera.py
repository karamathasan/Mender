import pygame
import numpy as np
from physics.transform import Transform2D, Transform3D
from rendering.quaternion import Quaternion
from abc import ABC

class Camera(ABC):
    def __init__(self, screen: pygame.Surface, width):
        self.screen = screen
        self.width = width
        pass

    def render(self, element):
        element.draw(self)

    def Vec2Screen(self, coordinate: np.ndarray) -> pygame.Vector2:
        pass

    def toScreenSpace(self, length: float):
        """
        converts a length from the worldspace coordinate system to the screenspace length
        """
        return int(length * self.screen.get_size()[0] / self.width)
    
class Camera2D(Camera):
    '''
    Create a generic 2D camera for 2D scenes.
    
    Parameters:
        screen:  Pygame surface, the screen were the camera will output to
        camera_width: the width of the camera in meters (its viewport width is equal to this amount)
        aspect_ratio: the ratio between the width and the height (16/9 by default)
        transform: the Transform2D associated with the camera in worldspace 
    '''
    def __init__(self, screen: pygame.Surface, camera_width = 30, aspect_ratio: float = 16/9, transform: Transform2D = None):
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
    def __init__(self, screen: pygame.Surface, transform: Transform3D = None, near_clip = 0.1, far_clip = 100):
        self.screen = screen
        if transform is None:
            self.transform = Transform3D()
        self.transform = transform

        self.direction = np.array([0,0,1],dtype=np.float64)
        
    def getGlobalDirection(self):
        direction = (self.transform.orientation * Quaternion.Vec2Quaternion(self.direction) * self.transform.orientation.conjugate()).toVec()
        return direction / np.linalg.norm(direction)

class Perspective3D(Camera3D):
    """
    Creates a camera with perspective
    """
    def __init__(self, screen:pygame.Surface, near_clip = 0.01, far_clip = 100, fov = 54, aspect_ratio: float = 16/9, transform: Transform3D = None):
        self.screen = screen
        self.fov = fov
        self.aspect = aspect_ratio
        self.near_clip = near_clip
        self.far_clip = far_clip
        self.width = 2 * np.tan(fov/2) * self.near_clip
        
        if transform is None:
            # by default
            self.transform = Transform3D(np.array([0,0,-5]))
        else:   
            self.transform = transform

        # the distance to the plane of projection (the screen) to the location of the camera
        self.direction = np.array([0,0,1],dtype=np.float64)

    def toScreenSpace(self, length: float):
        """
        converts a length from the worldspace coordinate system to the screenspace
        """
        return int(length * self.screen.get_size()[0] / self.width)
    
    def Vec2Screen(self, vec):
        v = vec - self.transform.position
        u = self.getGlobalDirection()


        v = (self.transform.orientation * Quaternion.Vec2Quaternion(v) * self.transform.orientation.conjugate()).toVec()
     
        if not (self.near_clip < np.linalg.norm(u * np.dot(u,v) / np.dot(u,u)) < self.far_clip):
            return
        if (np.dot(u,v/np.linalg.norm(v)) < np.cos(self.fov/2) ):
            return 
       
        v = self.near_clip * (-v / np.dot(u,v)) - u * self.near_clip

        size = self.screen.get_size()
        pygX = size[0]/2 + self.toScreenSpace(v[0])
        pygY = size[1]/2 - self.toScreenSpace(v[1])

        return pygame.Vector2(pygX,pygY)

class Orthographic3D(Camera3D):
    def __init__(self, screen: pygame.Surface, camera_width = 30, aspect_ratio: float = 16/9, transform: Transform3D = None, near_clip = 0.1, far_clip = 100):
        self.screen = screen
        self.width = camera_width
        self.aspect = aspect_ratio

        if transform is None:
            # by default
            self.transform = Transform3D(np.array([0,0,-5]))
        else:   
            self.transform = transform

        self.direction = np.array([0,0,1],dtype=np.float64)


    def Vec2Screen(self, vec: np.ndarray):
        assert vec.shape == (3,)
        # vec has to be infront of the viewing plane
        v = vec - self.transform.position
        u = self.getGlobalDirection()

        if np.dot(v,u) <= 0:
            return
        vec = (self.transform.orientation * Quaternion.Vec2Quaternion(vec) * self.transform.orientation.conjugate()).toVec()


        size = self.screen.get_size()
        pygX = size[0]/2 + self.toScreenSpace(vec[0])
        pygY = size[1]/2 - self.toScreenSpace(vec[1])
        return pygame.Vector2(pygX,pygY)
    
    def toScreenSpace(self, length: float):
        """
        converts a length from the worldspace coordinate system to the screenspace
        """
        return int(length * self.screen.get_size()[0] / self.width)