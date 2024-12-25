from abc import ABC
import numpy as np
import pygame 
from physics.transform import Transform2D, Transform3D

class Animation(ABC):
    def __init__(self):
        pass

    def visit(self, element):
        pass
