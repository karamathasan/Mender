import numpy
from element import Element3D
from physics.transform import Transform3D

class CartesianCoordinateGraph3D(Element3D):
    def __init__(self, dimensions:tuple = None, scale:tuple = None, transform:Transform3D = None):
        super().__init__()
        self.dimensions = dimensions
        self.scale = scale

        self.points = []
        self.plots = []
        self.vectors = []
        self.functions = []

        if transform:
            self.transform = transform
        else:
            self.transform = Transform3D()
        pass

    def plotFunction(self, function):
        self.functions.append(function)

    def draw(self):
        pass