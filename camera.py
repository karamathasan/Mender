import pygame
import numpy as np
from physics.transform import Transform2D, Transform3D
from rendering.quaternion import Quaternion
from rendering.renderer import Painter3D, Renderer3D
from abc import ABC

import time

class Camera(ABC):
    def __init__(self, screen: pygame.Surface, width, aspect_ratio = 16/9):
        self.screen = screen
        self.width = width
        self.pxarray = pygame.PixelArray(screen)
        self.aspect = aspect_ratio
        pass

    def render(self, element):
        element.draw(self)

    def Screen2Vec(self, pix: pygame.Vector2) -> np.ndarray:
        pass

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
        width: the width of the camera in meters (its viewport width is equal to this amount)
        aspect_ratio: the ratio between the width and the height (16/9 by default)
        transform: the Transform2D associated with the camera in worldspace 
    '''
    def __init__(self, screen: pygame.Surface, width = 30, aspect_ratio: float = 16/9, transform: Transform2D = None):
        super().__init__(screen, width, aspect_ratio)

        if transform is None:
            self.transform = Transform2D(np.array([0,0]),0)
        else:
            self.transform = transform

    def Screen2Vec(self, pix):
        size = self.screen.get_size()
        vecX = (pix.x - size[0]/2) * self.width / size[0]
        vecY = (-pix.y + size[1]/2) * self.width / size[0]
        return np.array([vecX,vecY])

    def Vec2Screen(self, vec: np.ndarray):
        # TODO: account for camera orientation
        assert vec.shape == (2,)
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
    def __init__(self, screen: pygame.Surface, width: float, aspect_ratio: float = 16/9 ,transform: Transform3D = None, near_clip:float = 0.1, far_clip:float = 100, focal_dist:float = 5):
        super().__init__(screen,width,aspect_ratio)
        self.focal_dist = focal_dist

        if transform is None:
            self.transform = Transform3D([0,0,self.focal_dist])
        else:
            self.transform = transform

        self.near_clip = near_clip
        self.far_clip = far_clip

        self.direction = np.array([0,0,-1],dtype=np.float64)
        self.painter = Painter3D(self.screen)
        self.renderer = Renderer3D(self.screen)

    def Vec2Screen(self, vec: np.ndarray):
        assert vec.shape == (3,)
        v = vec - self.transform.position
        u = self.direction
        v = (self.transform.orientation.conjugate() * Quaternion.Vec2Quaternion(v) * self.transform.orientation).toVec()
        if np.dot(v,u) <= 0:            
            return
        v = v - u * np.dot(u,v) / np.dot(u,u)

        size = self.screen.get_size()
        pygX = size[0]/2 + self.toScreenSpace(v[0])
        pygY = size[1]/2 - self.toScreenSpace(v[1])
        return pygame.Vector2(pygX,pygY)
        
    def getGlobalDirection(self):
        direction = (self.transform.orientation * Quaternion.Vec2Quaternion(self.direction) * self.transform.orientation.conjugate()).toVec()
        return direction / np.linalg.norm(direction)
    
    def paint(self, elements):
        for element in elements:
            tasks = element.draw(self)
            self.painter.addTasks(tasks)
        self.painter.drawFaces()
        # self.painter

    def render(self, elements):    
        self.renderer.clearPixels()
        tasks = []
        for element in elements:
            for task in element.draw(self):
                if np.dot(task.normal, self.getGlobalDirection()) > 0:
                    tasks.append(task)
        self.renderer.clear()

        # self.renderer.rasterizeCPU(tasks)
        self.renderer.rasterizeGPU(tasks)
        self.renderer.updatePixels()

    def getDepth(self, vec):
        v = vec - self.transform.position
        v = (self.transform.orientation.conjugate() * Quaternion.Vec2Quaternion(v) * self.transform.orientation).toVec()
        depth = -v[2]
        return depth

class Perspective3D(Camera3D):
    """
    Creates a camera with perspective
    """
    def __init__(self, screen:pygame.Surface, aspect_ratio: float = 16/9, near_clip: float = 0.01, far_clip: float = 100, fov = 100, transform: Transform3D = None):
        super().__init__(screen, 2 * np.tan(np.deg2rad(fov/2)) * near_clip, aspect_ratio, transform, near_clip, far_clip)
        self.fov = fov
    
    def Vec2Screen(self, vec):
        v = vec - self.transform.position
        u = self.direction
        v = (self.transform.orientation.conjugate() * Quaternion.Vec2Quaternion(v) * self.transform.orientation).toVec()

        if not (self.focal_dist + self.near_clip < np.linalg.norm(v) < self.focal_dist + self.far_clip):
            return
        
        v = self.near_clip * (v / np.dot(u,v)) - u * self.near_clip

        size = self.screen.get_size()
        pygX = size[0]/2 + self.toScreenSpace(v[0])
        pygY = size[1]/2 - self.toScreenSpace(v[1]) # TODO: should account for aspect ratio
        if not (0 <= pygX < size[0]):
            return 
        if not (0 <= pygY < size[1]):
            return 
        return pygame.Vector2(pygX,pygY)

class Orthographic3D(Camera3D):
    def __init__(self, screen: pygame.Surface, width = 30, aspect_ratio: float = 16/9, transform: Transform3D = None, near_clip = 0.1, far_clip = 100):
        super().__init__(screen, width, aspect_ratio, transform, near_clip, far_clip)

    def Vec2Screen(self, vec: np.ndarray):
        assert vec.shape == (3,)
        v = vec - self.transform.position
        u = self.direction
        v = (self.transform.orientation.conjugate() * Quaternion.Vec2Quaternion(v) * self.transform.orientation).toVec()
        if np.dot(v,u) <= 0:
            return
        v = v - u * np.dot(u,v) / np.dot(u,u)

        size = self.screen.get_size()
        pygX = size[0]/2 + self.toScreenSpace(v[0])
        pygY = size[1]/2 - self.toScreenSpace(v[1])
        return pygame.Vector2(pygX,pygY)
    
    def toScreenSpace(self, length: float):
        """
        converts a length from the plane space coordinate system to the screenspace
        """
        return int(length * self.screen.get_size()[0] / self.width)
    
    