import math
import layer
from point import Point
from piece import *
from options import *
from colors import *
from shapes import *
from game_logic.board import get_board

def fill_pieces(points):
    board = get_board()
    for index, point in enumerate(points):
        if index == 0 or index == 25: continue
        board_num = board[index - 1]
        n = math.fabs(board_num)
        piece_color = LIGHT_PIECE if board_num > 0 else DARK_PIECE
        point.add_piece(n, piece_color)

def initialize_points_array():
    points = []
    down_off_section_y = SCREEN_HEIGHT * 0.6 - OFF_SECTION_ADDED_HEIGHT - BOARD_HEIGHT
    right_off_section_x = SCREEN_WIDTH - BOARD_HEIGHT - OFF_SECTION_WIDTH
    points.append(OffSection(right_off_section_x, down_off_section_y, OFF_SECTION, True)) # Dark off section
    points[0].add_piece(2, DARK_PIECE)
    
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
    points[-1].add_piece(2, LIGHT_PIECE)
    
    fill_pieces(points)
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
            self.rect = draw_polygon(layer.points_highlight_layer, GREEN_HIGHLIGHT, [p1, p2, p3])
        
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
            piece.set_position(x, y)
            piece.draw()
            y += mult * OFF_PIECE_HEIGHT
            
    def add_piece(self, n=1, piece_color=BLACK):
        super().add_piece(n, piece_color)
        for piece in self.pieces: piece.is_off = True
        
# class Triangle:
#     def __init__(self, x: int, y: int, color: tuple, width: int, height: int, is_upside_down: bool, number_of_pieces: int, piece_color = (0, 0, 0)):
#         self.x = x
#         self.y = y
#         self.color = color
#         self.width = width
#         self.height = height
#         self.is_upside_down = is_upside_down
#         self.number_of_pieces = number_of_pieces
#         self.piece_color = piece_color
#         self.selected = False
#         self.pieces = [] 
#         self.add_piece(number_of_pieces)
            
#     def draw(self):
#         p1 = (self.x - self.width / 2, self.y)
#         p2 = (self.x + self.width / 2, self.y)
        
#         tmp = self.height if not self.is_upside_down else SCREEN_HEIGHT - self.height
#         p3 = (self.x, tmp)
#         self.rect = draw_polygon(layer.game_board_layer, self.color, [p1, p2, p3])
        
#         for piece in self.pieces: piece.draw()
            
#     def select(self):
#         if self.pieces: self.pieces[-1].set_highlight(True)
    
#     def deselect(self):
#         if self.pieces: self.pieces[-1].set_highlight(False)

#     def highlight(self):
#         p1 = (self.x - self.width / 2, self.y)
#         p2 = (self.x + self.width / 2, self.y)
        
#         tmp = self.height if not self.is_upside_down else SCREEN_HEIGHT - self.height
#         p3 = (self.x, tmp)
#         draw_transparent_polygon(layer.triangle_highlight_layer, (0, 255, 0, 128), [p1, p2, p3])
        
#     def add_piece(self, n = 1):
#         self.number_of_pieces += n
        
#         for _ in range(self.number_of_pieces):
#             piece = Piece(color=self.piece_color)
#             self.pieces.append(piece)
        
#         self.set_pieces_positions()

#     def add_specific_piece(self, piece):
#         self.pieces.append(piece)
#         self.number_of_pieces = len(self.pieces)
#         self.piece_color = piece.color
#         self.set_pieces_positions()

#     def set_pieces_positions(self):
#         mult = -1 if self.is_upside_down else 1
#         pieceX = self.x
#         pieceY = self.y + mult * PIECE_RADIUS
#         for piece in self.pieces:
#             piece.set_position(pieceX, pieceY)
#             pieceY += mult * 2 * PIECE_RADIUS

#     def remove_piece(self, n = 1):
#         self.number_of_pieces -= n
#         if self.pieces: last = self.pieces[-1]

#         if self.number_of_pieces < 0:
#             self.number_of_pieces = 0
#             self.pieces.clear()
#         else:
#             for _ in range(n): self.pieces.pop()

#         return last
    
#     def remove_specific_piece(self, piece):
#         self.pieces.remove(piece)
#         self.number_of_pieces = len(self.pieces)

#     def pop_piece(self):
#         if self.pieces: return self.pieces.pop()

#     def check_color(self, is_light_on_turn):
#         if self.number_of_pieces <= 1: return True
#         if is_light_on_turn and self.piece_color == DARK_PIECE: return False
#         if not is_light_on_turn and self.piece_color == LIGHT_PIECE: return False
#         return True