from physics.transform import Transform
from rendering.quaternion import Quaternion
# from camera import Camera

import numpy as np
# Camera parameters should create a Viewing Frustum for culling objects
class Frustum():
    """
    Create a viewing frustum for culling. 
    Params: 
        height: the height of the screen
        width: the width fo the screen
        near: the near clipping plane. Objects closer than this will not be rendered. This should also be the focal length of the camera
        far: the far clipping plane. 
    """
    def __init__(self, camera):
        self.camera = camera
        self.aspect_ratio = camera.aspect_ratio
        self.near_clip = camera.near_clip
        self.far_clip = camera.far_clip
        self.fov = camera.fov

        # self.far_plane = ()
        # self.near_plane = np.array([0,0,])

        # self.right_clip = 
        # self.left_clip = 
        # creating planes

    def _in_frustum(self, vec):
        # bring vec into camera's local coordinate system
        v = vec - self.camera.transform.position
        u = self.camera.direction
        v = (self.camera.transform.orientation.conjugate() * Quaternion.Vec2Quaternion(v) * self.camera.transform.orientation).toVec()
        
        h = self.camera.width/self.camera.aspect_ratio
        hfov = np.tan(h/(2*self.camera.focal_dist)) - np.pi/2 # top side
        wfov = np.deg2rad(self.camera.fov/2) - np.pi/2 # right side
        
        # hq = Quaternion.fromAxis(np.array([1,0,0]), hfov)
        # wq = Quaternion.fromAxis(np.array([0,1,0]), wfov)
        hq = Quaternion.fromAxis(hfov/2, np.array([1,0,0]))
        wq = Quaternion.fromAxis(wfov/2, np.array([0,1,0]))

        right_norm = (hq.conjugate() * Quaternion.Vec2Quaternion(np.array([0,0,-1])) * hq).toVec()
        top_norm = (wq.conjugate() * Quaternion.Vec2Quaternion(np.array([0,0,-1])) * wq).toVec()

        hq = Quaternion.fromAxis(-hfov/2, np.array([1,0,0]))
        wq = Quaternion.fromAxis(-wfov/2, np.array([0,1,0]))

        left_norm = (hq.conjugate() * Quaternion.Vec2Quaternion(np.array([0,0,-1])) * hq).toVec()
        bottom_norm = (wq.conjugate() * Quaternion.Vec2Quaternion(np.array([0,0,-1])) * wq).toVec()

        far_norm = np.array([0,0,1])
        near_norm = np.array([0,0,-1])

        norms = [right_norm, left_norm, top_norm, bottom_norm]
        for norm in norms:
            proj = np.dot(v,norm)
            if proj < 0:
                return False
        
        proj = np.dot(v,near_norm)
        if proj - self.near_clip < 0:
            return False
        
        proj = np.dot(v,far_norm)
        if proj + self.far_clip < 0:
            return False
        
        return True

    def __contains__(self, vec):
        return self._in_frustum(vec)
