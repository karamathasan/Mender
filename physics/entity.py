from element import Element, Element2D, Element3D
from physics.transform import Transform, Transform2D, Transform3D
from physics.dynamics import Dynamics, Dynamics2D, Dynamics3D
from physics.collider import Collider, Collider2D, Collider3D
from physics.force import Force2D, Force3D
from physics.torque import Torque3D
from physics.constraints.constraint import Constraint2D, Constraint3D

from physics.constraints.gravity import Gravity2D, Gravity3D


# an entity is an object affected by physics 
# entities hold constraints to the rules of physics that can be applied to them
#   for example, they may be immovable in some directions, or they may not be able to rotate
# entities in a sense, are rigidbodies

# parent type
class Entity(Element):
    def __init__(self, transform: Transform = None, dynamics: Dynamics = None, collider: Collider = None):
        self.transform = None
        self.dynamics = None
        self.collider = None
        self.mass = None
        pass
    
    def draw():
        pass

    def addForce():
        pass

    def update(self, transform, dynamics):
        pass

    def applyConstraint(self,constraint):
        pass

class Entity2D(Entity, Element2D):
    def __init__(self, mass: float = 10.0, transform: Transform2D = None, dynamics: Dynamics2D = None, collider: Collider2D = None, gravity_enabled = True):
        self.mass = mass if mass is not None else 10.0
        self.transform = transform if transform is not None else Transform2D()
        self.dynamics = dynamics if dynamics is not None else Dynamics2D(self)
        self.collider = collider if collider is not None else Collider2D(self, self.vertices)

        if gravity_enabled:
            self.applyConstraint(Gravity2D())

    def addForce(self, force: Force2D):
        self.dynamics.addForce(force)

    def update(self, mass: float = 10.0, transform: Transform2D = None, dynamics: Dynamics2D = None):
        self.mass = mass if mass is not None else 10.0
        if transform is None:
            self.transform = Transform2D()
        else: self.transform = transform
        if dynamics is None:
            self.dynamics = Dynamics2D(self)
        else: self.dynamics = dynamics

    def applyConstraint(self, constraint: Constraint2D):
        constraint.visit(self)

class Entity3D(Entity, Element3D):
    def __init__(self, mass: float = 10.0, transform: Transform3D = None, dynamics: Dynamics3D = None, collider: Collider3D = None, gravity_enabled = True):
        self.mass = mass if mass is not None else 10.0
        self.transform = transform if transform is not None else Transform3D()
        self.dynamics = dynamics if dynamics is not None else Dynamics3D(self)
        self.collider = collider if collider is not None else Collider3D(self, self.vertices)

        if gravity_enabled:
            self.applyConstraint(Gravity3D())

    def addForce(self, force: Force3D):
        self.dynamics.addForce(force)
    
    def addTorque(self, torque: Torque3D):
        self.dynamics.addTorque(torque)

    def update(self, transform: Transform3D = None, dynamics: Dynamics3D = None):
        if transform is not None:
            self.transform = transform
        if dynamics is not None:
            self.dynamics = dynamics
    
    def applyConstraint(self, constraint: Constraint3D):
        constraint.visit(self)