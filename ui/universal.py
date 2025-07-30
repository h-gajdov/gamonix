import random
import ai.agent as agent
import game_logic.board as brd
from colors import *

dice_values = (1, 1)
dice_values_ui = (1, 1)
players = [agent.DepthGreedyAgent(DARK_PIECE), agent.DepthGreedyAgent(LIGHT_PIECE)]
current_player_index = 0
current_player = players[current_player_index]

def roll_dice():
    global dice_values_ui
    value1 = random.randint(1, 6)
    value2 = random.randint(1, 6)
    if value1 != value2: result = [value1, value2]
    else: result = [value1] * 4
    
    result = current_player.handle_distant_dice_values(result, brd.board)
    dice_values_ui = (value1, value2)
    return tuple(result)

def player_has_moves():
    global current_player, dice_values
    return len(current_player.get_available_moves(brd.board, dice_values)) != 0

def change_player():
    global current_player_index, current_player, players, dice_values
    current_player_index = (current_player_index + 1) % len(players)
    current_player = players[current_player_index]

    # if isinstance(current_player, agent.Agent):
        # print(current_player.move())

    dice_values = roll_dice()
    if not player_has_moves(): 
        # print("NO LEGAL MOVES")
        change_player()
    
def start_game():
    global dice_values, dice_values_ui, current_player_index, current_player
    if 0 in brd.dice_fen: 
        dice_values = roll_dice()
    else:
        dice_values = dice_values_ui = brd.dice_fen
        
    current_player_index = brd.player_fen
    current_player = players[current_player_index]
    
    # if isinstance(current_player, agent.Agent):
        # print(current_player.move())
    
    if not player_has_moves(): 
        # print("NO LEGAL MOVES")
        change_player()