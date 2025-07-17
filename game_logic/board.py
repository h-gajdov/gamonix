from game_logic.fen import *
board = [0] * 24

number_of_light_pieces_off = 0
number_of_dark_pieces_off = 0

available_moves = {}

def initialize_board_array():
    global board
    fen = '2W:0:0:0:0:5B:0:3B:0:0:0:5W:5B:0:0:0:3W:0:5W:0:0:0:0:2B:0:0:0:0:0:0:0'
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
    
def get_available_moves_for_position(dice_values: tuple, is_light_on_turn: bool):
    indices = []
    turn_multiplier = 1 if is_light_on_turn else -1
    if dice_values[0] == dice_values[1]:
        indices.extend([turn_multiplier * mult * dice_values[0] for mult in range(1, 5)])
    else:
        idx1 = turn_multiplier * dice_values[0]
        idx2 = turn_multiplier * dice_values[1]
        idx3 = turn_multiplier * (dice_values[0] + dice_values[1])
        indices = [idx1, idx2, idx3]
    return [idx for idx in indices if idx != 0]