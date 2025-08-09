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
    
    def gnu_format(self, reverse):
        if self.source_point == 0 or self.source_point == 25: return ''
        
        if not reverse:
            source = self.source_point
            destination = self.destination_point
        else:
            source = 25 - self.source_point
            destination = 25 - self.destination_point
        
        if destination == 0 or destination == 25: destination = 'off'
        
        if self.source_point < 0 or self.source_point > 24: result = f'bar/{destination}'
        else: result = f"{source}/{destination}"
        return result
    
    @staticmethod
    def parse_moves_to_gnu_format(moves: list, reverse=False):
        gnu_format = ''
        for move in moves:
            gnu_format += f"{move.gnu_format(reverse)} "
        return gnu_format