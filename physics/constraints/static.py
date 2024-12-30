import numpy as np 
from constraints.constraint import Constraint2D, Constraint3D
from physics.transform import Transform, Transform2D, Transform3D


class Static2D(Constraint2D):
    def __init__(self):
        pass

    def accept(self, entity):
        # should make it so that the entity can never move, and collisions are fully elastic
        pass

class Static3D(Constraint3D):
    pass