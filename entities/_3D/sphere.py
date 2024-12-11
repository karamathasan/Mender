from physics.transform import Transform3D
from physics.dynamics import Dynamics3D
from physics.entity import Entity3D
from rendering.quaternion import Quaternion
from rendering.edge import Edge3D
from rendering.face import Triangle

import numpy as np
import pygame 

class Sphere3D(Entity3D):
    def __init__(self, radius = 0.5, color = "white", mass = 10, transform:Transform3D = Transform3D([0,0,0]), dynamics = None, gravity_enabled=False):
        super().__init__(mass, transform, dynamics, gravity_enabled)

        self.radius = radius
        self.normal = np.array([0,1,0])
        self.color = color

        self.vertices = []
        linlat = 8
        linlon = 8
        for lat in range(linlat + 1):
            lat_angle = np.pi * (lat / linlat)
            for lon in range(linlon + 1):
                lon_angle = 2 * np.pi * (lon / linlon)
                self.vertices.append(np.array([
                    radius * np.sin(lat_angle) * np.cos(lon_angle),
                    radius * np.sin(lat_angle) * np.sin(lon_angle),
                    radius * np.cos(lat_angle)
                ]))    

        self.quads = []
        for i in range(linlat - 1):
            for j in range(linlon):
                # Current index
                current = i * linlon + j
                # Next longitude index (wraps around)
                next_lon = (j + 1) % linlon
                # Indices for the quad
                v1 = current
                v2 = current + linlon
                v3 = current + linlon + next_lon - j
                v4 = current + next_lon - j

                # self.quads.append([self.vertices[v1], self.vertices[v2], self.vertices[v3], self.vertices[v4]])
                self.quads.append(
                    Triangle.fromQuad(self.vertices[v1], self.vertices[v2], self.vertices[v3], self.vertices[v4], parent=self.transform)
                )

    def draw(self, camera):
        for quad in self.quads:
            quad[0].draw(camera)
            quad[1].draw(camera)
        for vertex in self.vertices:
            vertex = (self.transform.orientation * Quaternion.Vec2Quaternion(vertex) * self.transform.orientation.conjugate()).toVec()
            if camera.Vec2Screen(vertex) is not None:
                pygame.draw.circle(camera.screen, "red", camera.Vec2Screen(vertex), 1)
