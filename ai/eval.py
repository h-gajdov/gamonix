import game_logic.board as brd
from ui.colors import *
from math import fabs
from ai.config import configs

def evaluate_points(board, color):
    light = 0
    dark = 0
    for idx in range(1, 25):
        value = board[idx]
        if value < 0: dark += idx
        elif value > 0: light += 25 - idx
    
    return light - dark if color == DARK_PIECE else dark - light

def block_counts(board):
    def count_blocks(positive):
        prevWasBlock = False
        result = []
        for idx, value in enumerate(board):
            if idx == 0 or idx == 25: continue

            if positive and value <= 0 or not positive and value >= 0: 
                prevWasBlock = False
                continue

            if fabs(value) < 2: 
                prevWasBlock = False
                continue

            if prevWasBlock: result[-1] += 1
            else: result.append(1) 
            prevWasBlock = True
        return result

    light = count_blocks(True)
    dark = count_blocks(False)

    return {'light': light, 'dark': dark}

def blot_positions(board):
    light = []
    dark = []
    for idx, value in enumerate(board):
        if value == 1: light.append(idx)
        elif value == -1: dark.append(idx)

    return {'light': light, 'dark': dark}
    
def evaluate_position_of_player(board, player_color):
    config = configs['trained']
    score = 0
    in_block = False
    block_count = 0
    
    bt = config.blots_threshold
    bf = config.blots_factor
    bfp = config.blots_factor_passed
    cbf = config.connected_blocks_factor
    bps = config.blocked_point_score
    
    other_color = LIGHT_PIECE if player_color == DARK_PIECE else DARK_PIECE
    
    my_most_distant = brd.get_most_distant_piece(player_color)
    opponent_most_distant = 25 - brd.get_most_distant_piece(other_color) #transformed to current player POV
    
    all_passed = True
    if my_most_distant > opponent_most_distant:
        for i in range(1, 25):
            pointNo = i if player_color == DARK_PIECE else 25 - i
            all_passed = pointNo < opponent_most_distant
            my_color = player_color == DARK_PIECE and board[i] < 0 or player_color == LIGHT_PIECE and board[i] > 0 
            if not my_color: continue
            
            if board[pointNo] != 0 and abs(board[pointNo]) > 1: #is block
                if in_block: block_count += 1   
                else: block_count = 1
                in_block = True
            else:
                if in_block:
                    score += (block_count * bps) ** cbf
                    block_count = 0
                
                in_block = False
                if abs(board[pointNo]) == 1 and pointNo < bt:
                    coef = bfp if all_passed else bf
                    score -= pointNo / coef 
                    
        #end of loop
        if in_block:
            score += (block_count * bps) ** cbf
        
        if all_passed:
            score += evaluate_points(board, player_color) * config.run_or_block_factor
        
    else: #passed each other
        pieces_in_base = brd.PiecesInBaseCounter.get_number_of_pieces_in_base()
        count_in_base = pieces_in_base.dark if player_color == DARK_PIECE else pieces_in_base.light
        count_in_other = pieces_in_base.dark_points_other_base if player_color == DARK_PIECE else pieces_in_base.light_points_other_base
        
        score += count_in_base * 100
        score += count_in_other * 50
    
    return score + evaluate_points(board, player_color)