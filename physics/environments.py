from scene import Scene, Scene2D, Scene3D
from entities._2D.pointmass import PointMass
from physics.transform import Transform2D, Transform3D
from physics.spatialtree import SpatialTree, QuadTree, OctTree
from physics.solver import Solver, ExplicitEuclid2D, ExplicitEuclidSpatial2D, ExplicitEuclid3D
from abc import ABC

from rendering.noise import PerlinNoise
from element import Element2D, Element3D
from camera import Camera2D, Camera3D

import numpy as np

class Environment(Scene):
    pass

class Environment2D(Scene2D):
    pass

class Environment3D(Scene3D):
    pass

class ManyBodyEnvironment2D(Environment2D):
    def __init__(self, bodies:int, screen, camera: Camera2D = None, fps = 60):
        
        self.elements = []

        x_noise = PerlinNoise(32,256)
        y_noise = PerlinNoise(32,256)

        for i in range(bodies):
            r = np.random.uniform(0,1,(2,))
            v = 5 * np.array([x_noise.sample(r),y_noise.sample(r)])
            t = Transform2D(15 * (r-0.5))
            p = PointMass(transform=t)
            p.dynamics.set(v)
            self.elements.append(p)

        self.fps = fps
        if camera is None:
            self.camera = Camera2D(screen)
        else:
            self.camera = camera

        self.solver = ExplicitEuclidSpatial2D()
        self.solver.initEntities(self.elements)
            # print(self.solver.entities)
        
    def add(self, *args: Element2D):
        self.elements.extend(args)
        self.solver.initEntities(self.elements)

    def render(self):
        self.solver.tree.draw(self.camera)
        return super().render()

    