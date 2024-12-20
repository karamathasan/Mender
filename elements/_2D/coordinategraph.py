from element import Element2D
from physics.transform import Transform2D
import numpy as np
import pygame
# import pyopencl

class CartesianGraph2D(Element2D):
    def __init__(self, dimensions:tuple = None, scale:tuple = None, transform:Transform2D = None):
        # if the dimensions are none, then they will span the remainder of the camera
        self.dimensions = dimensions
        self.scale = scale

        self.points = []
        self.plots = []
        self.functions = []

        if transform:
            self.transform = transform
        else:
            self.transform = Transform2D()
        pass
    
    def plotPoint(self, point: np.ndarray):
        self.points.append(point)

    def plotVec(self, start, end):
        pass

    def plotFunction(self, assertion):
        pass

    def draw(self, camera):
        def local2global(vec: np.ndarray):
            res = vec + np.array([
                -np.cos(self.transform.orientation),
                np.sin(self.transform.orientation)
            ])
            res += self.transform.position
            return res
        def drawVector(start, end):
            # local coordinates
            pass
        origin = camera.Vec2Screen(self.transform.position)
        # tick marks can be added through finding local coordinates of the graph through its transform

        if origin.x < camera.screen.get_size()[0] and origin.y < camera.screen.get_size()[1]:
            if not self.dimensions: 
                left = pygame.Vector2((0,origin.y + (camera.screen.get_size()[0] - origin.x) * np.sin(self.transform.orientation)))
                right = pygame.Vector2((camera.screen.get_size()[0],origin.y + (origin.x - camera.screen.get_size()[0]) * np.sin(self.transform.orientation) ))
                top = pygame.Vector2((origin.x - origin.y * np.sin(self.transform.orientation),0))
                bottom = pygame.Vector2(origin.x + origin.y * np.sin(self.transform.orientation),(camera.screen.get_size()[1]))
                pygame.draw.line(camera.screen, "white", left, right)
                pygame.draw.line(camera.screen, "white", top, bottom)
            else:
                left = pygame.Vector2((0,origin.y + (camera.screen.get_size()[0] - origin.x) * np.sin(self.transform.orientation)))
                right = pygame.Vector2((camera.screen.get_size()[0],origin.y + (origin.x - camera.screen.get_size()[0]) * np.sin(self.transform.orientation) ))
                top = pygame.Vector2((origin.x - origin.y * np.sin(self.transform.orientation),0))
                bottom = pygame.Vector2(origin.x + origin.y * np.sin(self.transform.orientation),(camera.screen.get_size()[1]))
                pygame.draw.line(camera.screen, "white", left, right)
                pygame.draw.line(camera.screen, "white", top, bottom)

    