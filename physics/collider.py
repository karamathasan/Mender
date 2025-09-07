import numpy as np
from abc import ABC
import pygame
import time

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
        selfLocal = self.getGlobalVertices()
        otherLocal = other.getGlobalVertices()

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
                dir = triple(simplex[1] - simplex[0], simplex[0], simplex[1] - simplex[0])
                dir = dir / (np.linalg.norm(dir) + 0.0001)
                # return None
                return False
            # simplex is complete
            a = simplex[2]
            ab = a-simplex[1]
            ac = a-simplex[0]
            abperp = triple(a,ab,a)                
            acperp = triple(a,ac,a)

            if np.dot(abperp, -a) > 0:    
                simplex.pop(0)
                return None
                # return False
            elif np.dot(acperp,-a) > 0:
                simplex.pop(1)
                return None
                # return False
            else:
                return simplex             
                # return True
            
        simplex = []
        # dir = np.array([1,0])
        dir = other.getCenter() - self.getCenter()
        support = supportPoint(dir)
        simplex.append(support)
        dir = -support / np.linalg.norm(-support)

        while True:
            support = supportPoint(dir)
            if np.dot(support,dir) < 0:
                return None
                # return False
            simplex.append(support)
            if handleSimplex(simplex, dir):
                return simplex  
                # return True

            
    def getPenetrationVector(self, other, polytope):
        assert isinstance(other, Collider2D)
        selfLocal = self.getGlobalVertices()
        otherLocal = other.getGlobalVertices()

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
        minNormal = np.array([1,0])

        while (minDistance == np.inf):
            for i in range(len(polytope)):
                j = (i + 1) % len(polytope)

                vertexI = polytope[i].copy()
                vertexJ = polytope[j].copy()

                ij = vertexJ - vertexI

                normal = np.array([ij[1], -ij[0]]) / (np.array([ij[1], -ij[0]]) + 0.0001)
                distance = normal.dot(vertexI)

                if (distance < 0):
                    distance *= -1
                    normal *= -1

                if (distance < minDistance):
                    minDistance = distance
                    minNormal = normal
                    minIndex = j
            support = supportPoint(minNormal)
            sDistance = np.dot(support, minNormal)

            if (abs(sDistance - minDistance) > 0.001):
                minDistance = np.inf
                polytope.insert(minIndex, support)

        return minNormal * (minDistance + 0.001)
    
    def getGlobalVertices(self):
        result = []
        rotmat = np.array(
            [[np.cos(self.parent.transform.orientation), -np.sin(self.parent.transform.orientation)],
             [np.sin(self.parent.transform.orientation), np.cos(self.parent.transform.orientation)]]
        )
        for vertex in self.vertices:
            result.append(self.parent.transform.position + rotmat @ vertex )
        return np.array(result)
    
    def getCenter(self):
        sum = 0
        for vertex in self.vertices:
            sum += vertex
        return sum/len(self.vertices)
    
class CircleCollider(Collider2D):
    def __init__(self):
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