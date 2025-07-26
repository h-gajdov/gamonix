import game_logic.player as player
from math import fabs
from game_logic.fen import *
from ui.colors import *
board = [0] * 28
player_fen = 0
dice_fen = (1, 1)

def update_board_array(points):
    for idx, point in enumerate(points):
        board[idx] = len(point.pieces) if point.get_color_of_last_piece() == LIGHT_PIECE else -len(point.pieces)
    print(board)

def initialize_board_array():
    global board, player_fen, dice_fen
    # 0-23 pieces:light_taken:dark_taken:light_off:dark_off:dice_1:dice_2:current_player_index
    fen = '2W:0:0:0:0:5B:0:3B:0:0:0:5W:5B:0:0:0:3W:0:5W:0:0:0:1B:1B:0:0:0:0:0:0:0'
    # fen = '2B:2B:2B:2B:2B:2B:3B:0:0:0:0:0:0:0:0:0:0:3W:2W:2W:2W:2W:2W:2w:0:0:0:0:0:0:0'
    board, dice_fen, player_fen = convert_fen_to_board(fen)
        
def get_board():
    return board
    
def get_available_moves(dice_values: tuple, is_light_on_turn: bool):
    indices = []
    turn_multiplier = 1 if is_light_on_turn else -1
    
    if len(dice_values) > 1 and dice_values[0] == dice_values[1]:
        indices.extend([turn_multiplier * dice_values[0]] * len(dice_values))
    else:
        indices = [turn_multiplier * value for value in dice_values]
    return indices

def get_available_points_from_position(position, dice_values, is_light_on_turn, is_taken=False):
    moves = get_available_moves(dice_values, is_light_on_turn)
    result = []
    visited = []
    for move in moves:
        if move in visited: continue
        pieces_in_base = PiecesInBaseCounter.get_number_of_pieces_in_base()

        visited.append(move)
        target = move + position
        if target < 0 or target > 25: continue

        if pieces_in_base.light != 15 and target == 25: continue
        if pieces_in_base.dark != 15 and target == 0: continue
        
        if fabs(board[target]) > 1: 
            if is_taken: 
                if is_light_on_turn and board[26] * board[target] < 0: continue
                if not is_light_on_turn and board[27] * board[target] < 0: continue
            elif not is_taken and board[position] * board[target] < 0: continue
        
        result.append(target)

    return result

def get_most_distant_piece(light: bool):
    if light:
        for idx in range(1, 25):
            if board[idx] > 0: return 25 - idx
    else:
        for idx in range(24, 0, -1):
            if board[idx] < 0: return idx
    return 0

def is_available_moves_empty():
    available_moves = player.Player.get_available_moves()

class PiecesInBaseCounter:
    def __init__(self, light, dark):
        self.light = light
        self.dark = dark
    
    def get_number_of_pieces_in_base():
        light_count = 0
        dark_count = 0
        for idx in range(19, 26):
            if board[idx] > 0: light_count += board[idx]
        for idx in range(0, 7):
            if board[idx] < 0: dark_count += int(fabs(board[idx]))
        
        return PiecesInBaseCounter(light_count, dark_count)