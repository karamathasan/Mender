import numpy as np
from elements._2D.point import Point2D
class Triangulator():
    def __init__():
        pass
    def triangulate():
        pass
    
class Delaunay(Triangulator):
    def __init__(self, points: list[Point2D]):
        self.points = points

    def triangulate(self):
        """
        Calculate the lines that would be needed to be drawn with pygame to create a delauney triangulation of the available points
        """
        pass

class Draftlaunay(Triangulator):
    def __init__(self):
        pass
    def triangulate(self):
        # x,y,z=np.zeros(NMAX,)
        #n means number of input points
        #indices of four points is i,j,k,m
        #xn,yn,zn is the outward normal to (i,j,k)
        #flag is True of m is above (i,j,k)
        #input points xy,z=x^2+y^2
            x=[31 ,-13,-63, -5, 87,40, 23, 64,  0,-14]
            y=[-76, 21,-83,-66,-94,71,-46,-80,-57,  2]
            n=len(x)
            z=[0]*n
            for t in range(n):
                z[t] = x[t]*x[t]+y[t]*y[t]
            for i in range (0,n-2):
                for j in range (i+1,n):
                    for k in range (i+1,n):
                        if(j!=k):
                            # computing normals to triangles (i,j,k) I think this is for all combos,
                            # and we keep only those below the paraboloid
                            xn = (y[j]-y[i])*(z[k]-z[i]) - (y[k]-y[i])*(z[j]-z[i])
                            yn = (x[k]-x[i])*(z[j]-z[i]) - (x[j]-x[i])*(z[k]-z[i])
                            zn = (x[j]-x[i])*(y[k]-y[i]) - (x[k]-x[i])*(y[j]-y[i])
                        
                            # Now we're only looking at faces on the bottom of paraboloid: zn < 0
                            flag = (zn < 0)
                            # print(flag)
                            if(flag):
                                #for each other point m
                                for m in range(0, n):
                                    #Check if m above (i,j,k). [Note: why?]
                                    flag = flag and ((x[m]-x[i])*xn +\
                                                     (y[m]-y[i])*yn + \
                                                     (z[m]-z[i])*zn <= 0)
                            if (flag):
                                # points.append(Point2D(color="white",Transform2d=(x[i],y[i]))) #draft, trying to compile pts
                                print(i,j,k)

class Voronoi():
    def __init__(self, points: list[Point2D]):
        self.points = points 
 
    def render(self, pxarray):
        """
        Calculate the the pixel coordinates of the points that are equally distant to the points in this Voronoi renderer
        """
        # Iterate through each pixel in pxarray, convert px array coordinates into world coordinates, calculate the distances
        # O(mn * p)
        pass