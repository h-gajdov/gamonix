import game_logic.board as brd
from ai.eval import evaluate_position_of_player
from ui.colors import *

class Move:
    def __init__(self, source_point: int, destination_point: int, board: list, dice_values: tuple, color: tuple):
        self.source_point = source_point
        self.destination_point = destination_point
        self.board = board[:]
        self.dice_values = dice_values
        self.color = color
    
    def evaluate(self, config):
        result_board, _ = brd.move_piece(self, self.board[:], self.dice_values, self.color) 
        return evaluate_position_of_player(result_board, self.color, config)
    
    def __repr__(self):
        return f"{self.source_point} -> {self.destination_point}"