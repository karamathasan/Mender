from abc import ABC
import numpy as np
import pygame 
from physics.transform import Transform2D, Transform3D
from element import Element

# animations should have end conditions that can be checked through the use of a lambda
# or another kind of observer
# an animation sequence can have multiple end behaviors
class Animation(ABC):
    def __init__(self, element):
        self.element = element
        self.is_complete = False

    def init(self):
        """
        Initialize an animation to use new information/variables that may have changed after the previous animations
        """
        pass

    def update(self):
        """
        update the animated element in a frame
        """
        pass