import pygame
import numpy as np
from scene import Scene, Scene2D, Scene3D
from entities._2D.circle import Circle
from entities._2D.square import Square


# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))

clock = pygame.time.Clock()
running = True

circle = Circle(40)
scene = Scene2D(circle, screen=screen)
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame

    # RENDER YOUR GAME HERE
    scene.render()
    # circle.drawCircle(screen)

    # flip() the display to put your work on screen
    pygame.display.flip()
    clock.tick(60)  # limits FPS to 60

pygame.quit()

