import math
import game_logic.board as brd

from ui.colors import *
from ai.config import configs

def evaluate_points(board, color):
    light = 0
    dark = 0
    for idx in range(0, 28):
        value = board[idx]
        if idx == 27 and value != 0: 
            dark += 25
            continue
        if idx == 26 and value != 0:
            light += 25
            continue
         
        if value < 0: dark += idx * abs(value)
        elif value > 0: light += (25 - idx) * abs(value)
    
    return light - dark if color == DARK_PIECE else dark - light
    
def evaluate_position_of_player(board, player_color, config):
    # config = configs['trained']
    score = 0
    in_block = False
    block_count = 0

    bt = config.blots_threshold
    bf = config.blots_factor
    bfp = config.blots_factor_passed
    cbf = config.connected_blocks_factor
    bps = config.blocked_point_score
    # tpf = config.taking_pieces_factor
    
    other_color = LIGHT_PIECE if player_color == DARK_PIECE else DARK_PIECE
    
    my_most_distant = brd.get_most_distant_piece(player_color, board)
    opponent_most_distant = 25 - brd.get_most_distant_piece(other_color, board) #transformed to current player POV

    all_passed = True
    # Check this. It might overfit the solution
    # if player_color == DARK_PIECE:
    #     score -= abs(board[27]) * tpf 
    # elif player_color == LIGHT_PIECE:
    #     score -= abs(board[26]) * tpf

    if my_most_distant > opponent_most_distant:
        for i in range(1, 25): 
            point_no = i if player_color == DARK_PIECE else 25 - i
            my_color = player_color == DARK_PIECE and board[i] < 0 or player_color == LIGHT_PIECE and board[i] > 0
            
            all_passed = point_no > opponent_most_distant                        
                        
            if my_color and abs(board[i]) > 1: #is block
                if in_block: block_count += 1   
                else: block_count = 1
                in_block = True
            else:
                if in_block:
                    score += (block_count * bps) ** cbf
                    block_count = 0
                
                if my_color: in_block = False
                if my_color and abs(board[i]) == 1 and point_no < bt:
                    coef = bfp if all_passed else bf
                    score -= point_no / coef
                    
        #end of loop
        if in_block:
            score += (block_count * bps) ** cbf
        
        if all_passed:
            score += evaluate_points(board, player_color) * config.run_or_block_factor
    
    else: #passed each other
        pieces_in_base = brd.PiecesInBaseCounter.get_number_of_pieces_in_base(board)
        count_in_base = pieces_in_base.dark if player_color == DARK_PIECE else pieces_in_base.light

        #Pieces in base heuristic
        score += count_in_base * 100

        #Pieces in off section heuristic
        player_off_section_idx = 0 if player_color == DARK_PIECE else 25
        player_number_of_off_pieces = abs(board[player_off_section_idx])
        opponent_number_of_off_pieces = abs(board[25 - player_off_section_idx])
        score += (player_number_of_off_pieces - opponent_number_of_off_pieces) * 100


    return score + evaluate_points(board, player_color)