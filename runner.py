import pygame
import numpy as np
from scene import Scene, Scene2D, Scene3D, Orthographic3D, Perspective3D
from entities._2D.circle import Circle
from entities._2D.square import Square
from elements._2D.point import Point2D
from entities._3D.cube import Cube as CubeEntity
from elements._3D.cube import Cube as CubeElement
from entities._3D.plane import Plane3D
from entities._3D.sphere import Sphere3D

from physics.transform import Transform2D
from rendering.quaternion import Quaternion

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))

clock = pygame.time.Clock()
running = True
fps = 60

# Scene setup
# circle.dynamics.set(velocity=np.array([1,0]))
scene = Scene2D(screen=screen, fps=fps)
for i in range(10):
    randx = np.random.uniform(-scene.camera.width/2, scene.camera.width/2)
    randy = np.random.uniform(-(scene.camera.width/2) / scene.camera.aspect, (scene.camera.width/2) / scene.camera.aspect)
    scene.add(Point2D(
        transform=Transform2D(np.array([randx,randy]))
    ))


elapsed_time = 0
while running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    scene.physicsStep()
    scene.render()

    pygame.display.flip()
    clock.tick(fps)  
    elapsed_time += 1/fps

pygame.quit()

