from abc import ABC
import numpy as np
from physics.entity import Entity, Entity2D, Entity3D
from rendering.quaternion import Quaternion

class Solver(ABC):
    def __init__(self):
        pass

class ExplicitEuclid2D(Solver):
    def __init__(self):
        # super().__init__(fps)
        pass
    
    def solve(self, entity: Entity2D, dt):
        # constraints will visit the solver to provide or edit calculations
        dyn = entity.dynamics
        transform = entity.transform
        v = dyn.velocity
        a = entity.dynamics.netAcceleration()

        v += a * dt
        transform.shift(v * dt)

class ExplicitEuclid3D(Solver):
    def __init__(self):
        # super().__init__(fps)
        pass
    
    def solve(self, entity: Entity3D, dt: float):
        # constraints will visit the solver to provide or edit calculations
        dyn = entity.dynamics
        transform = entity.transform
        v = dyn.velocity
        a = entity.dynamics.netAcceleration()

        angv = dyn.angular_velocity
        anga = dyn.angular_acceleration

        v += a * dt
        angv += anga * dt

        transform.shift(v * dt)
        if np.linalg.norm(angv) > np.finfo(float).eps:
            # print()
            transform.rotate(np.linalg.norm(angv) * dt, angv/np.linalg.norm(angv))
        # transform.rotate(0.1,np.array([1,0,0]))