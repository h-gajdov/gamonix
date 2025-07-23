import layer
from shapes import *
from options import *
from colors import *

class Piece:
    def __init__(self, x: int = 0, y: int = 0, color = (0, 0, 0), is_highlighted: bool = False):
        self.x = x
        self.y = y
        self.color = color
        self.is_highlighted = is_highlighted
        self.rect = None
        self.is_off = False
    
    def draw(self):
        if self.is_off:
            draw_rect(layer.game_board_layer, self.color, self.x, self.y, OFF_PIECE_WIDTH, OFF_PIECE_HEIGHT, 1, 2)
            return
        
        self.rect = draw_circle(layer.pieces_layer, self.color, self.x, self.y, PIECE_RADIUS, 1)
        if self.is_highlighted:
            draw_transparent_circle(layer.highlight_pieces_layer, GREEN_HIGHLIGHT, self.x, self.y, PIECE_RADIUS)

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def move_between_points(self, source_point, destination_point):
        source_point.remove_specific_piece(self)
        destination_point.add_specific_piece(self)
        # destination_point.set_pieces_positions()
        # destination_point.piece_color = self.color
        self.is_highlighted = False

    def set_highlight(self, value):
        self.is_highlighted = value
