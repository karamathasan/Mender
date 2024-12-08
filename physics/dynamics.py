import numpy as np
from abc import ABC

from physics.force import Force2D, Force3D
from physics.torque import Torque3D

class Dynamics(ABC):
    def __init__(self):
        self.velocity = None
        self.acceleration = None
        self.forces = {}
        self.parent = None

    def addForce(self, force):
        pass

    def netForce(self):
        sum = 0
        for force in self.forces.keys():
            sum += force
        return sum
        
    def netAcceleration(self) -> float:
        fn = self.netForce()
        return fn.toAcceleration(self.parent.mass)

class Dynamics2D(Dynamics):
    """
    Hold and handles information related to 2D entity physics and dynamics.
    Parameters:
        parent: the entity that is attached to this object
        velocity: the inital velocity in m/s
        acceleration: the initial acceleration in m/s^2
    """
    def __init__(self, parent, velocity: np.ndarray = None, acceleration: np.ndarray = None):
        assert parent
        self.parent = parent

        if velocity is None:
            self.velocity = np.array([0.0,0.0])
        else: 
            assert(velocity.shape == (2,))
            self.velocity = np.array(velocity, dtype=np.float64)

        if acceleration is None:
            self.acceleration = np.array([0.0,0.0])
        else: 
            assert(acceleration.shape == (2,))
            self.acceleration = np.array(acceleration, dtype=np.float64)
        self.forces = {}

    def set(self, velocity: np.ndarray = None, acceleration: np.ndarray = None):
        if velocity is not None:
            assert(velocity.shape == (2,))
            self.velocity = np.array(velocity, dtype=np.float64)
        if acceleration is not None:
            assert(acceleration.shape == (2,))
            self.acceleration = np.array(acceleration, dtype=np.float64)

    def addForce(self, force: Force2D):
        if force.forceMode == "impulse":
            self.forces[force] = force.duration
        else:
            self.forces[force] = np.inf

    def netForce(self):
        sum = Force2D.zero()
        for force in self.forces.keys():
            sum += force
        return sum

class Dynamics3D(Dynamics):
    """
    Hold and handles information related to 3D entity physics and dynamics.
    Parameters:
        parent: the entity that is attached to this object
        velocity: the inital velocity in m/s
        acceleration: the initial acceleration in m/s^2
        angular_velocity: the inital angular velocity in degrees/second
        angular_acceleration: the initial angular acceleration in degrees/second^2
    """
    def __init__(self, parent, 
                velocity: np.ndarray = None,
                acceleration: np.ndarray = None,
                angular_velocity: np.ndarray = None,
                angular_acceleration: np.ndarray = None):
        assert parent
        self.parent = parent

        if velocity is None:
            self.velocity = np.array([0.0,0.0,0.0])
        else:
            assert(velocity.shape == (3,))
            self.velocity = np.array(velocity, dtype=np.float64)

        if acceleration is None:
            self.acceleration = np.array([0.0,0.0,0.0])
        else: 
            assert(acceleration.shape == (3,))
            self.acceleration = np.array(acceleration, dtype=np.float64)

        if angular_velocity is None:
            self.angular_velocity = np.array([0.0,0.0,0.0])
        else:
            assert(angular_velocity.shape == (3,))
            self.angular_velocity = np.array(angular_velocity, dtype=np.float64)

        if angular_acceleration is None:
            self.angular_acceleration = np.array([0.0,0.0,0.0])
        else: 
            assert(angular_acceleration.shape == (3,))
            self.angular_acceleration = np.array(angular_acceleration, dtype=np.float64)

        self.forces = {}
        self.torques = {}

    def set(self, velocity: np.ndarray = None, acceleration: np.ndarray = None, angular_velocity: np.ndarray = None, angular_acceleration: np.ndarray = None):
        if velocity is not None:
            assert(velocity.shape == (3,))
            self.velocity = np.array(velocity, dtype=np.float64)
        if acceleration is not None:
            assert(acceleration.shape == (3,))
            self.acceleration = np.array(acceleration, dtype=np.float64)
        if angular_velocity is not None:
            assert(angular_velocity.shape == (3,))
            self.angular_velocity = np.array(angular_velocity, dtype=np.float64)
        if angular_acceleration is not None:
            assert(angular_acceleration.shape == (3,))
            self.angular_acceleration = np.array(angular_acceleration, dtype=np.float64)
    
    def addForce(self, force: Force3D):
        if force.forceMode == "impulse":
            self.forces[force] = force.duration
        else:
            self.forces[force] = np.inf

    #TODO: add impulse control. each iteration should remove 1/fps time to the duration value 
    def netForce(self): 
        sum = Force3D.zero()
        for force in self.forces.keys():
            sum += force
        return sum

    def addTorque(self, torque: Torque3D):
        if torque.duration is not np.inf:
            self.torques[torque] = torque.duration
        else:
            self.torques[torque] = np.inf

    def netTorque(self):
        sum = Torque3D.zero()
        for torque in self.torques.keys():
            sum += torque
        return Torque3D