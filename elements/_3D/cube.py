import pygame
import numpy as np
from element import Element3D
from physics.transform import Transform3D
from rendering.edge import Edge3D
from rendering.quaternion import Quaternion

class Cube(Element3D):

    def __init__(self, size, color = "white", transform: Transform3D = None):
        '''
        Parameters:
            size: the side length of the cube
            transform: the cube's transform, which includes its orientation and position
        '''
        self.size = size
        if transform is None:
            self.transform = Transform3D()
        else: self.transform = transform
        self.color = color

        # needs to account for orientation
        s = size * np.sqrt(2)/2
        self.vertices = [
            np.array([-s,-s,-s]), # 0
            np.array([s,-s,-s]), # 1

            np.array([s,s,-s]), # 2
            np.array([-s,s,-s]), # 3

            np.array([-s,-s,s]), # 4
            np.array([s,-s,s]), # 5

            np.array([s,s,s]), # 6
            np.array([-s,s,s]), # 7
        ]

        self.edges=[
            Edge3D(self.vertices[0],self.vertices[1]),
            Edge3D(self.vertices[0],self.vertices[4]),
            Edge3D(self.vertices[0],self.vertices[3]),
            Edge3D(self.vertices[1],self.vertices[5]),
            Edge3D(self.vertices[1],self.vertices[2]),
            Edge3D(self.vertices[4],self.vertices[5]),
            Edge3D(self.vertices[4],self.vertices[7]),
            Edge3D(self.vertices[3],self.vertices[7]),
            Edge3D(self.vertices[3],self.vertices[2]),
            Edge3D(self.vertices[5],self.vertices[6]),
            Edge3D(self.vertices[2],self.vertices[6]),
            Edge3D(self.vertices[7],self.vertices[6]),
        ]


    def draw(self, camera):
        screenVertices = [self.transform.orientation * Quaternion.Vec2Quaternion(self.transform.position + vertex) * self.transform.orientation.conjugate() for vertex in self.vertices]
        screenVertices = [camera.Vec2Screen(vertex.toVec()) for vertex in screenVertices]

        pygame.draw.aaline(camera.screen, self.color, screenVertices[0], screenVertices[1])
        pygame.draw.aaline(camera.screen, self.color, screenVertices[0], screenVertices[3])
        pygame.draw.aaline(camera.screen, self.color, screenVertices[0], screenVertices[4])
        pygame.draw.aaline(camera.screen, self.color, screenVertices[1], screenVertices[2])
        pygame.draw.aaline(camera.screen, self.color, screenVertices[1], screenVertices[5])

        pygame.draw.aaline(camera.screen, self.color, screenVertices[2], screenVertices[3])
        pygame.draw.aaline(camera.screen, self.color, screenVertices[2], screenVertices[6])

        pygame.draw.aaline(camera.screen, self.color, screenVertices[3], screenVertices[7])
        pygame.draw.aaline(camera.screen, self.color, screenVertices[4], screenVertices[5])
        pygame.draw.aaline(camera.screen, self.color, screenVertices[4], screenVertices[7])
        pygame.draw.aaline(camera.screen, self.color, screenVertices[5], screenVertices[6])
        pygame.draw.aaline(camera.screen, self.color, screenVertices[6], screenVertices[7])

        pygame.draw.circle(camera.screen, self.color, camera.Vec2Screen(self.transform.position), 1)
