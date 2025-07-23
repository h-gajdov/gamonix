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
    fen = '2W:0:0:0:0:5B:0:3B:0:0:0:5W:5B:0:0:0:3W:0:4W:1W:0:0:0:2B:0:0:0:0:0:0:0'
    # fen = '3B:3B:3B:2B:2B:2B:0:0:0:0:0:0:0:0:0:0:0:0:2W:2W:2W:3W:3W:3W:0:0:0:0:0:0:0'
    board, light, dark = convert_fen_to_board(fen)
    set_off_pieces(light, dark)
        
def get_board():
    return board

def get_off_pieces():
    return { "light": number_of_light_pieces_off, "dark": number_of_dark_pieces_off }

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
        if move + position < 1 or move + position > 24: continue
        if fabs(board[move + position]) > 1 and board[position] * board[move + position] < 0: continue
        
        result.append(move + position)
        
    return result