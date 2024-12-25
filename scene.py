from element import Element, Element2D, Element3D
from camera import Camera, Camera2D, Camera3D, Orthographic3D, Perspective3D

from physics.entity import Entity, Entity2D, Entity3D
from physics.solver import Solver, ExplicitEuclid2D, ExplicitEuclid3D
# the scene is where elements will be rendered together
# elements of the scene can be in 2d or 3d
# each scene should have its own coordinate system
class Scene():
    def __init__(self, *args: Element, screen):
        self.elements: list[Element]
        pass

    def add(self):
        pass

    def render(self):
        pass

    def physicsStep(self):
        # update all physics objects in the scene
        return


class Scene2D(Scene):
    def __init__(self, *args: Element2D, screen, camera: Camera2D = None, solver: Solver = None, fps = 60):
        self.elements = list(args)
        self.fps = fps
        if camera is None:
            self.camera = Camera2D(screen)
        else:
            self.camera = camera

        if solver is None:
            self.solver = ExplicitEuclid2D()
        else:
            self.solver = solver
        
    def add(self, *args: Element2D):
        self.elements.extend(args)

    def render(self):
        for element in self.elements:
            self.camera.render(element)
    
    def physicsStep(self):
        for element in self.elements:
            if isinstance(element, Entity2D):
                self.solver.solve(element)
        # update all physics objects in the scene
        return

# Note: +Z axis faces out of the screen, +Y is up and +X is to the right
class Scene3D(Scene):
    def __init__(self, *args: Element3D, screen, camera: Camera3D = None, solver: Solver = None, fps = 60):
        self.elements = list(args)
        if camera is None:
            self.camera = Orthographic3D(screen) # using a generic type may cause problems
        else: 
            self.camera = camera
        self.fps = fps
        if solver is None:
            self.solver = ExplicitEuclid3D()
        else:
            self.solver = solver

    def add(self, *args: Element3D):
        self.elements.extend(args)

    def render(self):
        for element in self.elements:
            self.camera.render(element)

    def physicsStep(self, dt):
        for element in self.elements:
            if isinstance(element, Entity3D):
                self.solver.solve(element, dt)
        # update all physics objects in the scene
        return