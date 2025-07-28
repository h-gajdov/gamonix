import random
import game_logic.player as player
import ai.random_move as rand_agent
import game_logic.board as brd
from colors import *
from ai.agent import Agent

dice_values = (1, 1)
dice_values_ui = (1, 1)
players = [rand_agent.RandomAI(DARK_PIECE), rand_agent.RandomAI(LIGHT_PIECE)]
current_player_index = 0
current_player = players[current_player_index]

def roll_dice():
    global dice_values_ui
    value1 = random.randint(1, 6)
    value2 = random.randint(1, 6)
    if value1 != value2: result = [value1, value2]
    else: result = [value1] * 4
    
    result = current_player.handle_distant_dice_values(result)
    dice_values_ui = (value1, value2)
    player.Player.set_dice_values(tuple(result))
    
    # print(current_player.get_available_moves())
    return tuple(result)

def player_has_moves():
    global current_player
    return len(current_player.get_available_moves()) != 0

def change_player():
    global current_player_index, current_player, players, dice_values
    current_player_index = (current_player_index + 1) % len(players)
    current_player = players[current_player_index]

    # if isinstance(current_player, Agent):
    #     print(current_player.move())

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
        player.Player.set_dice_values(dice_values)

    current_player_index = brd.player_fen
    current_player = players[current_player_index]
    
    # if isinstance(current_player, Agent):
    #     print(current_player.move())
    
    if not player_has_moves(): 
        # print("NO LEGAL MOVES")
        change_player()