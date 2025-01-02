import pygame
import numpy as np
from scene import Scene, Scene2D, Scene3D, Orthographic3D, Perspective3D
from entities._2D.circle import Circle
from elements._2D.circle import Circle as CircleElement
from elements._2D.square import Square
from entities._2D.square import Square as SquareEntity
from elements._2D.point import Point2D
from entities._3D.cube import Cube as CubeEntity
from elements._3D.cube import Cube as CubeElement
from entities._3D.plane import Plane3D
from entities._3D.sphere import Sphere3D

from elements.text import Text
from elements._2D.coordinategraph import CartesianGraph2D

from physics.transform import Transform2D
from rendering.quaternion import Quaternion

from animation.shift import LinearShift2D, QuadraticShift2D, CubicShift2D
from animation.animationgroup import ParallelGroup, DeadlineGroup, RaceGroup, SequentialGroup
from animation.playable import Playable
from presentation.presentation import Presentation

if __name__ == "__main__":
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((1280/2, 720/2))

    clock = pygame.time.Clock()
    running = True
    fps = 60

    # Scene setup
    # 2D
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

    # scene.physicsStep()
    # scene.render()

    _3dscene.render()
    _3dscene.physicsStep()

    pygame.display.flip()
    clock.tick(fps)  
    elapsed_time += 1/fps

    pygame.quit()

