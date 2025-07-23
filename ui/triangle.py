import math
import layer
from point import Point
from piece import *
from options import *
from colors import *
from shapes import *
from game_logic.board import get_board

def initialize_points_array():
    points = []
    down_off_section_y = SCREEN_HEIGHT * 0.6 - OFF_SECTION_ADDED_HEIGHT - BOARD_HEIGHT
    right_off_section_x = SCREEN_WIDTH - BOARD_HEIGHT - OFF_SECTION_WIDTH
    points.append(OffSection(right_off_section_x, down_off_section_y, OFF_SECTION)) # Dark off section
    
    is_dark = False
    for x in range(1, 14):
        if x == 7: continue
        startX = x * TRIANGLE_WIDTH + TRIANGLE_WIDTH / 2
        point = Triangle(startX, SCREEN_HEIGHT - BOARD_HEIGHT, LIGHT_TRIANGLES if is_dark else DARK_TRIANGLES, False)
        is_dark = not is_dark
        points.append(point)
    
    points.reverse()
    is_dark = not is_dark
    for x in range(1, 14):
        if x == 7: continue
        startX = x * TRIANGLE_WIDTH + TRIANGLE_WIDTH / 2
        point = Triangle(startX, BOARD_HEIGHT, LIGHT_TRIANGLES if is_dark else DARK_TRIANGLES, True)
        is_dark = not is_dark
        points.append(point)

    points.append(OffSection(right_off_section_x, BOARD_HEIGHT, OFF_SECTION))
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

class OffSection(Point):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        
    def draw(self):
        print('call')
        self.rect = draw_rect(layer.game_board_layer, OFF_SECTION, self.x, self.y, OFF_SECTION_WIDTH, OFF_SECTION_HEIGHT)        
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