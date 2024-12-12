import pygame
import numpy as np

# from rendering.edge import Edge2D, Edge3D
from rendering.quaternion import Quaternion
from rendering.rendertask import RenderTask
# from camera import Camera3D
from physics.transform import Transform3D

class Face():

    '''
    Create a 3D face for rendering

    Parameters:
        points: a list of points in 3D space that form the triangular face. the points must be in counterclockwise order relative to the normal of the face
    '''
    def __init__(self, *points: np.ndarray, color: str = "white", parent: Transform3D = None):
        for point in points:
            assert point.shape == (3,) 
        self.a, self.b, self.c = points
        self.color = color
        if parent is None:
            self.parent = Transform3D()
        else:
            self.parent = parent

class Triangle(Face):
    def __init__(self, *points, color: str = "white", parent: Transform3D = None):
        super().__init__(*points, parent=parent)
        self.normal = np.cross((self.c - self.a), (self.b - self.a))
        if np.linalg.norm(self.normal) > 0:
            self.normal = self.normal / np.linalg.norm(self.normal)
        else:
            self.normal = np.array([1,0,0])
    
    def draw(self, camera):
        # needs to account for rotations. 
        global_a = self.parent.position + (self.parent.orientation * Quaternion.Vec2Quaternion(self.a) * self.parent.orientation.conjugate()).toVec()
        global_b = self.parent.position + (self.parent.orientation * Quaternion.Vec2Quaternion(self.b) * self.parent.orientation.conjugate()).toVec()
        global_c = self.parent.position + (self.parent.orientation * Quaternion.Vec2Quaternion(self.c) * self.parent.orientation.conjugate()).toVec()

        depth = camera.getDepth((global_a + global_b + global_c)/3)
        screen_a = camera.Vec2Screen(global_a)
        screen_b = camera.Vec2Screen(global_b)
        screen_c = camera.Vec2Screen(global_c)
        # print(screen_a)
        basecolor = np.array([255,255,255])
        diff = max(np.dot(camera.getGlobalDirection(),(self.parent.orientation * Quaternion.Vec2Quaternion(self.normal) * self.parent.orientation.conjugate()).toVec()), 0)
        color = np.array(basecolor * diff, dtype=int)
        r,g,b = color
        # if screen_a and screen_b and screen_c:
        # pygame.draw.polygon(surface=camera.screen, color=(r,g,b), points=[screen_a, screen_b, screen_c])
        return RenderTask(
            (screen_a, screen_b, screen_c),
            (r,g,b),
            depth
        )

    @staticmethod
    def fromQuad(*points: np.ndarray, parent: Transform3D = None):
        for point in points:
            assert point.shape == (3,) 
        a,b,c,d = points
        return Triangle(a,b,c, parent=parent), Triangle(c,d,a, parent=parent)
    
# class Quad(Face):
#     def __init__(self, *points, color = "white", parent = None):
#         a,b,c,d = points
#         self.triangles = (Triangle(a,b,c),Triangle(c,d,a))

# def draw(self, camera: Camera3D):
#         # needs to account for rotations. 
#         a = camera.Vec2Screen(self.a)
#         b = camera.Vec2Screen(self.b)
#         c = camera.Vec2Screen(self.c)
        
#         color = np.dot(camera.getGlobalDirection(),self.normal)

#         pygame.draw.polygon(surface=camera.screen, color="white", points=[a, b, c])

#     @staticmethod