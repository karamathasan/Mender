from physics.transform import Transform3D
from physics.dynamics import Dynamics3D
from physics.entity import Entity3D
from rendering.quaternion import Quaternion
from rendering.face import Triangle

import numpy as np
import pygame 

class Plane3D(Entity3D):
    def __init__(self, size = 10, color = "white", mass = 10, transform:Transform3D = Transform3D([0,-5,0]), dynamics = None, gravity_enabled=False):
        super().__init__(mass, transform, dynamics, gravity_enabled)

        self.size = size
        self.normal = np.array([0,1,0])
        self.color = color

        self.face = Triangle.fromQuad(
            np.array([-size/2,0,size/2]),
            np.array([size/2,0,size/2]),
            np.array([-size/2,0,-size/2]),
            np.array([size/2,0,-size/2]),
            parent=self.transform
        )

    def draw(self, camera):
        tasks = []
        tasks.append(self.face[0].draw(camera))
        tasks.append(self.face[1].draw(camera))
        return tasks
