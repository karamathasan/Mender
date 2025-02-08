import pygame
import numpy as np
from scene import Scene, Scene2D, Scene3D, Orthographic3D, Perspective3D
from entities._2D.circle import Circle
from elements._2D.circle import Circle as CircleElement
from elements._2D.square import Square
from entities._2D.square import Square as SquareEntity
from elements._2D.point import Point2D
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

from rendering.triangulation import Draftlaunay
if __name__ == "__main__":
    #TESTING STUF BEN HI
    naive=Draftlaunay()
    naive.triangulate()

    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))

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
    dt = 1/fps
    while running:
        # poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        dt = clock.tick(fps)/1000

        elapsed_time += dt
        # print(f"true fps: {1/dt}")

    pygame.quit()

