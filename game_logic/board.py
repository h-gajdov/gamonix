from math import fabs
from game_logic.fen import *
from ui.colors import *
from random import randint
board = [0] * 28
player_fen = 0
dice_fen = (1, 1)

def update_board_array(points):
    for idx, point in enumerate(points):
        board[idx] = len(point.pieces) if point.get_color_of_last_piece() == LIGHT_PIECE else -len(point.pieces)
    # print(board)

def initialize_board_array():
    global board, player_fen, dice_fen
    # 0-23 pieces:light_taken:dark_taken:light_off:dark_off:dice_1:dice_2:current_player_index
    first_rand = randint(0, 1)
    fen = f'2W:0:0:0:0:5B:0:3B:0:0:0:5W:5B:0:0:0:3W:0:5W:0:0:0:0:2B:0:0:0:0:0:0:{first_rand}'
    board, dice_fen, player_fen = convert_fen_to_board(fen)
    
def get_available_moves(dice_values: tuple, color: tuple):
    indices = []
    is_light_on_turn = color == LIGHT_PIECE
    turn_multiplier = 1 if is_light_on_turn else -1
    
    if len(dice_values) > 1 and dice_values[0] == dice_values[1]:
        indices.extend([turn_multiplier * dice_values[0]] * len(dice_values))
    else:
        indices = [turn_multiplier * value for value in dice_values]
    return indices

def get_available_points_from_position(position, board, dice_values, color, is_taken=False):
    is_light_on_turn = color == LIGHT_PIECE

    moves = get_available_moves(dice_values, color)
    result = []
    visited = []
    for move in moves:
        if move in visited: continue
        pieces_in_base = PiecesInBaseCounter.get_number_of_pieces_in_base(board)

        visited.append(move)
        target = move + position
        if target < 0 or target > 25: continue

        if pieces_in_base.light != 15 and target == 25: continue
        if pieces_in_base.dark != 15 and target == 0: continue
        
        if fabs(board[target]) > 1: 
            if is_taken: 
                if is_light_on_turn and board[26] * board[target] < 0: continue
                if not is_light_on_turn and board[27] * board[target] < 0: continue
            elif board[position] * board[target] < 0: continue

        result.append(target)
    return result

def get_most_distant_piece(color: tuple, brd):
    if color == LIGHT_PIECE:
        for idx in range(1, 28):
            if brd[idx] > 0: return 25 - idx if idx < 26 else 25
    else:
        for idx in range(27, 0, -1):
            if brd[idx] < 0: return idx if idx < 26 else 25
    return 0

def get_delta(source_pos, destination_pos):
    delta = fabs(source_pos - destination_pos) 
    if source_pos == 26: delta = fabs(0 - destination_pos)
    elif source_pos == 27: delta = fabs(25 - destination_pos)
    return delta

def handle_distant_dice_values(dice_values, board, color, most_distant=None):
    if not most_distant: most_distant = get_most_distant_piece(color, board)
    result = [value if value <= most_distant else most_distant for value in dice_values]
    return tuple(result)

def update_dice_values(dice_values, move, color, board):
    most_distant = get_most_distant_piece(color, board)
    dice_values = handle_distant_dice_values(dice_values, board, color, most_distant)
    
    delta = get_delta(move.source_point, move.destination_point)
    if delta > most_distant: delta = most_distant
    
    dice_values = list(dice_values)
    dice_values.remove(delta)
    return tuple(dice_values)

def move_piece(move, board, dice_values, player_color):
    most_distant = get_most_distant_piece(player_color, board)
    dice_values = tuple([value if value <= most_distant else most_distant for value in dice_values])
    
    dice_values = update_dice_values(dice_values, move, player_color, board)
    if player_color == DARK_PIECE:
        if board[move.destination_point] * board[move.source_point] < 0:
            board[26] += 1
            board[move.destination_point] = 0
        
        board[move.source_point] += 1
        board[move.destination_point] -= 1
    else:
        if board[move.destination_point] * board[move.source_point] < 0:
            board[27] -= 1
            board[move.destination_point] = 0
        
        board[move.source_point] -= 1
        board[move.destination_point] += 1
    return board, dice_values

def get_all_unique_dice_values():
    return [(1, 1, 1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6),
            (2, 2, 2, 2), (2, 3), (2, 4), (2, 5), (2, 6),
            (3, 3, 3, 3), (3, 4), (3, 5), (3, 6),
            (4, 4, 4, 4), (4, 5), (4, 6),
            (5, 5, 5, 5), (5, 6),
            (6, 6, 6, 6)]

class PiecesInBaseCounter:
    def __init__(self, light, dark, light_points_other_base, dark_points_other_base):
        self.light = light
        self.dark = dark
        self.light_points_other_base = light_points_other_base
        self.dark_points_other_base = dark_points_other_base

    @staticmethod
    def get_number_of_pieces_in_base(board):
        light_count = 0
        dark_count = 0
        light_other = 0
        dark_other = 0
        for idx in range(19, 26):
            if board[idx] > 0: light_count += board[idx]
            elif board[idx] < 0: dark_other += abs(board[idx])
        for idx in range(0, 7):
            if board[idx] < 0: dark_count += abs(board[idx])
            elif board[idx] > 0: light_other += board[idx]

        light_other += board[26]
        dark_other += -board[27]

        return PiecesInBaseCounter(light_count, dark_count, light_other, dark_other)