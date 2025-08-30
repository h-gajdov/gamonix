import math
import layer
import game_logic.board as brd
from point import Point
from piece import *
from options import *
from colors import *
from shapes import *

def fill_pieces(points):
    board = brd.board
    for index, point in enumerate(points):
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
            startX = x * TRIANGLE_WIDTH_FLOATING + TRIANGLE_WIDTH_FLOATING / 2
            point = Triangle(startX, y, LIGHT_TRIANGLES if is_dark else DARK_TRIANGLES, is_upside_down)
            is_dark = not is_dark
            points.append(point)
    
    set_tris_array(True, False, SCREEN_HEIGHT - BOARD_HEIGHT, range(13, 0, -1))
    set_tris_array(False, True, BOARD_HEIGHT, range(1, 14))

    points.append(OffSection(right_off_section_x, BOARD_HEIGHT, OFF_SECTION, False)) #Light off section
    
    points.append(TakenSection(is_white_section=True))
    points.append(TakenSection(is_white_section=False))
    fill_pieces(points)
    brd.update_board_array(points)
    return points

class Triangle(Point):
    def __init__(self, x, y, color, is_upside_down):
        super().__init__(x, y, color)
        self.is_upside_down = is_upside_down
        
    def draw(self, transparent_pieces=False):
        p1 = (self.x - TRIANGLE_WIDTH_FLOATING / 2, self.y)
        p2 = (self.x + TRIANGLE_WIDTH_FLOATING / 2, self.y)
        
        tmp = TRIANGLE_HEIGHT if self.is_upside_down else SCREEN_HEIGHT - TRIANGLE_HEIGHT
        p3 = (self.x, tmp)
        self.rect = draw_polygon(layer.game_board_layer, self.color, [p1, p2, p3])

        dash1 = (p1[0] + 8, p1[1])
        dash2 = (p2[0] - 8, p2[1])
        dash3 = (p3[0] - 1.25, p3[1] - 30 if self.is_upside_down else p3[1] + 30)

        draw_dashed_polygon(layer.game_board_layer.surface, (211, 211, 211, 0), [dash1, dash3], dash_length=2)
        draw_dashed_polygon(layer.game_board_layer.surface, (211, 211, 211, 128), [dash3, dash2], dash_length=2)
        if self.is_highlighted:
            draw_polygon(layer.points_highlight_layer, GREEN_HIGHLIGHT, [p1, p2, p3])
        
        self.draw_pieces(transparent_pieces)
    
    def draw_pieces(self, transparent_pieces=False):
        alpha = 190 if transparent_pieces else 255
        mult = 1 if self.is_upside_down else -1
        max_height = TRIANGLE_HEIGHT - 2 * PIECE_RADIUS

        n = len(self.pieces)
        y = self.y + mult * PIECE_RADIUS

        if n > 5:
            diff = max_height / (len(self.pieces) - 1) * mult
        else:
            diff = mult * 2 * PIECE_RADIUS

        for piece in self.pieces:
            piece.set_position(self.x, y)
            piece.draw(alpha)
            y += diff

    def highlight_made_move(self):
        if self.is_highlighted: return

        p1 = (self.x - TRIANGLE_WIDTH_FLOATING / 2, self.y)
        p2 = (self.x + TRIANGLE_WIDTH_FLOATING / 2, self.y)

        tmp = TRIANGLE_HEIGHT if self.is_upside_down else SCREEN_HEIGHT - TRIANGLE_HEIGHT
        p3 = (self.x, tmp)
        draw_polygon(layer.points_highlight_layer, MOVE_HIGHLIGHT, [p1, p2, p3])

class OffSection(Point):
    def __init__(self, x, y, color, draw_pieces_from_down_to_up):
        super().__init__(x, y, color)
        self.draw_pieces_from_down_to_up = draw_pieces_from_down_to_up
        
    def draw(self, transparent_pieces=False):
        self.rect = draw_rect(layer.game_board_layer, OFF_SECTION, self.x, self.y, OFF_SECTION_WIDTH, OFF_SECTION_HEIGHT)

        #Shadows
        draw_rect(layer.ui_layer, (0, 0, 0, 25), self.x, self.y, OFF_SECTION_WIDTH, 4)
        draw_rect(layer.ui_layer, (0, 0, 0, 25), self.x, self.y, 4, OFF_SECTION_HEIGHT)
        draw_rect(layer.ui_layer, (0, 0, 0, 25), self.x, self.y + OFF_SECTION_HEIGHT - 4, OFF_SECTION_WIDTH, 4)
        draw_rect(layer.ui_layer, (0, 0, 0, 25), self.x + OFF_SECTION_WIDTH - 4, self.y, 4, OFF_SECTION_HEIGHT)
        
        
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

    def highlight_made_move(self):
        if self.is_highlighted: return
        draw_rect(layer.points_highlight_layer, MOVE_HIGHLIGHT, self.x, self.y, OFF_SECTION_WIDTH, OFF_SECTION_HEIGHT)

class TakenSection(Point):
    def __init__(self, is_white_section):
        super().__init__(x=SCREEN_WIDTH / 2, y=SCREEN_HEIGHT / 2, color=NO_COLOR)
        self.rect = None
        self.is_white_section = is_white_section
        
    def draw(self, transparent_pieces=False):
        self.draw_pieces(transparent_pieces)
        height = 2 * PIECE_RADIUS * len(self.pieces)
        y_coord = self.y - height if self.is_white_section else self.y
        self.rect = draw_rect(layer.game_board_layer, NO_COLOR, self.x - PIECE_RADIUS, y_coord, 2 * PIECE_RADIUS, height)
    
    def draw_pieces(self, transparent_pieces=False):
        x = self.x
        height = 2 * PIECE_RADIUS * len(self.pieces)
        mult = 1 if self.is_white_section else -1
        
        if self.is_white_section: y = self.y - height + PIECE_RADIUS
        else: y = self.y + height - PIECE_RADIUS
            
        for piece in self.pieces:
            alpha = 190 if transparent_pieces else 255
            piece.set_position(x, y)
            piece.draw(alpha)
            y += mult * 2 * PIECE_RADIUS

    def highlight_made_move(self):
        pass