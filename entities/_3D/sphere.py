from physics.transform import Transform3D
from physics.dynamics import Dynamics3D
from physics.entity import Entity3D
from rendering.quaternion import Quaternion
from rendering.edge import Edge3D

import numpy as np
import pygame 

class Sphere3D(Entity3D):
    def __init__(self, radius = 0.5, color = "white", mass = 10, transform:Transform3D = Transform3D([0,-5,0]), dynamics = None, gravity_enabled=False):
        super().__init__(mass, transform, dynamics, gravity_enabled)

        self.radius = radius
        self.normal = np.array([0,1,0])
        self.color = color

        self.vertices = []
        linlat = 10 
        linlon = 10
        for lat in range(linlat + 1):
            lat_angle = np.pi * (lat / linlat)
            for lon in range(linlon + 1):
                lon_angle = 2 * np.pi * (lon / linlon)
                self.vertices.append(np.array([
                    radius * np.sin(lat_angle) * np.cos(lon_angle),
                    radius * np.sin(lat_angle) * np.sin(lon_angle),
                    radius * np.cos(lat_angle)
                ]))    


    def draw(self, camera):
        for vertex in self.vertices:
            vertex = (self.transform.orientation * Quaternion.Vec2Quaternion(vertex) * self.transform.orientation.conjugate()).toVec()
            if camera.Vec2Screen(vertex) is not None:
                pygame.draw.circle(camera.screen, self.color, camera.Vec2Screen(vertex), 1)