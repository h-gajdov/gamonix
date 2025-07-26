import game_logic.board as brd
from game_logic.move import Move
from ui.colors import *

def get_destinations_from_source_point(source_idx, mult):
    visited = []
    destinations = []
    for value in Player.dice_values:
        if value in visited: continue
        visited.append(value)
                
        target = source_idx + mult * value
        if target >= 0 and brd.board[source_idx] * brd.board[target] >= 0:
            destinations.append(target)
    return destinations

class Player:
    dice_values = (1, 1)
    def set_dice_values(value: tuple):
        Player.dice_values = value
    
    def __init__(self, color):
        self.color = color
        self.available_moves = self.get_available_moves()

    def get_available_moves(self):
        result = []
        
        def get_moves(bigger_than_zero):
            for idx, point in enumerate(brd.board):
                if (bigger_than_zero and point > 0) or (not bigger_than_zero and point < 0):
                    mult = 1 if bigger_than_zero else -1
                    destinations = get_destinations_from_source_point(idx, mult)
                    result.append([Move(idx, dest) for dest in destinations])
        
        if self.color == LIGHT_PIECE:
            get_moves(bigger_than_zero=True)
        else:
            get_moves(bigger_than_zero=False)
            
        return result
    
    def is_light(self):
        return self.color == LIGHT_PIECE
    
    def handle_distant_dice_values(self, array):
        result = array[:]
        max_value = max(result)
        most_distant = brd.get_most_distant_piece(self.is_light())
        if max_value > most_distant:
            result = [value if value <= most_distant else most_distant for value in result]
        return result