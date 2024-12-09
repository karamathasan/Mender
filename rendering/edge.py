import numpy as np
from abc import ABC
import pygame
from physics.transform import Transform2D, Transform3D
from rendering.quaternion import Quaternion
from camera import Camera2D, Camera3D

class Edge(ABC):
    def __init__():
        pass

class Edge2D(Edge):
    '''
    Create an edge for 2D object rendering

    Parameters:
        a: position of vertex A
        b: position of vertex B
        parent: the parent transform where vertex A and B live
    '''
    def __init__(self, a:np.ndarray, b: np.ndarray, parent: Transform2D = None):
        assert a.shape == (2,)
        assert b.shape == (2,)

        self.a = np.array(a,dtype=np.float64)
        self.b = np.array(b,dtype=np.float64) 
        if parent is None:
            self.parent = Transform2D
        else:
            self.parent = parent

class Edge3D(Edge):
    '''
    Create an edge for 3D object rendering

    Parameters:
        a: position of vertex A in worldspace
        b: position of vertex B in worldspace
        parent: the parent transform where vertex A and B live
    '''
    def __init__(self, a:np.ndarray, b: np.ndarray, parent: Transform3D = None):
        assert a.shape == (3,)
        assert b.shape == (3,)

        self.a = np.array(a,dtype=np.float64)
        self.b = np.array(b,dtype=np.float64) 
        if parent is None:
            self.parent = Transform3D()
        else:
            self.parent = parent

    def draw(self, camera: Camera3D, color: str = "white"):
            global_a = self.parent.position + (self.parent.orientation * Quaternion.Vec2Quaternion(self.a) * self.parent.orientation.conjugate()).toVec()
            global_b = self.parent.position + (self.parent.orientation * Quaternion.Vec2Quaternion(self.b) * self.parent.orientation.conjugate()).toVec()
            
            screen_a = camera.Vec2Screen(global_a)
            screen_b = camera.Vec2Screen(global_b)

            # if camera.near_clip
            if screen_a is not None and screen_b is not None:
                pygame.draw.aaline(camera.screen, color, screen_a, screen_b)

