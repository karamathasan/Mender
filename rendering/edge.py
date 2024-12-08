import numpy as np
from abc import ABC
import pygame

class Edge(ABC):
    def __init__():
        pass

class Edge2D(Edge):
    '''
    Create an edge for 2D object rendering

    Parameters:
        a: position of vertex A
        b: position of vertex B
    '''
    def __init__(self, a:np.ndarray, b: np.ndarray):
        assert a.shape == (2,)
        assert b.shape == (2,)

        self.vertices = [a,b]

class Edge3D(Edge):
    '''
    Create an edge for 3D object rendering

    Parameters:
        a: position of vertex A in worldspace
        b: position of vertex B in worldspace
    '''
    def __init__(self, a:np.ndarray, b: np.ndarray):
        assert a.shape == (3,)
        assert b.shape == (3,)

        self.vertices = [a,b]