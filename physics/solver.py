from abc import ABC
import numpy as np
from physics.entity import Entity, Entity2D, Entity3D
from rendering.quaternion import Quaternion

class Solver(ABC):
    def __init__(self, fps):
        self.fps = fps
        self.deltaTime = 1/fps

class ExplicitEuclid2D(Solver):
    def __init__(self, fps):
        super().__init__(fps)
    
    def solve(self, entity: Entity2D):
        # constraints will visit the solver to provide or edit calculations
        dyn = entity.dynamics
        transform = entity.transform
        v = dyn.velocity
        a = entity.dynamics.netAcceleration()

        v += a * self.deltaTime
        transform.shift(v * self.deltaTime)

class ExplicitEuclid3D(Solver):
    def __init__(self, fps):
        super().__init__(fps)
    
    def solve(self, entity: Entity3D):
        # constraints will visit the solver to provide or edit calculations
        dyn = entity.dynamics
        transform = entity.transform
        v = dyn.velocity
        a = entity.dynamics.netAcceleration()

        angv = dyn.angular_velocity
        anga = dyn.angular_acceleration

        v += a * self.deltaTime
        angv += anga * self.deltaTime

        transform.shift(v * self.deltaTime)
        if np.linalg.norm(angv) > np.finfo(float).eps:
            # print()
            transform.rotate(np.linalg.norm(angv) * self.deltaTime, angv/np.linalg.norm(angv))
        # transform.rotate(0.1,np.array([1,0,0]))