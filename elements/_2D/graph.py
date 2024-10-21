import pygame
import numpy
from element import Element2D
from physics.transform import Transform2D

class Graph(Element2D):
    def __init__(self):
        '''
        Paramaters:
            
        '''
        pass

    def draw(self, camera):
        # the graph lines should span infinitely, but drawing and redrawing this might be useless
        # that is an optimization for later
        # the 2 axes can be drawn simply with some lines
        # the difficult part is the equally spaced graph lines and 
        pass