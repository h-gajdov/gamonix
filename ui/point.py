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