import numpy as np
import pygame
from abc import ABC
# from camera import Camera2D, Camera3D
# from rendering.face import Face, Triangle

class RenderTask():
    def __init__(self, points: tuple, color: tuple, depth: float):
        self.depth = depth
        self.points = points
        self.color = color

    def toTuple(self):
        return (self.depth, self)
    
    def __lt__(self, other):
        return self.depth < other.depth