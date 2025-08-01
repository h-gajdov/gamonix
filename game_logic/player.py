import game_logic.board as brd
from game_logic.move import Move
from ui.colors import *

def get_destinations_from_source_point(source_idx, board, dice_values, player_color, is_taken):
    return brd.get_available_points_from_position(source_idx, board, dice_values, player_color, is_taken)

class Player:
    def __init__(self, color):
        self.color = color

    def get_available_moves(self, board, dice_values, color=None):
        if not color: color = self.color
        dice_values = brd.handle_distant_dice_values(dice_values, board, color)
        result = []
        
        taken = False
        is_light = color == LIGHT_PIECE
        if is_light:
            mult = 1
            taken = brd.board[26] != 0
            source = 0
        else:
            mult = -1
            taken = brd.board[27] != 0
            source = 25
            
        if taken:
            point_idx = 26 if is_light else 27
            destinations = get_destinations_from_source_point(source, board, dice_values, color, taken)
            result.extend([Move(point_idx, dest, board, dice_values, color) for dest in destinations])
            return result
            
        for idx, point in enumerate(board):
            if (is_light and point > 0) or (not is_light and point < 0):
                destinations = get_destinations_from_source_point(idx, board, dice_values, color, taken)
                result.extend([Move(idx, dest, board, dice_values, color) for dest in destinations])
        
        return result