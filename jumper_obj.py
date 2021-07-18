import pygame
from pygame.locals import *
import imgs

class jumper_object():
    def __init__(self, loc):
        self.loc = loc

    def render(self, surf, scroll):
        surf.blit(imgs.arrow_up, (self.loc[0] - scroll[0], self.loc[1] - scroll[1]))

    def get_rect(self):
        rect = pygame.Rect(self.loc[0], self.loc[0], 7, 11)
        return rect

    def draw_rect(self,surf,color):
        return pygame.draw.rect(surf,color,pygame.Rect(self.loc[0], self.loc[0], 7, 11))

    def collision_test(self,rect):
        jump_rect = self.get_rect()
        return jump_rect.colliderect(rect)
