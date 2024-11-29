import numpy as np
from abc import ABC
class Force(ABC):
    def __init__(self):
        self.magnitude = 0.0
        self.direction = np.zeros((1,))
        self.duration = np.inf

    def __add__(self, other):
        out = self.direction * self.magnitude + other.direction * other.magnitude
        return self.vec2Force(out)
    
    def __iadd__(self, other):
        return self.__add__(other)

    def __mul__(self, other):
        out = self.direction * self.magnitude * other
        return self.vec2Force(out)
    
    def __imul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other: float | int):
        out = self.direction * self.magnitude / other
        return self.vec2Force(out)
    
    def __idiv__(self, other):
        return self.__div__(other)
    
    def toVec(self):
        return self.magnitude * self.direction

    def toAcceleration(self, mass: float):
        return self.toVec()/mass

class Force2D(Force):
    def __init__(self, magnitude: float, direction: np.ndarray, duration = None):
        assert magnitude is not None
        assert direction is not None
        self.magnitude = magnitude
        if duration is None:
            self.forceMode = "momentary"
            self.duration = duration # may need some changes
        else:
            self.forceMode = "impulse"
            self.duration = duration
        assert(direction.shape == (2,))
        self.direction = direction/np.linalg.norm(direction)

    def __str__(self):
        return f"Force2D {self.magnitude}N pointing {self.direction}"
    
    def zero():
        return Force2D(0, np.array([1,0]))
    
    @staticmethod
    def vec2Force(vec: np.ndarray):
        return Force2D(np.linalg.norm(vec), vec/np.linalg.norm(vec))

class Force3D(Force):
    def __init__(self, magnitude: float, direction: np.ndarray, duration = None):
        assert magnitude
        self.magnitude = magnitude
        if duration is None:
            self.forceMode = "momentary"
            self.duration = duration # may need some changes
        else:
            self.forceMode = "impulse"
            self.duration = duration # may need some changes
        assert(direction.shape == (3,))
        self.direction = direction

    @staticmethod
    def vec2Force(vec: np.ndarray):
        return Force3D(np.linalg.norm(vec), vec/np.linalg.norm(vec))
