import numpy as np
import pygame
import heapq
from abc import ABC
# from camera import Camera2D, Camera3D
from rendering.face import Face, Triangle
from rendering.rendertask import RenderTask
"""
the renderer class is meant to interpret the vertex data that the camera took 
and then arrange it in away that allows the faces to be drawn in order
i think in the future it might also be useful for adding in lighting here, 
but maybe the camera should handle that instead
"""

class Renderer(ABC):
    pass

class Renderer3D(Renderer):
    def __init__(self, camera): # may not need camera 
        self.camera = camera
        self.zbuffer = np.full(self.camera.screen.get_size(),np.inf) #not transposed on purpose
        self.pxarray = camera.pxarray

    # def rasterize(self, task: RenderTask):
    #   #   rasterize with bresenham and scanline algorithms
    #     xmax, ymax, xmin, ymin = self.bound(task.points)
    #     a,b,c = task.points
    #     lowest = min(task.points, key=lambda p: p[1])
        


    def clearBuffer(self):
        self.zbuffer.fill(np.inf) 

    def rasterize(self, task: RenderTask):
        xmax, ymax, xmin, ymin = self.bound(task.points)
        for x in range(xmax-xmin):
            for y in range(ymax-ymin):
                pointDepth = self.inTriangle((xmin + x,ymin + y),task)
                if pointDepth < self.zbuffer[xmin + x,ymin + y]:
                    self.zbuffer[xmin + x, ymin + y] = pointDepth
                    self.pxarray[xmin + x, ymin + y] = task.color
                
    def inTriangle(self, coordinate:tuple, task:RenderTask):
        px,py = coordinate
        a,b,c = task.points
        px -= a.x
        py -= a.y
        depth_a, depth_b, depth_c = task.depths
        u = b-a
        v = c-a
        det = (u.x * v.y - v.x * u.y)
        if det != 0:
            w1 = (px*v.y - py*v.x)/det
            w2 = (-px*u.y + py*u.x)/det
        else:
            return np.inf
        if w1 + w2 > 1 or w1 < 0 or w2 < 0:
            # for some reason, this should be negative inf
            return np.inf
        else:
            return depth_a + w1*(depth_b-depth_a) + w2*(depth_c-depth_a)

    def bound(self, points: tuple):
        xmax = -np.inf
        ymax = -np.inf
        xmin = np.inf
        ymin = np.inf
        for point in points:
            xmax = max(point.x,xmax)
            ymax = max(point.y,ymax)
        for point in points:
            xmin = min(point.x,xmin)
            ymin = min(point.y,ymin)
        xmax = int(xmax)
        ymax = int(ymax)
        xmin = int(xmin)
        ymin = int(ymin)
        return (xmax, ymax, xmin, ymin)
    
    def bresenham(a:tuple, b:tuple):
        """
        Bresenham's Line Algorithm for rasterizing a line between two points.

        """
        points = []

        # Calculate differences and steps
        ax,ay = a
        bx,by = b
        dx = abs(bx - ax)
        dy = abs(by - ay)
        sx = 1 if ax < bx else -1  # Step direction for x
        sy = 1 if ay < by else -1  # Step direction for y

        # Initial decision variable
        if dx > dy:
            err = dx / 2.0
        else:
            err = dy / 2.0

        while True:
            points.append((ax, ay))  # Append the current point

            if ax == bx and ay == by:  # End condition
                break
            # Store error term and adjust coordinates
            if dx > dy:
                err -= dy
                if err < 0:
                    ay += sy
                    err += dx
                ax += sx
            else:
                err -= dx
                if err < 0:
                    ax += sx
                    err += dy
                ay += sy

        return points

class Painter3D(Renderer):
    """
    A renderer that uses Painter's Algorithim to draw faces
    """
    def __init__(self, camera):
        self.faceheap = []
        self.camera = camera
        heapq.heapify(self.faceheap)

    def addTask(self, renderTasks:list[RenderTask]):
        if renderTasks:
            for task in renderTasks:
                if task:
                    heapq.heappush(self.faceheap, task)

    def drawFaces(self):
        for i in range(len(self.faceheap)):
            task = heapq.heappop(self.faceheap)
            a,b,c = task.points
            pygame.draw.polygon(self.camera.screen, color=task.color, points=[a,b,c])
            

