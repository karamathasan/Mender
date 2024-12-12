import numpy as np
from elements._2D.point import Point2D
class Triangulator():
    def __init__():
        pass
    def triangulate():
        pass
    
class Delauney(Triangulator):
    def __init__(self, points: list[Point2D]):
        self.points = points

    def triangulate(self):
        """
        Calculate the lines that would be needed to be drawn with pygame to create a delauney triangulation of the available points
        """
        pass

class Voronoi():
    def __init__(self, points: list[Point2D]):
        self.points = points 
 
    def render(self, pxarray):
        """
        Calculate the the pixel coordinates of the points that are equally distant to the points in this Voronoi renderer
        """
        # Iterate through each pixel in pxarray, convert px array coordinates into world coordinates, calculate the distances
        # O(mn * p)
        pass