from element import Element2D
from physics.transform import Transform2D
from elements._2D.coordinategraphelement import CoordinateVector2D, SatisfactionGraph2D, FunctionGraph2D

import pyopencl as cl
import types
import numpy as np
import pygame

class CartesianGraph2D(Element2D):
    def __init__(self, dimensions:tuple = None, scale:tuple = None, transform:Transform2D = None):
        # if the dimensions are none, then they will span the remainder of the camera
        # dimensions are lengths in world space
        # the scale of the dimensions will fit scale * dimension ticks
        self.dimensions = dimensions
        if scale:
            self.scale = scale
        else:
            self.scale = (1,1)

        self.points = []
        # self.plots = []
        # self.vectors = []
        # self.functions = []
        # self.satisfactions = []

        self.graphElements = []

        if transform:
            self.transform = transform
        else:
            self.transform = Transform2D()
        pass
    
    def plotPoint(self, point: np.ndarray):
        if not point in self.points:
            self.points.append(point)

    def plotVec(self, tip, tail: np.ndarray = np.array([0,0])):
        vecG = CoordinateVector2D(self, tip, tail)
        self.graphElements.append(vecG)
        # if not (start, end) in self.vectors:
            # self.vectors.append((start, end))

    #TODO: create function caching/sleeping
    #if the function definition does not change with time, then cache the produced image rather than recalculate
    def plotFunction(self, function: types.FunctionType):
        # self.functions.append(function)
        functionG = FunctionGraph2D(self, function)
        self.graphElements.append(functionG)

    def plotSatisfaction(self, satisfaction):
        """
        Include points (x,y) that satisfy the function passed
        Parameters:
            satisfaction: lambda x,y -> bool
        """
        # self.satisfactions.append(satisfaction)
        satisfactionG = SatisfactionGraph2D(self, satisfaction)
        self.graphElements.append(satisfactionG)


    #TODO: all drawings of must consider the graph's position and orientation
    def draw(self, camera):
        rotmat = np.array(
            [[np.cos(self.transform.orientation), -np.sin(self.transform.orientation)],
             [np.sin(self.transform.orientation), np.cos(self.transform.orientation)]]
        )

        def local2global(vec: np.ndarray):
            vec = np.array([vec[0] / self.scale[0], vec[1] / self.scale[1]])
            res = rotmat @ vec
            res += self.transform.position
            return camera.Vec2Screen(res)
        
        def drawTicks():
            for i in range(int(self.dimensions[0] * self.scale[0] + 1)):
                upper = camera.Vec2Screen(np.array([i / self.scale[0],0.2]))
                lower = camera.Vec2Screen(np.array([i / self.scale[0],-0.2]))
                pygame.draw.line(camera.screen, "white", upper, lower)

                upper = camera.Vec2Screen(-np.array([i / self.scale[0],0.2]))
                lower = camera.Vec2Screen(-np.array([i / self.scale[0],-0.2]))
                pygame.draw.line(camera.screen, "white", upper, lower)

            for j in range(int(self.dimensions[1] * self.scale[1] + 1)):
                left = camera.Vec2Screen(np.array([0.2, j / self.scale[1]]))
                right = camera.Vec2Screen(np.array([-0.2, j / self.scale[1]]))

                pygame.draw.line(camera.screen, "white", left, right)
                left = camera.Vec2Screen(-np.array([0.2, j / self.scale[1]]))
                right = camera.Vec2Screen(-np.array([-0.2, j / self.scale[1]]))
                pygame.draw.line(camera.screen, "white", left, right)
                
            del left
            del right
            del upper
            del lower
        
        origin = camera.Vec2Screen(self.transform.position)
        # tick marks can be added through finding local coordinates of the graph through its transform

        if not self.dimensions:
            # intentionally longer than needed, may cause issues when moving camera
            xLen = camera.screen.get_size()[0]/2
            yLen = camera.screen.get_size()[1]/2
        else:
            xLen = self.dimensions[0]
            yLen = self.dimensions[1]
            drawTicks()
            
        if origin.x < camera.screen.get_size()[0] and origin.y < camera.screen.get_size()[1]:
            xDir = rotmat @ np.array([1,0]) 
            yDir = rotmat @ np.array([0,1]) 

            right = camera.Vec2Screen(xDir * xLen)
            left = camera.Vec2Screen(-xDir * xLen)
            top = camera.Vec2Screen(yDir * yLen)
            bottom = camera.Vec2Screen(-yDir * yLen)
            pygame.draw.line(camera.screen, "white", origin, right)
            pygame.draw.line(camera.screen, "white", origin, left)
            pygame.draw.line(camera.screen, "white", origin, top)
            pygame.draw.line(camera.screen, "white", origin, bottom)

        # for point in self.points:
        #     position = local2global(point)
        #     pygame.draw.circle(camera.screen, "white", position, 3)

        # for vec in self.vectors:
        #     drawVector(*vec)

        # self.drawFunctions(camera)
        # self.drawSatisfactions(camera,0.1)

        for graphElement in self.graphElements:
            graphElement.draw(camera)
        