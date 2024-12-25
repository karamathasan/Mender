from abc import ABC
import numpy as np
import pygame 
from physics.transform import Transform2D, Transform3D
from element import Element2D, Element3D
from animation.animation import Animation

class LinearShift2D(Animation):
    def __init__(self, end: np.ndarray, duration):
        assert end.shape == (2,)
        self.end = end
        self.duration = duration

    def visit(self, element: Element2D):
        pass

class LinearShift3D(Animation):
    def __init__(self, end: np.ndarray, duration):
        assert end.shape == (2,)
        self.end = end
        self.duration = duration

    def visit(self, element: Element3D):
        pass

class QuadraticShift(Animation):
    def __init__(self,):
        pass
