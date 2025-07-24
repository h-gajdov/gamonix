from math import fabs
from game_logic.fen import *
from ui.colors import *
board = [0] * 27

number_of_light_pieces_off = 0
number_of_dark_pieces_off = 0
number_of_taken_light_pieces = 0
number_of_taken_dark_pieces = 0

available_moves = {}

def update_board_array(points):
    for idx, point in enumerate(points):
        board[idx] = len(point.pieces) if point.get_color_of_last_piece() == LIGHT_PIECE else -len(point.pieces)
    print(board)

def initialize_board_array():
    global board
    # fen = '2W:0:0:0:0:5B:0:3B:0:0:0:5W:5B:0:0:0:3W:0:5W:0:0:0:0:2B:0:0:0:0:0:0:0'
    fen = '3B:3B:3B:2B:2B:1B:1B:0:0:0:0:0:0:0:0:0:0:0:2W:2W:2W:3W:3W:3W:0:0:0:0:0:0:0'
    board, light, dark = convert_fen_to_board(fen)
    set_off_pieces(light, dark)
        
def get_board():
    return board

def set_off_pieces(light, dark):
    global number_of_light_pieces_off, number_of_dark_pieces_off
    number_of_light_pieces_off = light
    number_of_dark_pieces_off = dark
    
def get_available_moves(dice_values: tuple, is_light_on_turn: bool):
    indices = []
    turn_multiplier = 1 if is_light_on_turn else -1
    
    if len(dice_values) > 1 and dice_values[0] == dice_values[1]:
        indices.extend([turn_multiplier * mult * dice_values[0] for mult in range(1, 5)])
    else:
        indices = [turn_multiplier * value for value in dice_values]
    return indices

def get_available_points_from_position(position, dice_values, is_light_on_turn):
    moves = get_available_moves(dice_values, is_light_on_turn)
    result = []
    for move in moves:
        target = move + position
        if target < 0 or target > 25: continue
        if fabs(board[target]) > 1 and board[position] * board[target] < 0: continue
        
        result.append(target)

    return result

def get_most_distant_piece(light: bool):
    if light:
        for idx in range(1, 25):
            if board[idx] > 0: return 25 - idx
    else:
        for idx in range(24, 0, -1):
            if board[idx] < 0: return idx

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