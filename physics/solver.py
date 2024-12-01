from abc import ABC
import numpy as np
from physics.entity import Entity, Entity2D

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
        print(v)

        transform.shift(v * self.deltaTime)
        v += a * self.deltaTime
        dyn.set(v, a)
