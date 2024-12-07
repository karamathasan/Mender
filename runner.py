import pygame
import numpy as np
from scene import Scene, Scene2D, Scene3D, Orthographic3D
from entities._2D.circle import Circle
from entities._2D.square import Square
from entities._3D.cube import Cube as CubeEntity
from elements._3D.cube import Cube as CubeElement

from physics.transform import Transform2D
from rendering.quaternion import Quaternion

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))

clock = pygame.time.Clock()
running = True
fps = 600

# Scene setup
# circle = Circle(1,gravity_enabled=True)
# circle.dynamics.set(velocity=np.array([1,0]))

# scene = Scene2D(circle, screen=screen, fps=fps)
# scene.add(Square(1, 10, transform=Transform2D(np.array([10,0]),0),color = "red"))

cube = CubeElement(1)
# cube.transform.orientation=Quaternion.fromAxis(30, np.array([1,0,0]))
# cube.transform.rotate(45, np.array([0.0,1.0,1.0]))
_3dscene = Scene3D(screen=screen, camera=Orthographic3D(screen=screen))
_3dscene.add(cube)

while running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")
    # RENDER YOUR GAME HERE

    # scene.physicsStep()
    # scene.render()
    _3dscene.render()

    # flip() the display to put your work on screen
    pygame.display.flip()
    clock.tick(fps)  # source of bug

pygame.quit()

