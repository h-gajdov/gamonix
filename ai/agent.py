import game_logic.player as player
import game_logic.board as brd
import random
from ai.eval import evaluate_position_of_player
from ui.colors import *
from abc import ABC, abstractmethod
from copy import deepcopy

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
        
class ExpectimaxAgent(Agent):
    def __init__(self, color, max_depth=2):
        super().__init__(color)
        self.max_depth = max_depth

    def expectimax(self, board, is_max_player, depth):
        opponent_color = DARK_PIECE if self.color == LIGHT_PIECE else LIGHT_PIECE
        color = self.color if is_max_player else opponent_color

        if depth >= self.max_depth:
            return evaluate_position_of_player(board, self.color)
        else:
            all_dice = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6),
                        (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6),
                        (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6),
                        (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6),
                        (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6),
                        (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6)]

            average = -100000 #if blocked return this
            for dice in all_dice:
                new_boards = self.get_all_board_states_after_move(board, dice, color)
                scores = []
                for state in new_boards:
                    brd = state[-1]
                    scores.append(self.expectimax(brd, not is_max_player, depth + 1))

                if scores: average = sum(scores) / len(scores)
            return average

    def move(self, board, dice_values):
        best_score = float('-inf')
        best_move = None

        board_states = self.get_all_board_states_after_move(board, dice_values)
        for state in board_states:
            brd = state[-1]
            score = self.expectimax(brd, is_max_player=True, depth=1)

            if best_score < score:
                best_score = score
                best_move = state[0][0]

        return best_move

    def get_all_board_states_after_move(self, board, dice_values, color=None):
        if color is None: color = self.color
        available_moves = self.get_available_moves(board, dice_values, color)

        result = []
        for move in available_moves:
            board_inst = self.recursive(move, board, dice_values, 0, [], color)
            for brd in board_inst:
                result.append(brd)
        return result

    def recursive(self, move, board, dice_values, depth, mvs, color):
        mvs.append(move)
        result_board, result_dice = brd.move_piece(move, board[:], dice_values, color)

        if not result_dice or depth >= len(dice_values):
            return [[tuple(mvs), result_board]]

        available_moves = self.get_available_moves(result_board, result_dice, color)
        if not available_moves:
            return [[tuple(mvs), result_board]]

        result_array = []
        for mv in available_moves:
            result_array.extend(self.recursive(mv, result_board, result_dice, depth + 1, mvs, color))

        return result_array