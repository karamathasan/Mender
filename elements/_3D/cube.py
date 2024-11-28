import pygame
import numpy as np
from physics.entity import Entity3D
from physics.transform import Transform3D

class Cube(Entity3D):

    def __init__(self, size, transform: Transform3D = None, color = "white"):
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
        self.vertices = [
            self.transform.position + np.array([size * np.sqrt(2)/2, size * np.sqrt(2)/2, size * np.sqrt(2)/2]), # 0
            self.transform.position + np.array([size * np.sqrt(2)/2, size * np.sqrt(2)/2, size * -np.sqrt(2)/2]), # 1

            self.transform.position + np.array([size * np.sqrt(2)/2, size * -np.sqrt(2)/2, size * np.sqrt(2)/2]), # 2
            self.transform.position + np.array([size * np.sqrt(2)/2, size * -np.sqrt(2)/2, size * -np.sqrt(2)/2]), # 3

            self.transform.position + np.array([size * -np.sqrt(2)/2, size * np.sqrt(2)/2, size * np.sqrt(2)/2]), # 4
            self.transform.position + np.array([size * -np.sqrt(2)/2, size * np.sqrt(2)/2, size * -np.sqrt(2)/2]), # 5

            self.transform.position + np.array([size * -np.sqrt(2)/2, size * -np.sqrt(2)/2, size * np.sqrt(2)/2]), # 6
            self.transform.position + np.array([size * -np.sqrt(2)/2, size * -np.sqrt(2)/2, size * -np.sqrt(2)/2]), # 7
        ]

    def draw(self, camera):
        # draw lines between the correct vertices
        screenVertices = [camera.ToScreen(vertex) for vertex in self.vertices]

        # print(str(screenVertices[4]) + " true: " + str(self.vertices[4]))
        # print(str(screenVertices[2]) + " true: " + str(self.vertices[2]))
        # print(str(screenVertices[0]) + " true: " + str(self.vertices[0]))
        # print("")

        pygame.draw.aaline(camera.screen, self.color, screenVertices[0], screenVertices[1])
        pygame.draw.aaline(camera.screen, self.color, screenVertices[0], screenVertices[2])
        pygame.draw.aaline(camera.screen, self.color, screenVertices[0], screenVertices[4])
        pygame.draw.aaline(camera.screen, self.color, screenVertices[1], screenVertices[3])
        pygame.draw.aaline(camera.screen, self.color, screenVertices[1], screenVertices[5])

        pygame.draw.aaline(camera.screen, self.color, screenVertices[2], screenVertices[3])
        pygame.draw.aaline(camera.screen, self.color, screenVertices[2], screenVertices[6])

        pygame.draw.aaline(camera.screen, self.color, screenVertices[3], screenVertices[7])
        pygame.draw.aaline(camera.screen, self.color, screenVertices[4], screenVertices[5])
        pygame.draw.aaline(camera.screen, self.color, screenVertices[4], screenVertices[6])
        pygame.draw.aaline(camera.screen, self.color, screenVertices[5], screenVertices[7])
        pygame.draw.aaline(camera.screen, self.color, screenVertices[6], screenVertices[7])

        pygame.draw.circle(camera.screen, self.color, camera.ToScreen(np.array([0,0,0])), 1)
        # pygame.draw.aaline(camera.screen, self.color, screenVertices[3], screenVertices[5]) # this line is wrong



        
        pass