from element import Element, Element2D, Element3D
from physics.transform import Transform, Transform2D, Transform3D
from physics.dynamics import Dynamics, Dynamics2D, Dynamics3D

# an entity is an object affected by physics 
# entities hold constraints to the rules of physics that can be applied to them
#   for example, they may be immovable in some directions, or they may not be able to rotate
# entities in a sense, are rigidbodies

# parent type
class Entity(Element):
    def __init__(self, transform: Transform = None, dynamics: Dynamics = None):
        pass
    
    def draw():
        pass

    def update(self, transform, dynamics):
        pass

class Entity2D(Entity, Element2D):
    def __init__(self, transform: Transform2D = None, dynamics: Dynamics2D = None):
        if transform is None:
            self.transform = Transform2D()
        else: self.transform = transform
        if dynamics is None:
            self.dynamics = Dynamics2D()
        else: self.dynamics = dynamics

    def draw():
        pass

    def update(self, transform: Transform2D = None, dynamics: Dynamics2D = None):
        if transform is None:
            self.transform = Transform2D()
        else: self.transform = transform
        if dynamics is None:
            self.dynamics = Dynamics2D()
        else: self.dynamics = dynamics


class Entity3D(Entity, Element3D):
    def __init__(self, transform: Transform3D = None, dynamics: Dynamics3D = None):
        if transform is None:
            self.transform = Transform3D()
        else: self.transform = transform
        if dynamics is None:
            self.dynamics = Dynamics3D()
        else: self.dynamics = dynamics

    def draw():
        pass

    def update(self, transform: Transform2D = None, dynamics: Dynamics2D = None):
        if transform is not None:
            self.transform = transform
        if dynamics is not None:
            self.dynamics = dynamics