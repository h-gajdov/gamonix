import universal
import game_logic.board as brd
import debug.time_passed as tp

from ui.colors import *

next_moves = []

class GameInfo:
    def __init__(self, players, winner, move_history):
        self.players = players
        self.winner = winner
        self.move_history = move_history

    def __repr__(self):
        return f"Players: {self.players}\nWinner: {self.winner}\nMoves: {len(self.move_history)}\nMove history: {self.move_history}"

def simulate_move(debug_print=True):
    global next_moves
    if not next_moves:
        next_moves = universal.current_player.move(brd.board, universal.dice_values, universal.opening)
    
    move = next_moves.pop(0)
    brd.board, universal.dice_values = brd.move_piece(move, brd.board[:], universal.dice_values, universal.current_player.color)
    if debug_print: 
        print("Dice:", universal.dice_values)
        print("Move:", universal.current_player_index, move)    
        print("Board:", brd.board)
    
    if not universal.dice_values or not universal.current_player.get_available_moves(brd.board, universal.dice_values): universal.change_player()
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
        moves.append(simulate_move(debug_print=False))
        count += 1
        if count > 1000: 
            print(f"Game blocked")
            return None
    
    winner = players[0] if brd.board[0] == -15 else players[1]
    return GameInfo(players, winner, moves)

def simulate_games(n = 1):
    dark = 0
    light = 0
    while n > 0:
        print(f"n={n}")
        info = simulate_game()

        if info == None: continue

        if info.winner.color == DARK_PIECE: dark += 1
        else: light += 1
        n -= 1
        print("Light:", light, "Dark:", dark)

# tp.calculate_function_time(simulate_games, n=3000)