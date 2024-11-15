from element import Element, Element2D, Element3D
from entity import Entity, Entity2D, Entity3D
from camera import Camera, Camera2D, Camera3D, Orthographic3D, Perspective3D
# the scene is where elements will be rendered together
# elements of the scene can be in 2d or 3d
# each scene should have its own coordinate system
class Scene():
    def __init__(self, *args: Element, screen):
        pass

    def add(self):
        pass

    def render(self):
        pass

    def physicsStep(self):
        # update all physics objects in the scene
        return


class Scene2D(Scene):
    def __init__(self, *args: Element2D, screen, camera: Camera2D = None):
        self.elements = list(args)
        if camera is None:
            self.camera = Camera2D(screen)
        else:
            self.camera = camera

    def add(self, *args: Element2D):
        self.elements.extend(args)

    def render(self):
        for element in self.elements:
            self.camera.render(element)
        self.physicsStep()
    
    def physicsStep(self):
        for element in self.elements:
            if element.isinstance(Entity):
                print("element is an entity")
        # update all physics objects in the scene
        return

# Note: +Y axis faces into the screen, +Z is up and +X is to the right
class Scene3D(Scene):
    def __init__(self, *args: Element3D, screen, camera: Camera3D = None):
        self.elements = list(args)
        if camera is None:
            self.camera = Camera3D(screen) # using a generic type may cause problems
        else: 
            self.camera = camera

    def add(self, *args: Element3D):
        self.elements.extend(args)

    def render(self):
        for element in self.elements:
            self.camera.render(element)