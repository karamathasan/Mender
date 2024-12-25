from abc import ABC
import numpy as np
import pygame 
from physics.transform import Transform2D, Transform3D
from animation.animation import Animation

# animations should have end conditions that can be checked through the use of a lambda
# or another kind of observer
# an animation sequence can have multiple end behaviors

class AnimationGroup(Animation):
    pass

class SequentialGroup(AnimationGroup):
    pass

class DeadlineGroup(AnimationGroup):
    pass

class RaceGroup(AnimationGroup):
    pass

class ParallelGroup(AnimationGroup):
    pass
