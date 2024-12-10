import numpy as np
class Quaternion():
    def __init__(self, r: float = None, i:float = None, j:float = None, k:float = None):
        """
        Creates a quaternion from r, i, j, k componenents
        """
        self.i = i
        self.r = r 
        self.j = j
        self.k = k        

        if r is None:
            self.r = 1.0
        if i is None:
            self.i = 0.0
        if j is None:
            self.j = 0.0
        if k is None:
            self.k = 0.0


    @staticmethod
    def fromAxis(degrees: float, axis: np.ndarray):
        """
        Creates a quaternion given an angle and an axis
        Parameters:
            degrees: the angle of rotation in degrees
            axis: axis of rotation. Does not have to normalized
        """
        assert axis.shape == (3,)
        assert np.linalg.norm(axis) > 0.0001
        r = np.cos(np.radians(degrees/2))
        i,j,k = np.sin(np.radians(degrees/2)) * axis / np.linalg.norm(axis)
        return Quaternion(r,i,j,k)
    
    @staticmethod
    def Vec2Quaternion(vec: np.ndarray):
        """
        Creates a quaternion given a 3D coordinate/vector

        Parameters:
            vec: the vector in world space to be rotated
        """
        assert vec.shape[0] == 3
        return Quaternion(0,vec[0],vec[1],vec[2])
    
    def toVec(self):
        return np.array([self.i, self.j, self.k])

    def __mul__(self, other):
        if isinstance(other, float):
            return Quaternion(self.r * other, self.i * other, self.j * other, self.k * other)
        elif isinstance(other, Quaternion):
            return Quaternion(
                self.r * other.r - self.i * other.i - self.j * other.j - self.k * other.k,
                self.r * other.i + self.i * other.r + self.j * other.k - self.k * other.j,
                self.r * other.j - self.i * other.k + self.j * other.r + self.k * other.i,
                self.r * other.k + self.i * other.j - self.j * other.i + self.k * other.r 
            )
    
    def __truediv__(self, other):
        if isinstance(other, Quaternion):
            assert Quaternion.i == 0 and Quaternion.j == 0 and Quaternion.k == 0, "Quaternion could not be cast to scalar"
            other = Quaternion.r
        return Quaternion(self.r/other, self.i/other, self.j/other, self.k/other)

    def conjugate(self):
        """
        Conjugates this quaterion and then returns the resulting conjugate
        """
        self = Quaternion(self.r, -self.i, -self.j, -self.k)
        return self

    def len(self):
        """
        Returns the norm of this quaternion
        """
        return np.sqrt(self.r * self.r + self.i * self.i + self.j * self.j + self.k * self.k)

    def __invert__(self):
        self = self.conjugate() / self * self.conjugate()

    def __str__(self):
        return f"Quaternion: r:{self.r}, i:{self.i}, j:{self.j}, k:{self.k}"
            