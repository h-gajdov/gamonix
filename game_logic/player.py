import game_logic.board as brd
from game_logic.move import Move
from ui.colors import *

def get_destinations_from_source_point(source_idx, source_value, mult):
    visited = []
    destinations = []
    for value in Player.dice_values:
        if value in visited: continue
        visited.append(value)
        
        pieces_in_base = brd.PiecesInBaseCounter.get_number_of_pieces_in_base()
        
        target = source_idx + mult * value        
        if target > 25: continue
        if target < 0 or target >= len(brd.board): continue
        if target == 25 and pieces_in_base.light != 15: continue
        if target == 0 and pieces_in_base.dark != 15: continue
        
        if source_value * brd.board[target] >= 0 or brd.board[target] == 1:
            destinations.append(target)
    return destinations

class Player:
    dice_values = (1, 1)
    def set_dice_values(value: tuple):
        Player.dice_values = value
    
    def __init__(self, color):
        self.color = color

    def get_available_moves(self):
        result = []
        
        def get_moves(bigger_than_zero):
            taken = False
            if bigger_than_zero:
                mult = 1
                taken = brd.board[26] != 0
                source = 0
            else:
                mult = -1
                taken = brd.board[27] != 0
                source = 25
            
            if taken:
                point_idx = 26 if bigger_than_zero else 27
                destinations = get_destinations_from_source_point(source, brd.board[point_idx], mult)
                result.extend([Move(point_idx, dest) for dest in destinations])
                return
            
            for idx, point in enumerate(brd.board):
                if (bigger_than_zero and point > 0) or (not bigger_than_zero and point < 0):
                    destinations = get_destinations_from_source_point(idx, brd.board[idx], mult)
                    result.extend([Move(idx, dest) for dest in destinations])
        
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