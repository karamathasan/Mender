from element import Element2D
from physics.transform import Transform2D
import numpy as np
import pygame
# import pyopencl

class CoordinateGraph2D(Element2D):
    def __init__(self, scaleX, scaleY, transform:Transform2D):
        self.points = []
        self.plots = []
        self.functions = []
        pass
    
    def plotPoint(point: np.ndarray):
        pass

    def plotVec(start,end):
        pass

    def plotFunction(input: function):
        pass
