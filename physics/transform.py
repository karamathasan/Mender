import numpy as np
from rendering.quaternion import Quaternion

class Transform():
    def __init__(self):
        pass

class Transform2D(Transform):
    """
    An object used to hold information about elements and entities in 2D world space
    """
    def __init__(self, position: np.ndarray = None, orientation: float = None):
        """
        Creates a transform object that holds the position and orientation.
        Parameters:
            position: 2D vector of the position in world-space
            orientation: the Z rotation of a 2d object where Z points out of the sceen 
        """
        if position is None:
            self.position = np.array([0.0,0.0])
        else: self.position = np.float64(position)
        if orientation is None:
            self.orientation = 0
        else: self.orientation = orientation
    
    def shift(self, vec: np.ndarray):
        assert vec.shape == (2,)
        self.position += vec

    def rotate(self, degrees):
        self.orientation += degrees

    def __str__(self):
        return f"Transform: {str(self.position)} facing: {str(self.orientation)}"
        
class Transform3D(Transform):
    """
    An object used to hold information about elements and entities in 2D world space
    """
    def __init__(self, position: np.ndarray = None, orientation: Quaternion = None):
        """
        Creates a transform object that holds the position and orientation.
        Parameters:
            position: 3D vector of the position in world-space
            orientation: the quaternion that represents the rotation from global axes to this transforms local axes
        """
        if position is None:
            self.position = np.array([0.0,0.0,0.0])
        else: self.position = np.float64(position)
        if orientation is None:
            self.orientation = Quaternion()
        else: self.orientation = orientation
    
    def shift(self, vec):
        assert vec.shape == (3,)
        self.position += vec

    def rotate(self, degrees: float, axis: np.ndarray):
        assert axis.shape == (3,)
        q = Quaternion.fromAxis(degrees,axis)
        self.orientation = q * self.orientation 

    def face(self, orientation: Quaternion):
        self.orientation = orientation

    def __str__(self):
        return f"Transform: {str(self.position)} facing: {str(self.orientation)}"
