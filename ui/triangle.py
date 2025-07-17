import math
import layer
from options import *
from colors import *
from shapes import *
from game_logic.board import get_board
# from game import background_board_layer, game_board_layer, pieces_layer

def initialize_triangles_array():
    tris = []
    is_dark = False
    for x in range(1, 14):
        if x == 7: continue
        startX = x * TRIANGLE_WIDTH + TRIANGLE_WIDTH / 2
        tri = Triangle(startX, SCREEN_HEIGHT - BOARD_HEIGHT, LIGHT_TRIANGLES if is_dark else DARK_TRIANGLES, TRIANGLE_WIDTH, TRIANGLE_HEIGHT, True, 0)
        is_dark = not is_dark
        tris.append(tri)
    
    tris.reverse()
    is_dark = not is_dark
    for x in range(1, 14):
        if x == 7: continue
        startX = x * TRIANGLE_WIDTH + TRIANGLE_WIDTH / 2
        tri = Triangle(startX, BOARD_HEIGHT, LIGHT_TRIANGLES if is_dark else DARK_TRIANGLES, TRIANGLE_WIDTH, TRIANGLE_HEIGHT, False, 0)
        is_dark = not is_dark
        tris.append(tri)
        
    for idx, tri in enumerate(tris):
        board = get_board()
        n = math.fabs(board[idx])
        tri.piece_color = LIGHT_PIECE if board[idx] > 0 else DARK_PIECE
        tri.number_of_pieces = n

    return tris

class Triangle:
    def __init__(self, x: int, y: int, color: tuple, width: int, height: int, is_upside_down: bool, number_of_pieces: int, piece_color = (0, 0, 0)):
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.height = height
        self.is_upside_down = is_upside_down
        self.number_of_pieces = number_of_pieces
        self.piece_color = piece_color
        self.selected = False
            
    def draw(self):
        p1 = (self.x - self.width / 2, self.y)
        p2 = (self.x + self.width / 2, self.y)
        
        tmp = self.height if not self.is_upside_down else SCREEN_HEIGHT - self.height
        p3 = (self.x, tmp)
        self.rect = draw_polygon(layer.game_board_layer, self.color, [p1, p2, p3])
        
        count = 0
        pieceX = self.x
        mult = -1 if self.is_upside_down else 1
        pieceY = self.y + mult * PIECE_RADIUS
        while count < self.number_of_pieces:
            draw_circle(layer.pieces_layer, self.piece_color, pieceX, pieceY, PIECE_RADIUS, 1)
            pieceY += mult * 2 * PIECE_RADIUS
            count += 1
            
    def select(self):
        pieceX = self.x
        mult = -1 if self.is_upside_down else 1
        pieceY = self.y + mult * PIECE_RADIUS + (self.number_of_pieces - 1) * mult * 2 * PIECE_RADIUS
        
        draw_transparent_circle(layer.highlight_pieces_layer, (0, 255, 0, 128), pieceX, pieceY, PIECE_RADIUS)        
        
    def highlight(self):
        p1 = (self.x - self.width / 2, self.y)
        p2 = (self.x + self.width / 2, self.y)
        
        tmp = self.height if not self.is_upside_down else SCREEN_HEIGHT - self.height
        p3 = (self.x, tmp)
        draw_transparent_polygon(layer.triangle_highlight_layer, (0, 255, 0, 128), [p1, p2, p3])
        
    def check_color(self, is_light_on_turn):
        if self.number_of_pieces <= 1: return True
        if is_light_on_turn and self.piece_color == DARK_PIECE: return False
        if not is_light_on_turn and self.piece_color == LIGHT_PIECE: return False
        return True