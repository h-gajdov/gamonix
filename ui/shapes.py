import pygame
from colors import *

def draw_circle(layer, color, x, y, radius, width=0):
    rect = pygame.draw.circle(layer.surface, color, (x, y), radius)
    if width != 0:
        pygame.draw.circle(layer.surface, BLACK, (x, y), radius, width=width)
    return rect
    
def draw_transparent_circle(layer, color, x, y, radius, width=0):
    return draw_circle(layer, color, x, y, radius, width)

def draw_polygon(layer, color, points: list, width=0):
    rect = pygame.draw.polygon(layer.surface, color, points)
    if width != 0:
        pygame.draw.polygon(layer.surface, BLACK, points, width=width)
    return rect

def draw_transparent_polygon(layer, color, points: list, width=0):
    return draw_polygon(layer, color, points, width)

def draw_rect(layer, color, x, y, width, height, border_width=0, border_radius=0):
    rect = pygame.draw.rect(layer.surface, color, (x, y, width, height), border_radius=border_radius)
    if border_width != 0:
        pygame.draw.rect(layer.surface, BLACK, (x, y, width, height), border_width, border_radius=border_radius)
    return rect

def draw_transparent_rect(layer, color, x, y, width, height, border_width=0, border_radius=0):
    return draw_rect(layer, color, x, y, width, height, border_width, border_radius)