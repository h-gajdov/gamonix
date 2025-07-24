import game_logic.board as brd
from abc import ABC, abstractmethod
from piece import Piece
from colors import *

class Point(ABC):
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.rect = None
        self.is_highlighted = False
        self.pieces = []

    @abstractmethod
    def draw(self): pass
    
    @abstractmethod
    def draw_pieces(self): pass
    
    def set_highlight(self, value):
        self.is_highlighted = value
        
    def add_piece(self, n = 1, piece_color=BLACK):
        while n:
            self.pieces.append(Piece(color=piece_color))
            n -= 1
            
    def remove_specific_piece(self, piece):
        self.pieces.remove(piece)
    
    def add_specific_piece(self, piece):
        self.pieces.append(piece)
        
    def move_piece_to(self, destination, index=-1):
        self.pieces[index].move_between_points(self, destination)
        
    def check_pieces_color(self, other):
        if self.pieces: return self.pieces[-1].color == other.pieces[-1].color
        else: return True
    
    def take(self, idx, points):
        if brd.board[idx] < 0:
            self.move_piece_to(points[27])
        else:
            self.move_piece_to(points[26])
    
    def get_color_of_last_piece(self):
        if not self.pieces: return None
        return self.pieces[-1].color 