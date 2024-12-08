from abc import ABC
from physics.force import Force, Force2D, Force3D
import numpy as np


class Torque(ABC):
    def __init__(self):
        self.magnitude: float = None
        self.axis: float = None

    def vec2Torque():
        pass

    def toVec(self):
        return self.magnitude * self.axis
    
    def __add__(self, other):
        return self.fromVec(self.toVec() + other.toVec())
    
    def __iadd__(self, other):
        return self.__add__(other)
    
    def __mul__(self, other: float):
        out = self.axis * self.magnitude * other
        return self.vec2Torque(out)
    
    def __imul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other: float ):
        out = self.axis * self.magnitude / other
        return self.vec2Torque(out)
    
    def __idiv__(self, other):
        return self.__div__(other)
    
class Torque3D(Torque):
    '''
    Create a 3D torque vector
    
    Parameters:
        magnitude: the magnitude of the torque
        axis: the axis of the torque. The axis will be normalized and then stored
    '''
    def __init__(self, magnitude: float, axis: np.ndarray, duration: float = None):
        assert magnitude is not None
        assert axis is not None
        assert axis.shape == (3,)
        self.magnitude = magnitude
        self.axis = axis / np.linalg.norm(axis)

        if duration is None: #duration is still not fully implemented. see force.py
            self.duration = np.inf
        else:
            self.duration = duration

    def toAngularAcceleration(self, inertia: float):
        return self.axis * self.magnitude /inertia

    @staticmethod
    def vec2Torque(vec: np.ndarray):
        '''
        Create a torque given only a vector

        Parameters:
            vec: the torque vector. The magnitude of the vector will be the magnitude of the torque, the normalized vector will be treated as the axis of the torque
        '''
        return Torque3D(np.linalg.norm(vec), vec/np.linalg.norm(vec))
    
    @staticmethod
    def force2Torque(force: Force3D, radius: float):
        '''
        Create a torque given a force and a radius

        Parameters:
            force: the force being applied on the entity
            radius: the distance to the center of mass of the entity
        '''
        vec = np.cross(radius,force.toVec())
        return Torque3D(vec)
    
    @staticmethod
    def zero():
        return Torque3D(0, np.array([1,0,0]))
    
