import pygame
from colors import *

def draw_circle(screen, color, x, y, radius, width=0):
    rect = pygame.draw.circle(screen, color, (x, y), radius)
    
    if width == 0: return rect
    pygame.draw.circle(screen, BLACK, (x, y), radius, width=width)
    return rect
    
def draw_transparent_circle(surface, color, x, y, radius, width=0):
    return draw_circle(surface, color, x, y, radius, width)

def draw_polygon(screen, color, points: list, width=0):
    rect = pygame.draw.polygon(screen, color, points)
    if width == 0: return rect
    
    pygame.draw.polygon(screen, BLACK, points, width=width)
    return rect

def draw_transparent_polygon(surface, color, points: list, width=0):
    return draw_polygon(surface, color, points, width)