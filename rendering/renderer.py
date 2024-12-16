import numpy as np
import pygame
import heapq
from abc import ABC
# from camera import Camera2D, Camera3D
from rendering.face import Face, Triangle
from rendering.rendertask import RenderTask
from multiprocessing import Process
from multiprocessing.shared_memory import SharedMemory

import pyopencl as cl
"""
the renderer class is meant to interpret the vertex data that the camera took 
and then arrange it in away that allows the faces to be drawn in order
i think in the future it might also be useful for adding in lighting here, 
but maybe the camera should handle that instead
"""

class Renderer(ABC):
    pass

class Renderer3D(Renderer):
    def __init__(self, screen):
        self.screen = screen
        # self.zbuffer = np.full(self.screen.get_size(),np.inf) #not transposed on purpose
        self.zbuffer = np.full(self.screen.get_size(),np.finfo(np.float32).max) #not transposed on purpose
        self.pxarray = pygame.surfarray.array3d(screen) #indexed in the same way the zbuffer is
        # self.pxarray = np.full(self.screen.get_size(), np.int32(0))

        print(f"zbuffer: {self.zbuffer.shape}")
        print(f"pxarray: {self.pxarray.shape}")

    def clear(self):
        self.zbuffer.fill(np.inf) 
        self.pxarray.fill(0)

    def updatePixels(self):
        pygame.surfarray.blit_array(self.screen, self.pxarray)         

    def rasterize(self, task: RenderTask):
        xmax, ymax, xmin, ymin = self.bound(task.points)
        for x in range(xmax-xmin+1):
            for y in range(ymax-ymin+1):
                pointDepth = self.inTriangle((xmin + x,ymin + y),task)
                if pointDepth < self.zbuffer[xmin + x,ymin + y] and pointDepth != np.finfo(np.float32).max:
                    self.zbuffer[xmin + x, ymin + y] = pointDepth
                    self.pxarray[xmin + x, ymin + y] = task.color

    # def bresraster(self, task: RenderTask):
    #     # rasterize with bresenham and scanline algorithms
    #     # a is the highest point of the 
    #     xmax, ymax, xmin, ymin = self.bound(task.points)
    #     a = min(task.points, key=lambda p: p[1])
    #     b = min(task.points, key=lambda p: p[0])
    #     c = max(task.points, key=lambda p: p[1])
    #     l1 = self.bresenham(a,b)
    #     l2 = self.bresenham(a,c)

    def rasterizeGPU(self, task: RenderTask):
        xmax, ymax, xmin, ymin = self.bound(task.points)
        points, depths, color = task.toTuple()
        width = xmax - xmin + 1
        height = ymax - ymin + 1

        color = int(pygame.Color(color))
        color = np.int64(color)

        platform = cl.get_platforms()[0]
        device = platform.get_devices()[0]

        ctx = cl.Context([device])
        queue = cl.CommandQueue(ctx)

        mf = cl.mem_flags
        zbuffer_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=self.zbuffer)
        zbuffer_res = cl.Buffer(ctx, mf.WRITE_ONLY, self.zbuffer.nbytes)
        pxarray_res = cl.Buffer(ctx, mf.WRITE_ONLY | mf.COPY_HOST_PTR, hostbuf=self.pxarray)
        a_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=np.array([points[0].x, points[0].y]))
        b_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=np.array([points[1].x, points[1].y]))
        c_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=np.array([points[2].x, points[2].y]))
        depths_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=np.array(depths))

        # prg = cl.Program(ctx, """
        # __kernel void rasterize(
        #         __global float *zbuffer_g,
        #         __global float *zbuffer_res,
        #         __global int *pxarray_res, 
        #         __global const int *a,
        #         __global const int *b,
        #         __global const int *c,
        #         __global const float *depths,
        #         long color,
        #         int xmax, int xmin,
        #         int ymax, int ymin)
        #     {
        #         int gidx = get_global_id(0);
        #         int gidy = get_global_id(1);
        #         // int index = (xmin + gidx) + (ymax - ymin + 1) * (ymin + gidy);
        #         int index = (ymin + gidy) + (xmax - xmin + 1) * (xmin + gidx);
                            
        #         float depth_a = depths[0];
        #         float depth_b = depths[1];
        #         float depth_c = depths[2];
        #         float det = (float)((b[0]-a[0]) * (c[1]-a[1]) - (c[0]-a[0]) * (b[1]-a[1]));
        #         float w1 = 0.0;
        #         float w2 = 0.0;
                
        #         // int px = xmin + gidx - a[0];
        #         int px = ymin + gidy - a[0];
        #         // int py = ymin + gidy - a[1];
        #         int py = xmin + gidx - a[1];
        #         float pointDepth = FLT_MAX;
        #         if (det != 0)
        #         {
        #             w1 = (px * (b[1]-a[1]) - py * (b[0]-a[0]))/det;
        #             w2 = (-px * (c[1]-a[1]) + py * (c[0]-a[0]))/det;
        #         }
        #         if (w1 + w2 <= 1.0 && w1 >= 0.0 && w2 >= 0.0)
        #         {
        #             pointDepth = depth_a + w1*(depth_b - depth_a) + w2*(depth_c - depth_a);
        #         }          
                         
        #         if (pointDepth < zbuffer_g[index])
        #         {
        #             zbuffer_res[index] = pointDepth;
        #             pxarray_res[index] = color;
        #         } 
   
        #     } 
        # """ ).build()

        #         # if (pointDepth < zbuffer_g[index])
        #         # {
        #         #     zbuffer_res[index] = pointDepth;
        #         #     pxarray_res[index] = color;
        #         # }
        #         # else
        #         # {
        #         #     zbuffer_res[index] = pointDepth;
        #         #     pxarray_res[index] = color;
        #         # }

        prg = cl.Program(ctx, """
                __kernel void rasterize(
                        __global float *zbuffer_g,
                        __global float *zbuffer_res,
                        __global long *pxarray_res, 
                        __global const int *a,
                        __global const int *b,
                        __global const int *c,
                        __global const float *depths,
                        long color,
                        int xmax, int xmin,
                        int ymax, int ymin,
                        int width, int height)
                    {
                        int gidx = get_global_id(0);
                        int gidy = get_global_id(1);

                        pxarray_res[gidx] = 4294967295;
                    } 
                """ ).build()


        knl = prg.rasterize  # Use this Kernel object for repeated calls
        knl(queue, (width, height), None, zbuffer_g, zbuffer_res, pxarray_res, a_g, b_g, c_g, depths_g, color, np.int32(xmax), np.int32(xmin), np.int32(ymax), np.int32(ymin), np.int32(self.zbuffer.shape[0]), np.int32(self.zbuffer.shape[1]))

        cl.enqueue_copy(queue, self.pxarray, pxarray_res)
        cl.enqueue_copy(queue, self.zbuffer, zbuffer_res)

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
            return np.finfo(np.float32).max
            # return np.inf
        if w1 + w2 > 1 or w1 < 0 or w2 < 0:
            return np.finfo(np.float32).max
            # return np.inf
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
    def __init__(self, screen):
        self.faceheap = []
        self.screen = screen
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
            pygame.draw.polygon(self.screen, color=task.color, points=[a,b,c])
             