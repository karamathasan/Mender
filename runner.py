import pygame
import numpy as np
from scene import Scene, Scene2D, Scene3D, Orthographic3D, Perspective3D
from entities._2D.circle import Circle
from elements._2D.circle import Circle as CircleElement
from elements._2D.square import Square
from entities._2D.square import Square as SquareEntity
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
    screen = pygame.display.set_mode((1280, 720))

    clock = pygame.time.Clock()
    running = True
    fps = 60

    # Scene setup
    # 2D
    # p = Presentation()
    scene = Scene2D(screen=screen, fps=fps)
    
    square = SquareEntity(2,"red",20,gravity_enabled=False)
    square2 = SquareEntity(1,"white",gravity_enabled=False)

    # square.transform.orientation = np.pi/5
    # square2.transform.orientation = np.pi/4

    square.transform.shift(np.array([6,0]))
    square2.transform.shift(np.array([0,-6]))

    square.dynamics.set(velocity=np.array([-5,0]))
    square2.dynamics.set(velocity=np.array([0,5]))

    # circle = Circle(1,gravity_enabled=False)
    # circle.dynamics.set(velocity=np.array([1,0]))

    # circle = CircleElement(0.5)    
    # text = Text("hello", 22)
    # graph = CartesianGraph2D((5,5),(2,2))
    # graph.plotVec(end = np.array([-1,2]))

    # scene.add(text)
    # scene.add(graph)
    # print(square2.collider.getGlobalVertices())
    scene.add(square, square2)

    # p.add(scene, 
        # QuadraticShift2D(square, np.array([5,0]), 1),
        # CubicShift2D(circle, np.array([-5,0]), 1)
    # )
    
    # 3D
    # cube = CubeEntity(1, gravity_enabled=False)
    # cube.transform.orientation *= Quaternion.fromAxis(45,np.array([0,1,0]))
    # cube.transform.orientation *= Quaternion.fromAxis(45,np.array([0,0,1]))
    # cube.dynamics.set(angular_velocity= 50 * np.array([1,1,1]))
    # cube.dynamics.set(velocity= 2 * np.array([1,0,0]))

    # cube2 = CubeEntity(1, gravity_enabled=False)
    # cube2.transform.shift(np.array([0,2,0]))
    # cube2.dynamics.set(angular_velocity= 75 * np.array([0,1,1]))

    # sphere = Sphere3D(1)
    # sphere.dynamics.set(angular_velocity=50 * np.array([0,2,1]))

    # camera = Perspective3D(screen)
    # camera = Orthographic3D(screen)
    # camera.transform.shift(np.array([0,0,5]))
    # camera.transform.rotate(30, np.array([0,0,1]))

    # plane = Plane3D()

    # _3dscene = Scene3D(cube2, sphere, screen=screen, camera=camera, fps=fps)

    elapsed_time = 0
    dt = 1/fps
    # _3dscene.render()
    while running:
        # poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill("black")
        scene.physicsStep(dt)
        scene.render()

        # p.run(dt)

        # _3dscene.render()
        # _3dscene.physicsStep(dt)
        # cube.transform.rotate(0.5, np.array([0,1,0]))

        # square.collider.checkCollision(square2.collider)
        # if square.collider.checkCollision(square2.collider):
            # print(f"collision: {square.transform}")
        # print(square.collider.checkCollision(square2.collider))

        pygame.display.flip()
        dt = clock.tick(fps)/1000

        elapsed_time += dt
        # print(f"true fps: {1/dt}")

    pygame.quit()

