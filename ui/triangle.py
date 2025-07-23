import math
import layer
import game_logic.board as brd
from point import Point
from piece import *
from options import *
from colors import *
from shapes import *

def fill_pieces(points):
    board = brd.get_board()
    for index, point in enumerate(points):
        if index == 0 or index == 25: continue
        board_num = board[index]
        n = math.fabs(board_num)
        piece_color = LIGHT_PIECE if board_num > 0 else DARK_PIECE
        point.add_piece(n, piece_color)

def initialize_points_array():
    points = []
    down_off_section_y = SCREEN_HEIGHT * 0.6 - OFF_SECTION_ADDED_HEIGHT - BOARD_HEIGHT
    right_off_section_x = SCREEN_WIDTH - BOARD_HEIGHT - OFF_SECTION_WIDTH
    points.append(OffSection(right_off_section_x, down_off_section_y, OFF_SECTION, True)) # Dark off section
    
    def set_tris_array(is_dark, is_upside_down, y, iteration):
        for x in iteration:
            if x == 7: continue
            startX = x * TRIANGLE_WIDTH + TRIANGLE_WIDTH / 2
            point = Triangle(startX, y, LIGHT_TRIANGLES if is_dark else DARK_TRIANGLES, is_upside_down)
            is_dark = not is_dark
            points.append(point)
    
    set_tris_array(True, False, SCREEN_HEIGHT - BOARD_HEIGHT, range(13, 0, -1))
    set_tris_array(False, True, BOARD_HEIGHT, range(1, 14))

    points.append(OffSection(right_off_section_x, BOARD_HEIGHT, OFF_SECTION, False)) #Light off section
    fill_pieces(points)
    
    points.append(TakenSection())
    brd.update_board_array(points)
    return points

class Triangle(Point):
    def __init__(self, x, y, color, is_upside_down):
        super().__init__(x, y, color)
        self.is_upside_down = is_upside_down
        
    def draw(self):
        p1 = (self.x - TRIANGLE_WIDTH / 2, self.y)
        p2 = (self.x + TRIANGLE_WIDTH / 2, self.y)
        
        tmp = TRIANGLE_HEIGHT if self.is_upside_down else SCREEN_HEIGHT - TRIANGLE_HEIGHT
        p3 = (self.x, tmp)
        self.rect = draw_polygon(layer.game_board_layer, self.color, [p1, p2, p3])
        if self.is_highlighted:
            draw_polygon(layer.points_highlight_layer, GREEN_HIGHLIGHT, [p1, p2, p3])
        
        self.draw_pieces()
    
    def draw_pieces(self):
        y = self.y + PIECE_RADIUS if self.is_upside_down else self.y - PIECE_RADIUS
        
        for piece in self.pieces:
            piece.set_position(self.x, y)
            piece.draw()
            y += 2 * PIECE_RADIUS if self.is_upside_down else -2 * PIECE_RADIUS
    
class OffSection(Point):
    def __init__(self, x, y, color, draw_pieces_from_down_to_up):
        super().__init__(x, y, color)
        self.draw_pieces_from_down_to_up = draw_pieces_from_down_to_up
        
    def draw(self):
        self.rect = draw_rect(layer.game_board_layer, OFF_SECTION, self.x, self.y, OFF_SECTION_WIDTH, OFF_SECTION_HEIGHT)  
        if self.is_highlighted:
            draw_rect(layer.points_highlight_layer, GREEN_HIGHLIGHT, self.x, self.y, OFF_SECTION_WIDTH, OFF_SECTION_HEIGHT)
            
        self.draw_pieces()
            
    def draw_pieces(self):
        x = SCREEN_WIDTH - BOARD_HEIGHT - OFF_SECTION_WIDTH
        y = self.y if not self.draw_pieces_from_down_to_up else SCREEN_HEIGHT - BOARD_HEIGHT - OFF_PIECE_HEIGHT
        mult = 1 if not self.draw_pieces_from_down_to_up else -1
        
        for piece in self.pieces:
            piece.is_off = True
            piece.set_position(x, y)
            piece.draw()
            y += mult * OFF_PIECE_HEIGHT
        
class TakenSection(Point):
    def __init__(self):
        super().__init__(x=SCREEN_WIDTH / 2, y=SCREEN_HEIGHT / 2, color=NO_COLOR)
        self.rect = None
        
    def draw(self):
        self.draw_pieces()
        height = 2 * PIECE_RADIUS * len(self.pieces)
        self.rect = draw_rect(layer.game_board_layer, NO_COLOR, self.x - PIECE_RADIUS, self.y - height / 2, 2 * PIECE_RADIUS, height)
    
    def draw_pieces(self):
        x = self.x
        y = self.y - (len(self.pieces) - 1) * PIECE_RADIUS
        
        for piece in self.pieces:
            piece.set_position(x, y)
            piece.draw()
            y += 2 * PIECE_RADIUS