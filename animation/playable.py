import numpy as np
import pygame 
from physics.transform import Transform2D, Transform3D
from scene import Scene
from animation.animation import Animation
from animation.animationgroup import AnimationGroup

class Playable():
    def __init__(self, scene: Scene, *animations: Animation):
        self.elements = set(scene.elements)
        for anim in animations:
            if not isinstance(anim, AnimationGroup):
                assert anim.element in self.elements
        self.scene = scene
        self.animations = [*animations]
        