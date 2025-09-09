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
from entities._2D.pointmass import PointMass

from elements.text import Text
from elements._2D.coordinategraph import CartesianGraph2D

from physics.transform import Transform2D
from rendering.quaternion import Quaternion
from rendering.noise import Noise, ValueNoise, PerlinNoise

from animation.shift import LinearShift2D, QuadraticShift2D, CubicShift2D
from animation.animationgroup import ParallelGroup, DeadlineGroup, RaceGroup, SequentialGroup
from animation.playable import Playable
from presentation.presentation import Presentation

from physics.environments import ManyBodyEnvironment2D

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
    # scene = Scene2D(screen=screen, fps=fps)
    scene = ManyBodyEnvironment2D(100, screen=screen, fps=fps)

    # square = SquareEntity(2,"red", mass = 2, gravity_enabled=False)
    # square2 = SquareEntity(1,"white",gravity_enabled=False)

    # square.transform.orientation = np.pi/5
    # square2.transform.orientation = np.pi/4

    # square.transform.shift(np.array([6,0]))
    # square2.transform.shift(np.array([0,-6]))

    # square.dynamics.set(velocity=np.array([-5,0]))
    # square2.dynamics.set(velocity=np.array([0,5]))
    # scene.add(square,square2)

    #PARTICLES

    # x_noise = PerlinNoise(32,256)
    # y_noise = PerlinNoise(32,256)
    
    # particles = []
    # s = 5
    # d=1.5
    # for i in range(s):
    #     for j in range(s):
    #         r = np.random.uniform(0,1,(2,))
    #         v = 5 * np.array([x_noise.sample(r),y_noise.sample(r)])
    #         t = Transform2D(np.array([d*(j-s//2),1.5*(i-s//2)]))
    #         p = PointMass(transform=t)
    #         p.dynamics.set(v)
    #         particles.append(p)
    # scene.add(*particles)

    # p1 = PointMass()
    # p2 = PointMass(transform=Transform2D(np.array([0.25,0])))
    # x_noise = ValueNoise(16,128)
    # y_noise = ValueNoise(16,128)

    # x_noise.generate_texture()

    # scene.add(p1)
    # scene.add(p2)

    elapsed_time = 0
    dt = 1/fps
    while running:
        # poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill("black")
        
        scene.physicsStep(dt)
        scene.render()

        # r1 = np.random.uniform(0,1,(2,))
        # r2 = np.random.uniform(0,1,(2,))
        # vx = 2 * x_noise.sample(r1) -1
        # vy = 2 * y_noise.sample(r1) -1
        # v1 = np.array([x_noise.sample(r1),y_noise.sample(r1)])
        # v2 = np.array([x_noise.sample(r2),y_noise.sample(r2)])
        # p1.dynamics.set(15 * v1)
        # p2.dynamics.set(15 * v2)

        # square.collider.checkCollision(square2.collider)
        # if square.collider.checkCollision(square2.collider):
            # print(f"collision: {square.transform}")
        # print(square.collider.checkCollision(square2.collider))

        pygame.display.flip()
        dt = clock.tick(fps)/1000

        elapsed_time += dt
        print(f"true fps: {1/dt}")

    pygame.quit()

