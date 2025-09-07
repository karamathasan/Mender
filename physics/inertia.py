import numpy as np

"""
Holds informaton on entity mass and rotational inertia
"""
class Inertia():
    def __init__(self, mass, vertices):
        pass

    def calcMOI():
        pass

    def calcCOM():
        pass

class Inertia2D(Inertia):
    def __init__(self, mass, vertices):
        self.mass = mass
        self.vertices = vertices

        self.com = np.mean(self.vertices)

    def calcMOI(self, r, moi_func = None):
        center_moi = moi_func(self.mass) if moi_func is not None else self._integrate_moi()
        return self.mass * r**2 + center_moi
    
    def _integrate_moi(self):
        return 
    
class Inertia3D(Inertia):
    def __init__(self, mass, vertices):
        self.mass = mass
        self.vertices = vertices

        self.com = np.mean(self.vertices)

    def calcMOI(self, r, moi_func = None):
        center_moi = moi_func(self.mass) if moi_func is not None else self._integrate_moi()
        return self.mass * r**2 + center_moi
    
    def _integrate_moi(self):
        return 

