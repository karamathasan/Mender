import pygame
import numpy as np
from scene import Scene, Scene2D, Scene3D, Orthographic3D
from entities._2D.circle import Circle
from entities._2D.square import Square
from elements._3D.cube import Cube
from physics.transform import Transform2D

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))

clock = pygame.time.Clock()
running = True
fps = 60

# Scene setup
circle = Circle(1)
scene = Scene2D(circle, screen=screen)
# scene.add(Square(20, 5, transform=Transform2D(np.array([40,0]),0),color = "red"))

# cube = Cube(100)
# _3dscene = Scene3D(screen=screen, camera=Orthographic3D(screen=screen))
# _3dscene.add(cube)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")
    # RENDER YOUR GAME HERE

    scene.render()
    scene.physicsStep()
    # _3dscene.render()

    # flip() the display to put your work on screen
    pygame.display.flip()
    clock.tick(fps)  # limits FPS to 60

pygame.quit()

