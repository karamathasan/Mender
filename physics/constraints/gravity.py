from physics.constraints.constraint import Constraint2D, Constraint3D
# from physics.entity import Entity2D, Entity3D
from physics.force import Force2D, Force3D

import numpy as np

class Gravity2D(Constraint2D):
    def __init__(self, acceleration_magnitude = 9.81):
        self.gravity = Force2D(acceleration_magnitude, np.array([0,-1]))

    def accept(self, entity):
        # needs to make sure that there a gravity vector always present on the objects that this is applied to
        entity.addForce(entity.mass * self.gravity)


class Gravity3D(Constraint3D):
    def __init__(self, acceleration_magnitude = 9.81):
        self.gravity = Force3D(acceleration_magnitude, np.array([0,0,-1]))

    def accept(self, entity):
        # needs to make sure that there a gravity vector always present on the objects that this is applied to
        entity.addForce(entity.mass * self.gravity)
