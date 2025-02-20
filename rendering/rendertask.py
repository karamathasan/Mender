import numpy as np
import pygame
from abc import ABC
# from camera import Camera2D, Camera3D
# from rendering.face import Face, Triangle

class RenderTask():
    def __init__(self, points: tuple, depths: tuple, color: tuple, normal):
        self.points = points
        self.depths = depths
        self.color = color

        self.normal = normal
        
    def avgDepth(self):
        sum = 0
        for depth in self.depths:
            sum += depth
        return sum/3 
    

    def __lt__(self, other):
        # for max heap implementation
        return self.avgDepth() >= other.avgDepth()
    
    def toTuple(self):
        return (self.points, self.depths, self.color)
    
    def __str__(self):
        return f"RenderTask:\n      points: ({self.points}),\n      depths:   ({self.depths})"