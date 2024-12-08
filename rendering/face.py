from edge import Edge2D, Edge3D
import numpy as np

class Face():

    '''
    Create a 3D face for rendering

    Parameters:
        points: a list of points in 3D space that form the triangular face. the points must be in counterclockwise order relative to the normal of the face
    '''
    def __init__(self, points: list[np.ndarray]):
        for point in points:
            assert point.shape == (3,) 
        self.a, self.b, self.c = points

        self.normal = np.cross((self.c - self.a), (self.b - self.a))
        self.normal = self.normal / np.linalg.norm(self.normal)

    # def edges2face()