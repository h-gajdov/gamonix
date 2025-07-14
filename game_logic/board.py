from game_logic.fen import *
board = [0] * 24

def initialize_board_array():
    global board
    fen = '2W:0:0:0:0:5B:0:3B:0:0:0:5W:5B:0:0:0:3W:0:5W:0:0:0:0:2B:0:0:0:0:0:0:0'
    board = convert_fen_to_board(fen)
        
def get_board():
    return board