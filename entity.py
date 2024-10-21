from element import Element, Element2D, Element3D
# an entity is an object affected by physics 
# entities hold constraints to the rules of physics that can be applied to them
#   for example, they may be immovable in some directions, or they may not be able to rotate
# entities in a sense, are rigidbodies

# parent type
class Entity(Element):
    def __init__():
        pass
    def draw():
        pass

class Entity2D(Entity, Element2D):
    def __init__():
        pass
    def draw():
        pass

class Entity3D(Entity, Element3D):
    def __init__():
        pass
    def draw():
        pass