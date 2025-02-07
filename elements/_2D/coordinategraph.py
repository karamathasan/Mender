from element import Element2D
from physics.transform import Transform2D
import numpy as np
import pygame
import pyopencl as cl
import types

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
        self.plots = []
        self.vectors = []
        self.functions = []

        if transform:
            self.transform = transform
        else:
            self.transform = Transform2D()
        pass
    
    def plotPoint(self, point: np.ndarray):
        if not point in self.points:
            self.points.append(point)

    def plotVec(self, start: np.ndarray = np.array([0,0]), end:np.ndarray = None):
        assert end is not None, "Invalid end"
        if not (start, end) in self.vectors:
            self.vectors.append((start, end))

    # def translateFunction(self, function: types.FunctionType):
    #     res = ""
    #     return res

    def plotFunction(self, function: types.FunctionType):
        print(type(function))
        self.functions.append(function)

    def drawFunctionGPU(self, function: str):
        # self.screen = screen
        # self.pxarray = pygame.surfarray.array3d(screen) #indexed in the same way the zbuffer is
        # self.pxarray = np.array(self.pxarray, np.int32(0))

        # platform = cl.get_platforms()[0]
        # device = platform.get_devices()[0]

        # self.ctx = cl.Context([device])
        # self.queue = cl.CommandQueue(self.ctx)

        # mf = cl.mem_flags
        # self.pxarray_g = cl.Buffer(self.ctx, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=self.pxarray)
        
        # self.prg = cl.Program(self.ctx, """
        # __kernel void plotFunc(
        #         __global__ float *pxarray_g,
        #         float xmin,
        #         float xmax,
        #         int width, 
        #         int height)
        #     {
        #         float y = """ + function + """;
        #     } 
        # """ ).build()
        # for all x present in screen, graph the corresponding y
        # str is expected to in the form:
        
        # "2 * x", "2 ** x", "x * x + 2 * x + 2"
        pass

    def drawSatisfaction(self, assertion):
        pass

    def drawFunctions(self, camera):
        for function in self.functions:
            # overlay = np.zeros(shape=camera.get_size())
            leftBound = int(camera.Vec2Screen(np.array([-self.dimensions[0],0]) + self.transform.position).x)
            rightBound = int(camera.Vec2Screen(np.array([self.dimensions[0],0]) + self.transform.position).x)
            # upperBound = int(camera.Vec2Screen(np.array([0, self.dimensions[1]]) + self.transform.position).y)
            # lowerBound = int(camera.Vec2Screen(np.array([0, self.dimensions[1]]) + self.transform.position).y)
            print(leftBound)
            print(rightBound)
            for xPix in range(leftBound,rightBound):
                x = camera.Screen2Vec(pygame.Vector2(xPix,0))[0]
                y = function(x) 
                yPix = int(camera.Vec2Screen(np.array([x,y])).y)
                # yPix = min(yPix, upperBound)
                # yPix = max(yPix, lowerBound)
                camera.screen.set_at((xPix,yPix),(255,255,255))
                print(xPix, yPix)

    def draw(self, camera):
        rotmat = np.array(
            [[np.cos(self.transform.orientation), -np.sin(self.transform.orientation)],
             [np.sin(self.transform.orientation), np.cos(self.transform.orientation)]]
        )

        # def global2local(vec: np.ndarray):
        #     res = rotmat @ vec
        #     res += self.transform.position
        #     return camera.Vec2Screen(res)

        def local2global(vec: np.ndarray):
            vec = np.array([vec[0] / self.scale[0], vec[1] / self.scale[1]])
            res = rotmat @ vec
            res += self.transform.position
            return camera.Vec2Screen(res)
        
        def drawVector(start = np.array([0,0]), end = None):
            assert end is not None, "End invalid"
            vecAngle = np.arctan2((end[1]-start[1]),(end[0]-start[0])) 
            leftDiagonal = (-0.5,0.2)
            rightDiagonal = (-0.5,-0.2)
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

        for point in self.points:
            position = local2global(point)
            pygame.draw.circle(camera.screen, "white", position, 3)

        for vec in self.vectors:
            drawVector(*vec)

        self.drawFunctions(camera)
        