import numpy as np
import pygame
import heapq
from abc import ABC
# from camera import Camera2D, Camera3D
from rendering.face import Face, Triangle
from rendering.rendertask import RenderTask

import time
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
        self.zbuffer = np.full(self.screen.get_size(),np.finfo(np.float32).max) # not transposed on purpose
        self.pxarray = pygame.surfarray.array3d(screen) # indexed in the same way the zbuffer is
        self.pxarray = np.array(self.pxarray, np.int32(0))

        platform = cl.get_platforms()[0]
        device = platform.get_devices()[0]

        self.ctx = cl.Context([device])
        self.queue = cl.CommandQueue(self.ctx)

        mf = cl.mem_flags
        self.zbuffer_g = cl.Buffer(self.ctx, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=self.zbuffer)
        self.pxarray_g = cl.Buffer(self.ctx, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=self.pxarray)
        self.prg = cl.Program(self.ctx, """
        __kernel void rasterize(
                __global float *zbuffer_g,
                __global int *pxarray_g, 
                __global int *a_g,
                __global int *b_g,
                __global int *c_g,
                __global const float *depths,
                int r, int g, int b,
                int xmin,
                int ymin,
                int height,
                int width,
                int maxDepth)
            {
                int gidx = get_global_id(0);
                int gidy = get_global_id(1);
                int depthidx = (ymin + gidy) + height * (xmin + gidx);
                int pxidx = 3*depthidx;
                            
                float depth_a = depths[0];
                float depth_b = depths[1];
                float depth_c = depths[2];
                int det = ((b_g[0]-a_g[0]) * (c_g[1]-a_g[1]) - (c_g[0]-a_g[0]) * (b_g[1]-a_g[1]));
                float w1 = 0.0;
                float w2 = 0.0;
                
                int px = (xmin + gidx - a_g[0]);
                int py = ymin + gidy - a_g[1];
                        
                float pointDepth = maxDepth;
                if (det != 0)
                {
                    w1 = (float)(px * (c_g[1]-a_g[1]) - py * (c_g[0]-a_g[0]))/det;
                    w2 = (float)(-px * (b_g[1]-a_g[1]) + py * (b_g[0]-a_g[0]))/det;
                }
                else {return;}
                
                if (w1 + w2 > 1.0 || w1 < 0. || w2 < 0.)
                {
                    return;
                }          
                pointDepth = depth_a + w1*(depth_b - depth_a) + w2*(depth_c - depth_a);        
                            
                if (pointDepth < zbuffer_g[depthidx])
                {
                    if (pxidx < height * width * 3)
                    {
                        zbuffer_g[depthidx] = pointDepth;
                        pxarray_g[pxidx] = r;
                        pxarray_g[pxidx + 1] = g;
                        pxarray_g[pxidx + 2] = b;
                    }
                }
            } 
        """ ).build()

    def clear(self):
        self.zbuffer.fill(np.finfo(np.float32).max) 
        self.pxarray.fill(0)

        cl.enqueue_copy(self.queue, self.zbuffer_g, self.zbuffer)
        cl.enqueue_copy(self.queue, self.pxarray_g, self.pxarray)

    def updatePixels(self):
        # potential for conflicts due to blit overwrite
        pygame.surfarray.blit_array(self.screen, self.pxarray)         
    
    def rasterizeGPU(self, tasks: list[RenderTask]): 
        for task in tasks:
            xmax, ymax, xmin, ymin = self.bound(task.points)
            points, depths, color = task.toTuple()
            width = xmax - xmin + 1
            height = ymax - ymin + 1

            r,g,b = color

            r = np.int32(r)
            g = np.int32(g)
            b = np.int32(b) 

            mf = cl.mem_flags
            a_g = cl.Buffer(self.ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=np.array([points[0].x, points[0].y], dtype=np.int32))
            b_g = cl.Buffer(self.ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=np.array([points[1].x, points[1].y], dtype=np.int32))
            c_g = cl.Buffer(self.ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=np.array([points[2].x, points[2].y], dtype=np.int32))
            depths_g = cl.Buffer(self.ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=np.array(depths, dtype=np.float32))
            knl = self.prg.rasterize  
            knl(self.queue, (width, height), None, 
                self.zbuffer_g,
                self.pxarray_g,
                a_g, 
                b_g, 
                c_g, 
                depths_g, 
                r,g,b, 
                np.int32(xmin), 
                np.int32(ymin), 
                np.int32(self.pxarray.shape[1]),
                np.int32(self.pxarray.shape[0]),
                np.finfo(np.float32).max 
            )
        cl.enqueue_copy(self.queue, self.pxarray, self.pxarray_g)
        cl.enqueue_copy(self.queue, self.zbuffer, self.zbuffer_g)

    def rasterizeCPU(self, task: RenderTask):
        xmax, ymax, xmin, ymin = self.bound(task.points)
        for x in range(xmax-xmin+1):
            for y in range(ymax-ymin+1):
                pointDepth = self.inTriangle((xmin + x,ymin + y),task)
                if pointDepth < self.zbuffer[xmin + x,ymin + y] and pointDepth != np.finfo(np.float32).max:
                    self.zbuffer[xmin + x, ymin + y] = pointDepth
                    self.pxarray[xmin + x, ymin + y] = task.color
                    # self.pxarray[xmin + x, ymin + y] = [255,255,255]

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
        if w1 + w2 > 1 or w1 < 0 or w2 < 0:
            return np.finfo(np.float32).max
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

    def addTasks(self, renderTasks:list[RenderTask]):
        if renderTasks:
            for task in renderTasks:
                if task:
                    heapq.heappush(self.faceheap, task)

    def drawFaces(self):
        for i in range(len(self.faceheap)):
            task = heapq.heappop(self.faceheap)
            a,b,c = task.points
            pygame.draw.polygon(self.screen, color=task.color, points=[a,b,c])

class DoubleBufferRenderer3D(Renderer3D):
    def __init__(self, screen):
        self.screen = screen
        self.zbuffer_fronthost = np.full(self.screen.get_size(),np.finfo(np.float32).max) # not transposed on purpose
        self.zbuffer_backhost = np.full(self.screen.get_size(),np.finfo(np.float32).max) # not transposed on purpose
        
        self.pxarray_fronthost = pygame.surfarray.array3d(screen) # indexed in the same way the zbuffer is
        self.pxarray_fronthost = np.array(self.pxarray, np.int32(0))
        
        self.pxarray_backhost = pygame.surfarray.array3d(screen) # indexed in the same way the zbuffer is
        self.pxarray_backhost = np.array(self.pxarray, np.int32(0))

        platform = cl.get_platforms()[0]
        device = platform.get_devices()[0]

        self.ctx = cl.Context([device])
        self.queue = cl.CommandQueue(self.ctx)

        mf = cl.mem_flags
        self.zbuffer_frontbuf = cl.Buffer(self.ctx, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=self.zbuffer)
        self.zbuffer_backbuf = cl.Buffer(self.ctx, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=self.zbuffer)
        self.pxarray_frontbuf = cl.Buffer(self.ctx, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=self.pxarray)
        self.pxarray_backbuf = cl.Buffer(self.ctx, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=self.pxarray)
        self.prg = cl.Program(self.ctx, """
        __kernel void rasterize(
                __global float *zbuffer_g,
                __global int *pxarray_g, 
                __global int *a_g,
                __global int *b_g,
                __global int *c_g,
                __global const float *depths,
                int r, int g, int b,
                int xmin,
                int ymin,
                int height,
                int width,
                int maxDepth)
            {
                int gidx = get_global_id(0);
                int gidy = get_global_id(1);
                int depthidx = (ymin + gidy) + height * (xmin + gidx);
                int pxidx = 3*depthidx;
                            
                float depth_a = depths[0];
                float depth_b = depths[1];
                float depth_c = depths[2];
                int det = ((b_g[0]-a_g[0]) * (c_g[1]-a_g[1]) - (c_g[0]-a_g[0]) * (b_g[1]-a_g[1]));
                float w1 = 0.0;
                float w2 = 0.0;
                
                int px = (xmin + gidx - a_g[0]);
                int py = ymin + gidy - a_g[1];
                        
                float pointDepth = maxDepth;
                if (det != 0)
                {
                    w1 = (float)(px * (c_g[1]-a_g[1]) - py * (c_g[0]-a_g[0]))/det;
                    w2 = (float)(-px * (b_g[1]-a_g[1]) + py * (b_g[0]-a_g[0]))/det;
                }
                else {return;}
                
                if (w1 + w2 > 1.0 || w1 < 0. || w2 < 0.)
                {
                    return;
                }          
                pointDepth = depth_a + w1*(depth_b - depth_a) + w2*(depth_c - depth_a);        
                            
                if (pointDepth < zbuffer_g[depthidx])
                {
                    if (pxidx < height * width * 3)
                    {
                        zbuffer_g[depthidx] = pointDepth;
                        pxarray_g[pxidx] = r;
                        pxarray_g[pxidx + 1] = g;
                        pxarray_g[pxidx + 2] = b;
                    }
                }
            } 
        """ ).build()

    def rasterizeGPU(self, tasks: list[RenderTask]): 
        for task in tasks:
            xmax, ymax, xmin, ymin = self.bound(task.points)
            points, depths, color = task.toTuple()
            width = xmax - xmin + 1
            height = ymax - ymin + 1

            r,g,b = color

            r = np.int32(r)
            g = np.int32(g)
            b = np.int32(b) 

            mf = cl.mem_flags
            a_g = cl.Buffer(self.ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=np.array([points[0].x, points[0].y], dtype=np.int32))
            b_g = cl.Buffer(self.ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=np.array([points[1].x, points[1].y], dtype=np.int32))
            c_g = cl.Buffer(self.ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=np.array([points[2].x, points[2].y], dtype=np.int32))
            depths_g = cl.Buffer(self.ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=np.array(depths, dtype=np.float32))
            knl = self.prg.rasterize  
            knl(self.queue, (width, height), None, 
                self.zbuffer_frontbuf,
                self.pxarray_frontbuf,
                a_g, 
                b_g, 
                c_g, 
                depths_g, 
                r,g,b, 
                np.int32(xmin), 
                np.int32(ymin), 
                np.int32(self.pxarray_frontbuf.shape[1]),
                np.int32(self.pxarray_frontbuf.shape[0]),
                np.finfo(np.float32).max 
            )
        cl.enqueue_copy(self.queue, self.pxarray_frontbuf, self.pxarray_frontbuf, wait_for=False)
        cl.enqueue_copy(self.queue, self.zbuffer_frontbuf, self.zbuffer_frontbuf, wait_for=False)

        self.pxarray_frontbuf, self.pxarray_backbuf = self.pxarray_backbuf, self.pxarray_frontbuf
        self.zbuffer_frontbuf, self.zbuffer_backbuf = self.zbuffer_backbuf, self.zbuffer_frontbuf

        self.zbuffer_fronthost, self.zbuffer_backhost = self.zbuffer_backhost, self.zbuffer_fronthost
        self.pxarray_fronthost, self.pxarray_backhost = self.pxarray_backhost, self.pxarray_fronthost

    def clear(self):
        self.zbuffer.fill(np.finfo(np.float32).max) 
        self.pxarray.fill(0)

        cl.enqueue_copy(self.queue, self.zbuffer_frontbuf, self.zbuffer)
        cl.enqueue_copy(self.queue, self.zbuffer_backbuf, self.zbuffer)
        cl.enqueue_copy(self.queue, self.pxarray_frontbuf, self.pxarray)
        cl.enqueue_copy(self.queue, self.pxarray_backbuf, self.pxarray)

    def mergeBuffers(self):
        self.pxarray = np.minimum(self.pxarray_fronthost,self.pxarray_backhost)
        
             