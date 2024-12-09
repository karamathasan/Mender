import pygame
import numpy as np
from scene import Scene, Scene2D, Scene3D, Orthographic3D, Perspective3D
from entities._2D.circle import Circle
from entities._2D.square import Square
from entities._3D.cube import Cube as CubeEntity
from elements._3D.cube import Cube as CubeElement
from entities._3D.plane import Plane3D

from physics.transform import Transform2D
from rendering.quaternion import Quaternion

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))

clock = pygame.time.Clock()
running = True
fps = 60

# Scene setup
# circle = Circle(1,gravity_enabled=True)
# circle.dynamics.set(velocity=np.array([1,0]))

# scene = Scene2D(circle, screen=screen, fps=fps)
# scene.add(Square(1, 10, transform=Transform2D(np.array([10,0]),0),color = "red"))

# POSITIVE Z MIGHT BE OUT OF THE PAGE 
cube = CubeEntity(1, gravity_enabled=False)
# cube.dynamics.set(angular_velocity= 50 * np.array([0,0,1]))
cube.dynamics.set(velocity= 4 * np.array([1,0,1]))
# cube.transform.orientation=Quaternion.fromAxis(30, np.array([1,0,0]))
# cube.transform.rotate(45, np.array([0.0,1.0,1.0]))

camera = Perspective3D(screen)
# camera = Orthographic3D(screen)
# perspectiveCam.transform.rotate(-30, np.array([0,1,0]))
_3dscene = Scene3D(cube, screen=screen, camera=camera, fps=fps)
# _3dscene = Scene3D(cube, screen=screen, camera=perspectiveCam, fps=fps)

elapsed_time = 0
while running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    # camera.transform.rotate(1,np.array([0,1,0]))

    # scene.physicsStep()
    # scene.render()

    _3dscene.render()
    _3dscene.physicsStep()

    pygame.display.flip()
    clock.tick(fps)  
    elapsed_time += 1/fps

pygame.quit()

