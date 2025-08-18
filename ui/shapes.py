import pygame
import pygame.gfxdraw
from colors import *

def draw_circle(layer, color, x, y, radius, width=0):
    rect = pygame.draw.circle(layer.surface, color, (x, y), radius)
    if width != 0:
        alpha = color[3] if len(color) == 4 else 255
        border_color = tuple(list(BLACK) + [alpha])
        pygame.draw.circle(layer.surface, border_color, (x, y), radius, width=width)
    return rect
    
def draw_transparent_circle(layer, color, x, y, radius, width=0):
    return draw_circle(layer, color, x, y, radius, width)

def draw_polygon(layer, color, points: list, width=0):
    scale = 4
    points_scaled = [(int(x * scale), int(y * scale)) for x, y in points]
    w = int(max(p[0] for p in points) - min(p[0] for p in points)) * scale + 4
    h = int(max(p[1] for p in points) - min(p[1] for p in points)) * scale + 4
    surf = pygame.Surface((w, h), pygame.SRCALPHA)

    offset_x = -min(p[0] for p in points_scaled) + 2
    offset_y = -min(p[1] for p in points_scaled) + 2
    points_offset = [(x + offset_x, y + offset_y) for x, y in points_scaled]

    pygame.draw.polygon(surf, color, points_offset)
    surf = pygame.transform.smoothscale(surf, (w // scale, h // scale))
    layer.surface.blit(surf, (min(p[0] for p in points) - 1, min(p[1] for p in points) - 1))

    return pygame.Rect(min(p[0] for p in points),
                       min(p[1] for p in points),
                       max(p[0] for p in points) - min(p[0] for p in points),
                       max(p[1] for p in points) - min(p[1] for p in points))

def draw_transparent_polygon(layer, color, points: list, width=0):
    return draw_polygon(layer, color, points, width)

def draw_rect(layer, color, x, y, width, height, border_width=0, border_radius=0):
    rect = pygame.draw.rect(layer.surface, color, (x, y, width, height), border_radius=border_radius)
    if border_width != 0:
        pygame.draw.rect(layer.surface, BLACK, (x, y, width, height), border_width, border_radius=border_radius)
    return rect

def draw_transparent_rect(layer, color, x, y, width, height, border_width=0, border_radius=0):
    return draw_rect(layer, color, x, y, width, height, border_width, border_radius)