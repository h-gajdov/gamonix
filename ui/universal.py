import random
import ai.agent as agent
import game_logic.board as brd
from ui.colors import *
from ai.config import configs

dice_values = (1, 1)
dice_values_ui = (1, 1)
players = [agent.AdaptiveBeamAgent(color=DARK_PIECE, config=configs['trained'], play_opening=True, max_depth=2), 
            agent.AdaptiveBeamAgent(color=DARK_PIECE, config=configs['trained'], play_opening=True, max_depth=2)]
current_player_index = 0
current_player = players[current_player_index]
opening = True

STARTING_BOARD = [0, 2, 0, 0, 0, 0, -5, 0, -3, 0, 0, 0, 5, -5, 0, 0, 0, 3, 0, 5, 0, 0, 0, 0, -2, 0, 0, 0]

def roll_dice():
    global dice_values_ui
    value1 = random.randint(1, 6)
    value2 = random.randint(1, 6)
    if value1 != value2: result = [value1, value2]
    else: result = [value1] * 4
    
    result = brd.handle_distant_dice_values(result, brd.board, current_player.color)
    dice_values_ui = (value1, value2)
    return tuple(result)

def player_has_moves():
    global current_player, dice_values
    return len(current_player.get_available_moves(brd.board, dice_values)) != 0

def change_player():
    global current_player_index, current_player, players, dice_values, opening
    
    opening = False
    if isinstance(current_player, agent.CachingExpectimaxAgent): 
        current_player.clear_cache()
    
    current_player_index = (current_player_index + 1) % len(players)
    current_player = players[current_player_index]
    
    dice_values = roll_dice()
    if not player_has_moves():
        change_player()
    
def start_game():
    global dice_values, dice_values_ui, current_player_index, current_player, opening

    brd.initialize_board_array()
    opening = brd.board == STARTING_BOARD
    
    if 0 in brd.dice_fen: 
        dice_values = roll_dice()
    else:
        dice_values = dice_values_ui = brd.dice_fen
        
    current_player_index = brd.player_fen
    current_player = players[current_player_index]

    if not player_has_moves():
        change_player()

def create_new_game():
    start_game()  # Initializes global vars, but you may need to isolate
    return brd.board.copy(), dice_values[:], current_player, current_player_index