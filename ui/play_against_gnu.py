import subprocess
import re
import os
import random
import game_logic.extract_gnu as gnu
from game_logic.move import Move
from dotenv import load_dotenv
from ai.agent import AdaptiveBeamAgent
from ai.config import configs
from colors import *

def roll_dice_plain():
    value1 = random.randint(1, 6)
    value2 = random.randint(1, 6)
    return (value1, value2)

game_finished = False
dice_values = (0, 0)
while dice_values[0] == dice_values[1]: dice_values = roll_dice_plain() #with gnu you can't start with duplicates

agent = AdaptiveBeamAgent(DARK_PIECE, configs['trained'], 2)
env = load_dotenv(dotenv_path='.env')
path_to_gnubg = os.getenv('PATH_TO_GNUBG')

gnubg = subprocess.Popen(
    [path_to_gnubg, '--tty'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1
)

gnubg.stdin.write(f'new game\n')
gnubg.stdin.write(f'{dice_values[0]} {dice_values[1]}\n')
# gnubg.stdin.write('set board Qx8mJBgHAAAAAA')
gnubg.stdin.flush()
print(dice_values)

def send_command(command):
    gnubg.stdin.write(command + "\n")
    gnubg.stdin.flush()

def read_line():
    return gnubg.stdout.readline().strip()

def get_player_on_turn():
    send_command('show turn')
    return read_line().split(' ')[0]

def get_position_id():
    send_command('show board')
    return read_the_board(False)

#read the board
def read_the_board(print_board=False):
    global game_finished
    position_id = ''
    while not game_finished:
        line = gnubg.stdout.readline().strip()
        if line == 'Session complete': 
            game_finished = True
        elif 'resign' in line:
            send_command('accept')
        
        id = re.search(r'Position ID: .*', line)
        if id: position_id = id.group().split(':')[1].strip()
        
        if print_board: print(line) 
        if re.search(r'X: [aA-zZ]*', line): 
            break
        
    if not game_finished: gnubg.stdout.readline() # a line that is returned after the board
    return position_id

read_the_board()
while not game_finished:
    send_command('roll')
    send_command(f'{dice_values[0]} {dice_values[1]}')
    read_the_board(True)
    if game_finished: break

    position_id = get_position_id()
    player_on_turn = get_player_on_turn()
    if not position_id: continue
    board = gnu.decode_position(position_id, player_on_turn == 'gamonix')
    print("PLAYER ON TURN:", player_on_turn)
    moves = None
    if player_on_turn == 'gnubg': pass
        # agent.color = LIGHT_PIECE
        # if dice_values[0] == dice_values[1]: dice_values = tuple([dice_values[0]] * 4)
        # moves = Move.parse_moves_to_gnu_format(agent.move(board, dice_values), reverse=True)
        # send_command(f"move {moves.strip()}")
    elif player_on_turn == 'gamonix':
        agent.color = DARK_PIECE
        if dice_values[0] == dice_values[1]: dice_values = tuple([dice_values[0]] * 4)
        moves = Move.parse_moves_to_gnu_format(agent.move(board, dice_values))
        send_command(f"move {moves.strip()}")
    else:     
        dice_values = roll_dice_plain()
        continue

    print(moves)
    read_the_board(True)

    dice_values = roll_dice_plain()