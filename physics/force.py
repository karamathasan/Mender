import numpy as np
from abc import ABC
class Force(ABC):
    def __init__():
        pass

class Force2D(Force):
    def __init__(self, direction: np.ndarray, duration = None):
        if duration is None:
            self.forceMode = "momentary"
        else:
            self.forceMode = "impulse"
        assert(direction.shape == (2,))
        self.direction = direction

class Force3D(Force):
    def __init__(self, direction: np.ndarray, duration = None):
        if duration is None:
            self.forceMode = "momentary"
        else:
            self.forceMode = "impulse"
        assert(direction.shape == (3,))
        self.direction = direction
