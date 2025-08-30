import pygame
from options import *

background_board_layer = None
game_board_layer = None
points_highlight_layer = None
shadows_layer = None
pieces_layer = None
highlight_pieces_layer = None
ui_layer = None

def intialize_layers():
    global background_board_layer, game_board_layer
    global points_highlight_layer, pieces_layer, highlight_pieces_layer, ui_layer, shadows_layer
    
    background_board_layer = Layer.add_layer(0, False)
    game_board_layer = Layer.add_layer(1, True)
    shadows_layer = Layer.add_layer(2, True)
    points_highlight_layer = Layer.add_layer(3, True)
    pieces_layer = Layer.add_layer(4, True)
    highlight_pieces_layer = Layer.add_layer(5, True)
    ui_layer = Layer.add_layer(6, True)

class Layer:
    LAYERS = []
    
    def __init__(self, level, is_transparent):
        self.level = level
        self.is_transparent = is_transparent
        
        if not is_transparent: self.surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        else: self.surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        
    def blit(self, screen):
        screen.blit(self.surface, (0, 0))
    
    def clear(self):
        self.surface.fill((0, 0, 0, 0))
    
    @staticmethod
    def add_layer(level, is_transparent):
        layer = Layer(level, is_transparent)
        Layer.LAYERS.append(layer)
        return layer

    @staticmethod
    def draw_layers(screen):
        for layer in Layer.LAYERS:
            layer.blit(screen)
    
    @staticmethod
    def clear_layers():
        for layer in Layer.LAYERS: layer.clear()