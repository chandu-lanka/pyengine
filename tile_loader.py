import pygame
from pygame.locals import *
import imgs
import globals

tile_rects = []

def render_tiles(display, tile, x, y):
    if tile == '1':
        display.blit(imgs.dirt, (x * globals.TILE_SIZE - globals.true_scroll[0], y * globals.TILE_SIZE - globals.true_scroll[1]))
    if tile == '2':
        display.blit(imgs.grass, (x * globals.TILE_SIZE - globals.true_scroll[0], y * globals.TILE_SIZE - globals.true_scroll[1]))
    if tile != '0':
        tile_rects.append(pygame.Rect(x * globals.TILE_SIZE, y * globals.TILE_SIZE, globals.TILE_SIZE, globals.TILE_SIZE))
