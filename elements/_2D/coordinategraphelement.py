from element import Element2D, Element3D
from abc import ABC
import types

import numpy as np
import pygame

import pyopencl as cl


class CoordinateGraphElement2D(Element2D, ABC):
    def __init__(self):
        self.parent = None
        pass
    
    def setParent(self, graph):
        self.parent = graph

class CoordinateVector2D(CoordinateGraphElement2D):
    def __init__(self, parent, tip, tail: np.ndarray = np.array([0,0])):
        assert tip is not None, "Invalid tip"
        self.parent = parent
        self.tip = tip
        self.tail = tail

    #TODO: account for parent graph orientation
    def draw(self, camera):
        rotmat = np.array(
            [[np.cos(self.parent.transform.orientation), -np.sin(self.parent.transform.orientation)],
             [np.sin(self.parent.transform.orientation), np.cos(self.parent.transform.orientation)]]
        )

        def local2global(vec: np.ndarray):
            vec = np.array([vec[0] / self.parent.scale[0], vec[1] / self.parent.scale[1]])
            res = rotmat @ vec
            res += self.parent.transform.position
            return camera.Vec2Screen(res)
        
        vecAngle = np.arctan2((self.tip[1]-self.tail[1]),(self.tip[0]-self.tail[0])) 
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
        leftDiagonal += self.tip
        rightDiagonal += self.tip
        tail = local2global(self.tail)
        tip = local2global(self.tip)
        leftDiagonal = local2global(leftDiagonal)
        rightDiagonal = local2global(rightDiagonal)
        pygame.draw.line(camera.screen, "white", tail, tip)
        pygame.draw.polygon(camera.screen, "white", (tip, leftDiagonal, rightDiagonal), )

class FunctionGraph2D(CoordinateGraphElement2D):
    def __init__(self, parent, function: types.FunctionType):
        self.parent = parent
        self.function = function
        self.cached = None

    def __call__(self, *args):
        return self.function(*args)
    
    def draw(self, camera):
        self.drawNaive(camera)

    def drawNaive(self, camera):
        if self.cached: #also check if the function and graph are unchanged
            for coordinate in self.cached:
                camera.screen.set_at(coordinate,(255,255,255))
        else:
            cache = []
            leftBound = int(camera.Vec2Screen(np.array([-self.parent.dimensions[0],0]) + self.parent.transform.position).x)
            rightBound = int(camera.Vec2Screen(np.array([self.parent.dimensions[0],0]) + self.parent.transform.position).x)
            upperBound = int(camera.Vec2Screen(np.array([0, self.parent.dimensions[1]]) + self.parent.transform.position).y)
            lowerBound = int(camera.Vec2Screen(np.array([0, -self.parent.dimensions[1]]) + self.parent.transform.position).y)
            for xPix in range(leftBound,rightBound):
                x = camera.Screen2Vec(pygame.Vector2(xPix,0))[0]
                y = self.function(x) 
                yPix = int(camera.Vec2Screen(np.array([x,y])).y)
                if -lowerBound < -yPix < -upperBound:
                    camera.screen.set_at((xPix,yPix),(255,255,255))

                    cache.append((xPix,yPix))
            self.cached = cache

    def drawGPU(self, camera):
        pass

class SatisfactionGraph2D(CoordinateGraphElement2D):
    def __init__(self, parent, satisfaction: types.FunctionType):
        self.parent = parent
        self.satisfaction = satisfaction
        self.cached = None

    def __call__(self, *args):
        return self.function(*args)
    
    def draw(self, camera):
        self.drawNaive(camera)

    def drawNaive(self, camera, density = 1):
        if self.cached:
            for coordinate in self.cached:
                camera.screen.set_at(coordinate,(255,255,255))
        else:
            leftBound = int(camera.Vec2Screen(np.array([-self.parent.dimensions[0],0]) + self.parent.transform.position).x)
            rightBound = int(camera.Vec2Screen(np.array([self.parent.dimensions[0],0]) + self.parent.transform.position).x)
            upperBound = int(camera.Vec2Screen(np.array([0, self.parent.dimensions[1]]) + self.parent.transform.position).y)
            lowerBound = int(camera.Vec2Screen(np.array([0, -self.parent.dimensions[1]]) + self.parent.transform.position).y)
            cache = []
            for xPix in range(leftBound, rightBound):
                for yPix in range(upperBound, lowerBound):
                    if xPix % int(1/density) != 0 or yPix % int(1/density) != 0:
                        continue
                    vec = camera.Screen2Vec(pygame.Vector2(xPix,yPix))
                    if self.satisfaction(vec[0],vec[1]):
                        camera.screen.set_at((xPix,yPix),(255,255,255))
                        cache.append((xPix,yPix))
            self.cached = cache
            
    def drawGPU(self, translation, camera):
        screen = camera.screen
        pxarray = pygame.surfarray.array3d(screen) 
        pxarray = np.array(pxarray, np.int32(0))
        platform = cl.get_platforms()[0]
        device = platform.get_devices()[0]

        # width = np.int32(screen.get_size()[0])
        # height = np.int32(screen.get_size()[1])

        ctx = cl.Context([device])
        queue = cl.CommandQueue(ctx)

        mf = cl.mem_flags
        pxarray_buf = cl.Buffer(ctx, mf.WRITE | mf.COPY_HOST_PTR, hostbuf = pxarray)

        leftBound = int(camera.Vec2Screen(np.array([-self.parent.dimensions[0],0]) + self.parent.transform.position).x)
        rightBound = int(camera.Vec2Screen(np.array([self.parent.dimensions[0],0]) + self.parent.transform.position).x)
        upperBound = int(camera.Vec2Screen(np.array([0, self.parent.dimensions[1]]) + self.parent.transform.position).y)
        lowerBound = int(camera.Vec2Screen(np.array([0, -self.parent.dimensions[1]]) + self.parent.transform.position).y)

        width = rightBound - leftBound + 1
        height = lowerBound - upperBound + 1

        # size = self.screen.get_size()
        # vecX = (pix.x - size[0]/2) * self.width / size[0]
        # vecY = (-pix.y + size[1]/2) * self.width / size[0]
        # return np.array([vecX,vecY])

        prg = cl.Program(ctx,"""
        __kernel void draw(
            __global int *pxarray,
            const int screenWidth,
            const int screenHeight,
            const int cameraWidth,
            const int xmin,
            const int ymin)
            {
                int gidx = get_global_id(0);
                int gidy = get_global_id(1);
                int pxidx = 3 * (ymin + gidy) + height * (xmin + gidx);
                
                int vecx = (gidx - screenWidth/2) * cameraWidth / screenWidth;
                int vecy = (-gidy + screenHeight/2) * cameraWidth / screenWidth;
                
                if ("""+ translation +"""){
                    pxarray[pxidx] = 255;
                    pxarray[pxidx] = 255;
                    pxarray[pxidx] = 255;
                }
            }
        """).build()

        knl = prg.draw
        knl(queue, (width,height), None, pxarray_buf)

        cl.enqueue_copy(queue, pxarray, pxarray_buf) 


        # print(upperBound < lowerBound)
        # for xPix in range(leftBound, rightBound):
        #     for yPix in range(upperBound, lowerBound):
        #         vec = camera.Screen2Vec(pygame.Vector2(xPix,yPix))
        #         if self.satisfaction(vec[0],vec[1]):
        #             camera.screen.set_at((xPix,yPix),(255,255,255))

class CoordinateGraphElement3D(Element3D, ABC):
    def __init__(self):
        pass

class CoordinateVector3D(CoordinateGraphElement3D):
    def __init__(self):
        pass

class FunctionGraph3D(CoordinateGraphElement3D):
    def __init__(self):
        super().__init__()

class SatisfactionGraph3D(CoordinateGraphElement3D):
    def __init__(self):
        super().__init__()