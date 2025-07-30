import game_logic.player as player
import game_logic.board as brd
import random
from ui.colors import *
from abc import ABC, abstractmethod

class Agent(player.Player):
    def __init__(self, color):
        super().__init__(color)
    
    @abstractmethod
    def move(self): pass
    
class RandomAgent(Agent):
    def __init__(self, color):
        super().__init__(color)
        
    def move(self, board):
        available_moves = self.get_available_moves(board)
        if not available_moves: return None
        return random.choice(available_moves)
    
class GreedyAgent(Agent):
    def __init__(self, color):
        super().__init__(color)
    
    def move(self, board,):
        available_moves = self.get_available_moves(board)
        available_moves = sorted(available_moves, key=lambda x: x.source_point)
        if self.color == DARK_PIECE: available_moves.reverse()
        best_move = max(available_moves, key=lambda x: x.evaluate())
        return best_move