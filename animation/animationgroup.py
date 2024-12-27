from abc import ABC
import numpy as np
import pygame 
from physics.transform import Transform2D, Transform3D
from animation.animation import Animation

# animations should have end conditions that can be checked through the use of a lambda
# or another kind of observer
# an animation sequence can have multiple end behaviors

class AnimationGroup(Animation):
    def __init__(self):
        self.is_complete = False
    pass

class SequentialGroup(AnimationGroup):
    def __init__(self, *animations):
        self.animations = list(animations)
        self.current: Animation = None
        self.is_complete = False

    def update(self, dt: float):
        if not self.current:
            self.current = self.animations.pop(0)
            self.current.init()
        if self.current.is_complete:
            if len(self.animations) == 0:
                self.is_complete = True
            else: 
                self.current = self.animations.pop(0)
                self.current.init()
        self.current.update(dt)


class DeadlineGroup(AnimationGroup):
    def __init__(self, deadline:Animation, *followers:Animation):   
        self.deadline = deadline
        self.animations: list[Animation] = [deadline]
        for anim in followers:
            self.animations.append(anim)
        self.is_complete = False

    def init(self):
        for animation in self.animations:
            animation.init()

    def update(self, dt: float):
        if self.deadline.is_complete:
            self.is_complete = True
        for animation in self.animations:
            if not animation.is_complete:
                animation.update(dt) 
    
class RaceGroup(AnimationGroup):
    def __init__(self, *animations: Animation):
        self.animations = list(animations)
        self.is_complete = False

    def init(self):
        for animation in self.animations:
            animation.init()

    def update(self, dt: float):
        for animation in self.animations:
            self.is_complete = self.is_complete or animation.is_complete
            if not animation.is_complete:
                animation.update(dt) 

class ParallelGroup(AnimationGroup):
    def __init__(self, *animations: Animation):
        self.animations = list(animations)
        self.is_complete = False

    def init(self):
        for animation in self.animations:
            animation.init()

    def update(self, dt: float):
        res = True
        for animation in self.animations:
            res = res and animation.is_complete
            if not animation.is_complete:
                animation.update(dt) 
        self.is_complete = res
