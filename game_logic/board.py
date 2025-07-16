from game_logic.fen import *
board = [0] * 24

number_of_light_pieces_off = 0
number_of_dark_pieces_off = 0

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
    
def get_available_moves_for_position(position: int, dice_values: tuple):
    indices = []
    if dice_values[0] == dice_values[1]:
        indices.extend([mult * dice_values[0] + position for mult in range(1, 5)])
    else:
        idx1 = dice_values[0] + position
        idx2 = dice_values[1] + position
        idx3 = dice_values[0] + dice_values[1] + position
        indices = [idx1, idx2, idx3]
    return [idx for idx in indices if idx < 24]