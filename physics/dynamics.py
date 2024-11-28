import numpy as np
from abc import ABC

from physics.force import Force2D, Force3D

class Dynamics(ABC):
    def __init__(self):
        self.velocity = None
        self.acceleration = None
        self.forces = {}

    def addForce(self, force):
        pass

    def netForce(self):
        sum = 0
        for force in self.forces.keys():
            sum += force
        return sum

class Dynamics2D(Dynamics):
    def __init__(self, velocity: np.ndarray = None, acceleration: np.ndarray = None):
        if velocity is None:
            self.velocity = np.array([0.0,0.0])
        else: 
            assert(velocity.shape == (2,))
            self.velocity = velocity
        if acceleration is None:
            self.acceleration = np.array([0.0,0.0])
        else: 
            assert(acceleration.shape == (2,))
            self.acceleration = acceleration
        self.forces = {}

    def set(self, velocity: np.ndarray = None, acceleration: np.ndarray = None):
        assert(velocity.shape == (2,))
        assert(acceleration.shape == (2,))

        if velocity is not None:
            self.velocity = velocity
        if acceleration is not None:
            self.acceleration = acceleration

    def addForce(self, force: Force2D):
        if force.forceMode == "impulse":
            self.forces[force] = force.duration

class Dynamics3D(Dynamics):
    def __init__(self, velocity: np.ndarray = None, acceleration: np.ndarray = None):

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
        assert(velocity.shape == (3,))
        assert(acceleration.shape == (3,))

        if velocity is not None:
            self.velocity = velocity
        if acceleration is not None:
            self.acceleration = acceleration
    
    def addForce(self, force: Force3D):
        if force.forceMode == "impulse":
            self.forces[force] = force.duration
