import game_logic.player as player
import game_logic.board as brd
import random
from ai.eval import evaluate_position_of_player
from ui.colors import *
from abc import ABC, abstractmethod

class Agent(player.Player):
    def __init__(self, color):
        super().__init__(color)
    
    @abstractmethod
    def move(self, board, dice_values): pass
    
class RandomAgent(Agent):
    def __init__(self, color):
        super().__init__(color)
        
    def move(self, board, dice_values):
        available_moves = self.get_available_moves(board, dice_values)
        if not available_moves: return None
        return random.choice(available_moves)
    
class GreedyAgent(Agent):    
    def __init__(self, color):
        super().__init__(color)
    
    def move(self, board, dice_values):
        available_moves = self.get_available_moves(board, dice_values)
        available_moves = sorted(available_moves, key=lambda x: x.source_point)
        if self.color == DARK_PIECE: available_moves.reverse()
        best_move = max(available_moves, key=lambda x: x.evaluate())
        return best_move

class DepthGreedyAgent(Agent):
    def __init__(self, color):
        super().__init__(color)

    def move(self, board, dice_values):
        available_moves = self.get_available_moves(board, dice_values)
        sort_order = -1 if self.color == DARK_PIECE else 1
        available_moves.sort(key=lambda x: sort_order * x.source_point)
        
        best = float('-inf')
        result = available_moves[0]
        for move in available_moves:
            score = self.recursive(move, board, dice_values, 1)
            if best < score:
                best = score
                result = move
        return result
    
    def recursive(self, move, board, dice_values, depth) :
        result_board, result_dice = brd.move_piece(move, board[:], dice_values, self.color)

        if not result_dice or depth >= len(dice_values):
            return evaluate_position_of_player(result_board, self.color)

        available_moves = self.get_available_moves(result_board, result_dice)
        if not available_moves:
            return evaluate_position_of_player(result_board, self.color)

        return max(
            self.recursive(mv, result_board, result_dice, depth + 1)
            for mv in available_moves
        )