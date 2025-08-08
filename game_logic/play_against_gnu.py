import subprocess
import re
import os
import extract_gnu as gnu
from dotenv import load_dotenv


env = load_dotenv(dotenv_path='../.env')
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
gnubg.stdin.write('roll 3 5\n')
gnubg.stdin.flush()

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
    position_id = ''
    while True:
        line = gnubg.stdout.readline().strip()
        
        id = re.search(r'Position ID: .*', line)
        if id: position_id = id.group().split(':')[1].strip()
        
        if print_board: print(line) 
        if re.search(r'X: [aA-zZ]*', line): 
            break
        
    gnubg.stdout.readline() # a line that is returned after the board
    return position_id

read_the_board()
read_the_board(True)
print(get_player_on_turn())
position_id = get_position_id()
print(gnu.decode_position(position_id))
send_command("move 8/3 6/3")
read_the_board(True)
position_id = get_position_id()
print(gnu.decode_position(position_id))

send_command('roll')
send_command('6 1')
read_the_board(True)
send_command('move 13/7 8/7')
read_the_board(True)