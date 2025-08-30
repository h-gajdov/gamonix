import sys
import time
import sounds
import universal
import game_logic.board as brd
import debug.time_passed as tp

from ui.colors import *
from ai.agent import Agent
from ai.config import configs

class GameInfo:
    def __init__(self, players, winner, move_history):
        self.players = players
        self.winner = winner
        self.move_history = move_history

    def __repr__(self):
        return f"Players: {self.players}\nWinner: {self.winner}\nMoves: {len(self.move_history)}\nMove history: {self.move_history}"

line = ''
dark = 0
light = 0
save_to_file = '-s' in sys.argv

if '--agents' in sys.argv:
    i = sys.argv.index('--agents')
    print(sys.argv, i)
    agent_1 = Agent.get_agent_from_name(sys.argv[i + 1], LIGHT_PIECE, configs['41gensnodoubles'], True)
    agent_2 = Agent.get_agent_from_name(sys.argv[i + 2], DARK_PIECE, configs['41gensnodoubles'], True)
    universal.players = [agent_1, agent_2]

num_games = 100
if '--games' in sys.argv:
    i = sys.argv.index("--games")
    num_games = int(sys.argv[i + 1])

def simulate_move(debug_print=True):
    if not universal.next_moves:
        universal.next_moves = universal.current_player.move(brd.board, universal.dice_values, universal.opening)
        if not universal.next_moves: return None

    move = universal.next_moves.pop(0)
    brd.board, universal.dice_values = brd.move_piece(move, brd.board[:], universal.dice_values, universal.current_player.color)
    universal.current_player.add_move_this_turn(move)
    if debug_print:
        print("Dice:", universal.dice_values)
        print("Move:", universal.current_player_index, move)
        print("Board:", brd.board)

    if not universal.dice_values or not universal.current_player.get_available_moves(brd.board, universal.dice_values):
        universal.change_player()

    return move

def simulate_game(players=universal.players):
    if players != universal.players:
        universal.players = players

    if len(players) != 2:
        print("ERROR: There must be 2 players!")
        return None

    moves = []
    count = 0
    universal.start_game()
    while brd.board[0] != -15 and brd.board[25] != 15:
        start = time.time()
        move = simulate_move(debug_print=False)
        end = time.time()
        move_time = end - start
        universal.current_player.add_move_time(move_time)
        
        moves.append(move)
        count += 1
        if count > 1000: 
            print(f"Game blocked")
            return None
    
    winner = players[1] if brd.board[0] == -15 else players[0]
    return GameInfo(players, winner, moves)

def simulate_games(n = 1):
    global line, light, dark

    while n > 0:
        print(f"n={n}")
        line += f"n={n}\n"
        info = simulate_game()

        if info is None: continue

        if info.winner.color == DARK_PIECE: dark += 1
        else: light += 1
        n -= 1
        print("Light:", light, "Dark:", dark)
        line += f"Light: {light} Dark: {dark}\n"

if __name__ == '__main__':
    sounds.play_sounds = False
    t = str(tp.calculate_function_time(simulate_games, n=num_games))
    stats = ''
    stats += f"Time passed: {t} seconds\n"
    stats += '\n'
    stats += f"Total branches {universal.players[0].name}: {universal.players[0].total_number_of_branches()}\n"
    stats += f"Average branches {universal.players[0].name}: {universal.players[0].average_branching_factor()}\n"
    stats += f"Average time per move {universal.players[0].name}: {universal.players[0].average_time_per_move()} seconds\n"
    stats += f"Winning percentage {universal.players[0].name}: {light / (light + dark) * 100}%\n"
    stats += f"\n"
    stats += f"Total branches {universal.players[1].name}: {universal.players[1].total_number_of_branches()}\n"
    stats += f"Average branches {universal.players[1].name}: {universal.players[1].average_branching_factor()}\n"
    stats += f"Average time per move {universal.players[1].name}: {universal.players[1].average_time_per_move()} seconds\n"
    stats += f"Winning percentage {universal.players[1].name}: {dark / (light + dark) * 100}%\n"
    file_content = stats + '\n' + line

    print(stats)

    if save_to_file:
        with open(f'results/agent_evaluation/{universal.players[0].name}_VS_{universal.players[1].name}.txt', 'w') as f:
            f.write(file_content)