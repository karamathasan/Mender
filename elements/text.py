from element import Element
from physics.transform import Transform2D
import numpy as np
import pygame

class Text(Element):
    def __init__(self, text: str, size: np.ndarray, transform: Transform2D = None, color = "white"):
        self.text = text
        self.size = size
        if transform:
            self.transform = transform
        else:
            self.transform = Transform2D()
        self.color = color
        pygame.font.init()
        self.font = pygame.sysfont.SysFont("arial", self.size)

    def setText(self,text: str):
        self.text = text

    def draw(self, camera):
        render = self.font.render(self.text,False,self.color)
        # render = pygame.surfarray.array3d(render)
        # pygame.surfarray.blit_array(camera.screen,render)
        origin = camera.Vec2Screen(self.transform.position)
        camera.screen.blit(render,origin)
