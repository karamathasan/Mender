from animation.playable import Playable
from animation.animation import Animation
from animation.animationgroup import AnimationGroup

class Presentation():
    def __init__(self, *playable: Playable):
        self.playables = [*playable]
        self.current_playable = None
        self.current_animation = None

    def add(self, scene, *animations: Animation):
        elements = set(scene.elements)
        for anim in animations:
            if not isinstance(anim, AnimationGroup):
                assert anim.element in elements
        self.playables.append(Playable(scene, *animations))

    def next(self):
        if len(self.current_playable.animations) > 0:
            self.current_animation = self.current_playable.animations.pop(0)
        elif len(self.playables) > 0:
            self.current_playable = self.playables.pop(0)
            self.current_animation = self.current_playable.animations.pop(0)

    def run(self, dt: float):
        if not self.current_playable:
            self.current_playable = self.playables.pop(0)
        if not self.current_animation:
            self.current_animation = self.current_playable.animations.pop(0)
            self.current_animation.init()

        if not self.current_animation.is_complete:
            self.current_animation.update(dt)
        else: 
            self.next()
            self.current_animation.init()
            
        self.current_playable.scene.render()
