from abc import ABC
import numpy as np
from physics.entity import Entity, Entity2D, Entity3D
from rendering.quaternion import Quaternion

class Solver(ABC):
    def __init__(self):
        pass

class ExplicitEuclid2D(Solver):
    def __init__(self):
        self.entities = []

    def initEntities(self, elements):
        """
        filters through a scene's elements to retrieve its entities
        """
        for element in elements:
            if isinstance(element, Entity2D):
                self.entities.append(element)
    
    def solve(self, entity: Entity2D, dt):
        # constraints will visit the solver to provide or edit calculations
        dyn = entity.dynamics
        transform = entity.transform
        v = dyn.velocity
        a = entity.dynamics.netAcceleration()

        v += a * dt
        transform.shift(v * dt)

    #can be inconsistent with some situations (objects phase through each other)
    def handleCollsion(self, entity1, entity2):
        #linear
        v1 = entity1.dynamics.velocity 
        v2 = entity2.dynamics.velocity
        m1 = entity1.mass
        m2 = entity2.mass
        sysmomentum = m1 * v1 + m2 * v2
        sysmass = m1 + m2
        v2new = ((v1-v2) * m1 + sysmomentum)/sysmass
        v1new = ((v2-v1) * m2 + sysmomentum)/sysmass

        entity1.dynamics.set(velocity=v1new)
        entity2.dynamics.set(velocity=v2new)

    # experimental method
    def solveEntities(self, dt):
        for entity1 in self.entities:
            for entity2 in self.entities:
                if entity1 != entity2:
                    simplex = entity1.collider.checkCollision(entity2.collider) 
                    if simplex:
                        # return
                        v1 = entity1.collider.getPenetrationVector(entity2.collider,simplex)
                        v2 = entity2.collider.getPenetrationVector(entity1.collider,simplex)
                        entity1.transform.shift(v1)
                        entity2.transform.shift(v2)
                        self.handleCollsion(entity1, entity2)
                        # v1, v2 = self.handleCollsion(entity1, entity2)
                        # entity1.dynamics.set(velocity = v1)
                        # entity2.dynamics.set(velocity = v2)
            self.solve(entity1,dt)
            
class ExplicitEuclid3D(Solver):
    def __init__(self):
        self.entities = []
        # super().__init__(fps)
        pass

    def initEntities(self, elements):
        for element in elements:
            if isinstance(element, Entity3D):
                self.entities.append(element)
    
    def solve(self, entity: Entity3D, dt: float):
        # constraints will visit the solver to provide or edit calculations
        dyn = entity.dynamics
        transform = entity.transform
        v = dyn.velocity
        a = entity.dynamics.netAcceleration()

        angv = dyn.angular_velocity
        anga = dyn.angular_acceleration # will need to properly calculate through inerta tensor

        v += a * dt
        angv += anga * dt

        transform.shift(v * dt)
        if np.linalg.norm(angv) > np.finfo(float).eps:
            # print()
            transform.rotate(np.linalg.norm(angv) * dt, angv/np.linalg.norm(angv))
        # transform.rotate(0.1,np.array([1,0,0]))