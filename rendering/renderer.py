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
    def __init__(self, camera):
        pass
    def rasterize(self, tri: Triangle):
        pass

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
            

