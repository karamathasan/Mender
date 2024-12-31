import numpy as np
from abc import ABC
import pygame

class Collider(ABC):
    def __init__(self, parent, vertices):
        self.vertices = np.array(vertices)
        self.parent = parent

    def checkCollision(self, other):
        pass

class Collider2D(Collider):
    def __init__(self, parent, vertices: np.ndarray):
        for vertex in vertices:
            assert vertex.shape == (2,), f"invalid vertex shape. got:{vertex.shape}"
        super().__init__(parent,vertices)

    def checkCollision(self, other: Collider):
        assert isinstance(other, Collider2D)
        selfLocal = self.getLocalVertices()
        otherLocal = other.getLocalVertices()
        # GJK 
        def triple(a,b,c):
            a = np.append(a,0)
            b = np.append(b,0)
            c = np.append(c,0)
            res = np.cross(np.cross(a,b),c)
            return res[:2]

        def supportPoint(dir):
            selfExtreme = selfLocal[np.argmax(selfLocal @ dir)]
            otherExtreme = otherLocal[np.argmax(otherLocal @ -dir)]           
            return selfExtreme - otherExtreme 
        
        def handleSimplex(simplex, dir):
            # buidling simplex from line
            if len(simplex) == 2:
                # dir = np.cross(np.cross(simplex[1] - simplex[0], simplex[0]), simplex[1]-simplex[0])
                dir = triple(simplex[1] - simplex[0], simplex[0], simplex[1] - simplex[0])
                dir = dir / np.linalg.norm(dir)
                return False
            
            # simplex is complete
            a = simplex[2]
            ab = a-simplex[1]
            ac = a-simplex[0]
            # abperp = np.cross(np.cross(a,ab),a)         
            abperp = triple(a,ab,a)                
            # acperp = np.cross(np.cross(a,ac),a)
            acperp = triple(a,ac,a)
            if np.dot(abperp, -a) > 0:    
                simplex.pop(0)
                return False
            elif np.dot(acperp,-a) > 0:
                simplex.pop(1)
                return False
            else:
                return True             
            
        simplex = []
        dir = np.array([-1,-1])
        support = supportPoint(dir)
        simplex.append(support)
        dir = -support / np.linalg.norm(-support)

        while True:
            support = supportPoint(dir)
            if np.dot(support,dir) < 0:
                return False
            simplex.append(support)
            if handleSimplex(simplex, dir):
                return True  
        
    def getLocalVertices(self):
        # localVertices = self.parent.transform.position + 
        result = []
        rotmat = np.array(
            [[np.cos(self.parent.transform.orientation), -np.sin(self.parent.transform.orientation)],
             [np.sin(self.parent.transform.orientation), np.cos(self.parent.transform.orientation)]]
        )
        for vertex in self.vertices:
            result.append(self.parent.transform.position + rotmat @ vertex )
        return np.array(result)
    
class CircleCollider(Collider2D):
    pass

class Collider3D(Collider):
    def __init__(self, parent, vertices: np.ndarray):
        for vertex in vertices:
            assert vertex.shape == (3,0)
        super().__init__(parent,vertices)

    def checkCollision(self, other):
        # GJK algorithm
        pass

class SphereCollider(Collider3D):
    pass