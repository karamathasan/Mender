import numpy as np
from abc import ABC

from physics.force import Force2D, Force3D

class Dynamics(ABC):
    def __init__(self):
        self.velocity = None
        self.acceleration = None
        self.forces = {}
        self.parent = None

    def addForce(self, force):
        pass

    def netForce(self):
        sum = 0
        for force in self.forces.keys():
            sum += force
        return sum
        
    def netAcceleration(self) -> float:
        fn = self.netForce()
        return fn.toAcceleration(self.parent.mass)

class Dynamics2D(Dynamics):
    def __init__(self, parent ,velocity: np.ndarray = None, acceleration: np.ndarray = None):
        assert parent
        self.parent = parent
        if velocity is None:
            self.velocity = np.array([0.0,0.0])
        else: 
            assert(velocity.shape == (2,))
            self.velocity = np.float64(velocity)
        if acceleration is None:
            self.acceleration = np.array([0.0,0.0])
        else: 
            assert(acceleration.shape == (2,))
            self.acceleration = np.float64(acceleration)
        self.forces = {}

    def set(self, velocity: np.ndarray = None, acceleration: np.ndarray = None):
        if velocity is not None:
            assert(velocity.shape == (2,))
            self.velocity = np.float64(velocity)
        if acceleration is not None:
            assert(acceleration.shape == (2,))
            self.acceleration = np.float64(acceleration)

    def addForce(self, force: Force2D):
        if force.forceMode == "impulse":
            self.forces[force] = force.duration
        else:
            self.forces[force] = np.inf

    def netForce(self):
        sum = Force2D.zero()
        for force in self.forces.keys():
            sum += force
        return sum

class Dynamics3D(Dynamics):
    def __init__(self, parent, velocity: np.ndarray = None, acceleration: np.ndarray = None):
        assert parent
        self.parent = parent
        if velocity is None:
            self.velocity = np.array([0.0,0.0,0.0])
        else:
            assert(velocity.shape == (3,))
            self.velocity = velocity
        if acceleration is None:
            self.acceleration = np.array([0.0,0.0,0.0])
        else: 
            assert(acceleration.shape == (3,))
            self.acceleration = acceleration
        self.forces = {}

    def set(self, velocity: np.ndarray = None, acceleration: np.ndarray = None):
        if velocity is not None:
            assert(velocity.shape == (3,))
            self.velocity = velocity
        if acceleration is not None:
            assert(acceleration.shape == (3,))
            self.acceleration = acceleration
    
    def addForce(self, force: Force3D):
        if force.forceMode == "impulse":
            self.forces[force] = force.duration
        else:
            self.forces[force] = np.inf
