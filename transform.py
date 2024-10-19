import numpy as np

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
            self.position = np.array([0,0])
        else: self.position = position
        if orientation is None:
            self.orientation = 0
        else: self.orientation = orientation
    
    def shift(self, vec):
        self.position += vec

    def rotate(self, degrees):
        self.orientation += degrees