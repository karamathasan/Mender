from abc import ABC
from entity import Entity
class Solver(ABC):
    def __init__(self, fps):
        self.fps = fps
        self.deltaTime = 1/fps

class ExplicitEuclid(Solver):
    def __init__(self, fps):
        super().__init__(fps)
    
    def solve(entity: Entity):
        entity.update()