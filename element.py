from physics.transform import Transform
from abc import ABC

class Element(ABC):
    def __init__(self):
        self.transform: Transform 
        pass

    def draw(self):
        pass

class Element2D(Element):
    pass

class Element3D(Element):
    pass
