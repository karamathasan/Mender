from abc import ABC
import numpy as np
import pygame 
from physics.transform import Transform2D, Transform3D

class Animation(ABC):
    def __init__(self):
        pass

    def visit(self, element):
        pass
# meant to be a visitor class for different elements. 
# each element would accept an Animation object that would be applied to the object in time
class LinearShift(Animation):
    def __init__(self, end: np.ndarray, duration):
        self.end = end
        self.duration = duration

    def visit(self, element):
        pass

class QuadraticShift(Animation):
    def __init__(self,):
        pass
