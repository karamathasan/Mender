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
        self.vectors = []
        self.functions = []

        if transform:
            self.transform = transform
        else:
            self.transform = Transform2D()
        pass
    
    def plotPoint(self, point: np.ndarray):
        self.points.append(point)

    def plotVec(self, start: np.ndarray = np.array([0,0]), end:np.ndarray = None):
        assert end is not None, "Invalid end"
        self.vectors.append((start, end))


    def plotFunction(self, assertion):
        pass

    def draw(self, camera):
        def local2global(vec: np.ndarray):
            res = np.array([
                vec[0] * np.cos(self.transform.orientation) - vec[1] * np.sin(self.transform.orientation),
                vec[0] * np.sin(self.transform.orientation) + vec[1] * np.cos(self.transform.orientation)
            ])
            res += self.transform.position
            return camera.Vec2Screen(res)
        def drawVector(start = np.array([0,0]), end = None):
            assert end is not None, "End invalid"
            vecAngle = np.atan((end[1]-start[1])/(end[0]-start[0]))
            leftDiagonal = (-1,0.2)
            rightDiagonal = (-1,-0.2)
            leftDiagonal = np.array([
                leftDiagonal[0] * np.cos(vecAngle) - leftDiagonal[1] * np.sin(vecAngle),
                leftDiagonal[0] * np.sin(vecAngle) + leftDiagonal[1] * np.cos(vecAngle)
            ])
            rightDiagonal = np.array([
                rightDiagonal[0] * np.cos(vecAngle) - rightDiagonal[1] * np.sin(vecAngle),
                rightDiagonal[0] * np.sin(vecAngle) + rightDiagonal[1] * np.cos(vecAngle)
            ])
            leftDiagonal += end
            rightDiagonal += end
            start = local2global(start)
            end = local2global(end)
            leftDiagonal = local2global(leftDiagonal)
            rightDiagonal = local2global(rightDiagonal)
            pygame.draw.line(camera.screen, "white", start, end)

            pygame.draw.polygon(camera.screen, "white", (end, leftDiagonal, rightDiagonal), )
            # local coordinates
            pass
        origin = camera.Vec2Screen(self.transform.position)
        # tick marks can be added through finding local coordinates of the graph through its transform

        # axes are currently not correctly drawn
        if origin.x < camera.screen.get_size()[0] and origin.y < camera.screen.get_size()[1]:
            if not self.dimensions: 
                left = pygame.Vector2((0,origin.y + (camera.screen.get_size()[0] - origin.x) * np.sin(self.transform.orientation)))
                right = pygame.Vector2((camera.screen.get_size()[0],origin.y + (origin.x - camera.screen.get_size()[0]) * np.sin(self.transform.orientation) ))
                top = pygame.Vector2((origin.x - origin.y * np.sin(self.transform.orientation),0))
                bottom = pygame.Vector2(origin.x + origin.y * np.sin(self.transform.orientation),(camera.screen.get_size()[1]))
                pygame.draw.line(camera.screen, "white", left, right)
                pygame.draw.line(camera.screen, "white", top, bottom)
            else:
                # xAxisLen = 
                left = pygame.Vector2((0,origin.y + (camera.screen.get_size()[0] - origin.x) * np.sin(self.transform.orientation)))
                right = pygame.Vector2((camera.screen.get_size()[0],origin.y + (origin.x - camera.screen.get_size()[0]) * np.sin(self.transform.orientation) ))
                top = pygame.Vector2((origin.x - origin.y * np.sin(self.transform.orientation),0))
                bottom = pygame.Vector2(origin.x + origin.y * np.sin(self.transform.orientation),(camera.screen.get_size()[1]))
                pygame.draw.line(camera.screen, "white", left, right)
                pygame.draw.line(camera.screen, "white", top, bottom)

        for point in self.points:
            position = local2global(point)
            pygame.draw.circle(camera.screen, "white", position, 3)
        for vec in self.vectors:
            drawVector(*vec)
        