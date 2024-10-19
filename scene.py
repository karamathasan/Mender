from element import Element, Element2D, Element3D
# the scene is where elements will be rendered together
# elements of the scene can be in 2d or 3d
# each scene should have its own coordinate system
class Scene():
    def __init__(self, elements):
        pass

    def add(self):
        pass
    def render(self):
        pass
        for element in self.elements:
            element.render()

class Scene2D(Scene):
    def __init__(self, *args: Element2D):
        self.elements = list(args)
        pass

    def add(self, *args: Element2D):
        self.elements.extend(args)

    def render(self, screen):
        for element in self.elements:
            element.render(screen)

class Scene3D(Scene):
    def __init__(self, elements):
        pass

    def add(self, *args: Element3D):
        pass

    def render(self, screen):
        for element in self.elements:
            element.render(screen)