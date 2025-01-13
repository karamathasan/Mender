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

    #could return none if there is not collision and a the simplex if there is. the simplex can then be used for EPA
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
                return None
            
            # simplex is complete
            a = simplex[2]
            ab = a-simplex[1]
            ac = a-simplex[0]
            abperp = triple(a,ab,a)                
            acperp = triple(a,ac,a)
            if np.dot(abperp, -a) > 0:    
                simplex.pop(0)
                return None
            elif np.dot(acperp,-a) > 0:
                simplex.pop(1)
                return None
            else:
                return simplex             
            
        simplex = []
        dir = np.array([-1,-1])
        support = supportPoint(dir)
        simplex.append(support)
        dir = -support / np.linalg.norm(-support)

        while True:
            support = supportPoint(dir)
            if np.dot(support,dir) < 0:
                return None
            simplex.append(support)
            if handleSimplex(simplex, dir):
                return simplex  

    def getPenetrationVector(self, other, polytope):
        assert isinstance(other, Collider2D)
        selfLocal = self.getLocalVertices()
        otherLocal = other.getLocalVertices()

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

        minIndex = 0
        minDistance = np.inf
        minNormal

        while (minDistance == np.inf):
            for i in range(len(polytope)):
                j = (i + 1) % polytope.length

                vertexI = polytope[i].copy()
                vertexJ = polytope[j].copy()

                ij = vertexJ.sub(vertexI)

                normal = np.array([ij.y, -ij.x]) / np.linalg.norm([ij.y, -ij.x])
                distance = normal.dot(vertexI)

                if (distance < 0):
                    distance *= -1
                    normal *= -1

                if (distance < minDistance):
                    minDistance = distance
                    minNormal = normal
                    minIndex = j
            support = supportPoint(self.vertices, other.vertices, minNormal)
            sDistance = np.dot(support, minNormal)

            if (abs(sDistance - minDistance) > 0.001):
                minDistance = np.inf
                # polytope.splice(minIndex, 0, support)
                polytope.insert(minIndex, support)

        return minNormal.mult(minDistance + 0.001)
    
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