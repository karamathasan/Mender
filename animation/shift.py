from abc import ABC
import numpy as np
import pygame 
from physics.transform import Transform2D, Transform3D
from element import Element2D, Element3D
from animation.animation import Animation

class LinearShift2D(Animation):
    def __init__(self, element:Element2D, end_pos: np.ndarray, duration):
        assert end_pos.shape == (2,)
        super().__init__(element)
        self.end_pos = end_pos
        self.duration = duration
        self.t = 0

    def init(self):
        self.start = self.element.transform.position

    def update(self, dt):            
        self.t += dt/self.duration
        self.element.transform.position = self.start * (1-self.t) + self.end_pos * self.t
        if self.t >= 1.0:
            self.is_complete = True

class LinearShift3D(Animation):
    def __init__(self, element: Element3D, end_pos: np.ndarray, duration):
        assert end_pos.shape == (3,)
        super().__init__(element)
        self.end_pos = end_pos
        self.duration = duration
        self.t = 0

    def update(self, dt):            
        self.t += dt/self.duration
        self.element.transform.position = self.start * (1-self.t) + self.end_pos * self.t
        if self.t >= 1.0:
            self.is_complete = True

class QuadraticShift2D(Animation):
    def __init__(self, element: Element2D, end_pos: np.ndarray, duration):
        assert end_pos.shape == (2,)
        super().__init__(element)
        self.end_pos = end_pos
        self.duration = duration
        self.t = 0

    def init(self):
        self.start = self.element.transform.position

    def update(self, dt):
        self.t += dt/self.duration
        t = -self.t * (self.t-2)
        self.element.transform.position = self.start * (1-t) + self.end_pos * t
        if self.t >= 1.0:
            self.is_complete = True

class QuadraticShift3D(Animation):
    def __init__(self, element: Element3D, end_pos: np.ndarray, duration):
        assert end_pos.shape == (3,)
        super().__init__(element)
        self.end_pos = end_pos
        self.duration = duration
        self.t = 0

    def init(self):
        self.start = self.element.transform.position

    def update(self, dt):
        self.t += dt/self.duration
        t = -self.t * (self.t-2)
        self.element.transform.position = self.start * (1-t) + self.end_pos * t
        if self.t >= 1.0:
            self.is_complete = True

class CubicShift2D(Animation):
    def __init__(self, element: Element2D, end_pos: np.ndarray, duration):
        assert end_pos.shape == (2,)
        super().__init__(element)
        self.end_pos = end_pos
        self.duration = duration
        self.t = 0

    def init(self):
        self.start = self.element.transform.position

    def update(self, dt):
        self.t += dt/self.duration
        t = self.t*self.t*(3.0-2.0*self.t)
        self.element.transform.position = self.start * (1-t) + self.end_pos * t
        if self.t >= 1.0:
            self.is_complete = True

class CubicShift3D(Animation):
    def __init__(self, element: Element3D, end_pos: np.ndarray, duration):
        assert end_pos.shape == (3,)
        super().__init__(element)
        self.end_pos = end_pos
        self.duration = duration
        self.t = 0

    def init(self):
        self.start = self.element.transform.position

    def update(self, dt):
        self.t += dt/self.duration
        t = self.t*self.t*(3.0-2.0*self.t)
        self.element.transform.position = self.start * (1-t) + self.end_pos * t
        if self.t >= 1.0:
            self.is_complete = True