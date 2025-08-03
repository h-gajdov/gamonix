import game_logic.player as player
import game_logic.board as brd
import random
from ai.eval import evaluate_position_of_player
from ai.state import State
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
        if not available_moves: return None
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
    
    def recursive_search(self, move, board, dice_values, depth) :
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
        
class ExpectimaxAgent(Agent):
    def __init__(self, color, max_depth=2):
        super().__init__(color)
        self.max_depth = max_depth

    def expectimax(self, state, is_max_player, depth):
        opponent_color = DARK_PIECE if self.color == LIGHT_PIECE else LIGHT_PIECE
        color = self.color if is_max_player else opponent_color
        
        if depth >= self.max_depth:
            return evaluate_position_of_player(state.board, self.color)
        else:
            all_dice = brd.get_all_unique_dice_values()

            average = -100000 #if blocked return this
            scores = []
            for dice in all_dice:
                new_boards = self.get_all_board_states_after_move(state.board, dice, color)
                for new_state in new_boards:
                    scores.append(self.expectimax(new_state, not is_max_player, depth + 1))

            if scores: average = sum(scores) / len(scores)
            return average

    def move(self, board, dice_values):
        best_score = float('-inf')
        best_move = None
        
        board_states = self.get_all_board_states_after_move(board, dice_values)
        for state in board_states:
            score = self.expectimax(state, is_max_player=False, depth=1)

            if best_score < score:
                best_score = score
                best_move = state.move_history[0]

        return best_move

    def get_all_board_states_after_move(self, board, dice_values, color=None):
        if color is None: color = self.color
        available_moves = self.get_available_moves(board, dice_values, color)

        result = []
        for move in available_moves:
            board_inst = self.recursive_search(move, board, dice_values, 0, [], color)
            result.extend(board_inst)
        return result

    def recursive_search(self, move, board, dice_values, depth, mvs, color):
        new_mvs = mvs + [move]
        result_board, result_dice = brd.move_piece(move, board[:], dice_values, color)

        if not result_dice or depth >= len(dice_values):
            return [State(result_board, color, new_mvs)]

        available_moves = self.get_available_moves(result_board, result_dice, color)
        if not available_moves:
            return [State(result_board, color, new_mvs)]

        result_array = []
        for mv in available_moves:
            result_array.extend(self.recursive_search(mv, result_board, result_dice, depth + 1, new_mvs, color))

        return result_array