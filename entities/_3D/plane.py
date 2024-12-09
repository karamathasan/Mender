from physics.transform import Transform3D
from physics.dynamics import Dynamics3D
from physics.entity import Entity3D
from rendering.quaternion import Quaternion
from rendering.edge import Edge3D

import numpy as np
import pygame 

class Plane3D(Entity3D):
    def __init__(self, size = 10, color = "white", mass = 10, transform:Transform3D = Transform3D([0,-5,0]), dynamics = None, gravity_enabled=False):
        super().__init__(mass, transform, dynamics, gravity_enabled)

        self.size = size
        self.normal = np.array([0,1,0])
        self.color = color

    def draw(self, camera):
        # very laggy
        for i in range(self.size):
            for j in range(self.size):
                pygame.draw.circle(camera.screen, self.color, camera.Vec2Screen(self.transform.position + np.array([10 * (i - self.size/2), 0,10 * j])), 1)
