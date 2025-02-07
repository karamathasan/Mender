from element import Element2D
from elements.text import Text
from physics.transform import Transform2D
import numpy as np
import pygame

class Node(Element2D):
    def __init__(self, content, *connections, transform: Transform2D):
        self.connections = connections
        self.transform = transform if transform else Transform2D()
        self.content = Text(content, np.ndarray(2), self.transform)

        self.start = Transform2D(transform.position + np.array([0,1]))
        self.end = Transform2D(transform.position + np.array([0,-1]))

    def draw(self, camera):
        origin = camera.Vec2Screen(self.transform.position)
        pygame.draw.circle(camera.screen, "white", origin, camera.toScreen(1))
        Text.draw(camera)

        # draw connection to children
        # for connection in connection:
            

        