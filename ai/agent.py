import game_logic.player as player
import game_logic.board as brd
import random

from game_logic.move import Move
from ai.opening_moves import opening_moves
from ai.eval import evaluate_position_of_player
from ai.state import State
from ui.colors import *
from abc import ABC, abstractmethod

class Agent(player.Player):
    def __init__(self, color, config, play_opening=False):
        super().__init__(color)
        self.config = config
        self.play_opening = play_opening

        #Stats
        self.sum_of_branches = 0
        self.number_of_levels = 0
        self.sum_of_move_times = 0
        self.number_of_moves = 0

    @abstractmethod
    def move(self, board, dice_values, opening_move=False):
        if opening_move:
            opening = self.get_opening_moves(dice_values)
            result = []
            for mv in opening:
                result.append(Move.convert_to_global(mv[0], mv[1], self.color, board, dice_values))
            return result
        else: 
            return None

    def get_opening_moves(self, dice_values):
        sorted_dice = tuple(sorted(list([dice_values[0], dice_values[1]])))
        return opening_moves[sorted_dice]

    def _apply_beam(self, states, k):
        if len(states) <= k:
            return states
        
        scored = []
        for s in states:
            cache_check = self.cache.get(s)
            if cache_check:
                scored.append((cache_check, s))
            else:
                scored.append((evaluate_position_of_player(s.board, self.color, self.config), s))
                
        scored.sort(reverse=True, key=lambda x: x[0])
        return [s for (_, s) in scored[:k]]

    def expectimax(self, state, is_max_player, depth, use_beam=False):
        color = self.color if is_max_player else self.opponent_color

        has_cache = hasattr(self, 'cache')
        if has_cache:
            cache_check = self.cache.get(state)
            if cache_check: return cache_check

        if depth >= self.max_depth:
            score = evaluate_position_of_player(state.board, self.color, self.config)
            score -= evaluate_position_of_player(state.board, self.opponent_color, self.config)
            if has_cache: self.cache[state] = score
            return score
        else:
            all_dice = brd.get_all_unique_dice_values()

            average = -100000 #if blocked return this
            scores = []
            for dice in all_dice:
                new_states = self.get_all_board_states_after_move(state.board, dice, color)
                if use_beam: 
                    if isinstance(self, AdaptiveBeamAgent):
                        new_states = self._apply_beam(new_states, self.beam_width, depth)
                    else:
                        new_states = self._apply_beam(new_states, self.beam_width)            

                m = 1 if dice[0] == dice[1] else 2
                for new_state in new_states:
                    scores.append(self.expectimax(new_state, not is_max_player, depth + 1) * m)

            if scores: average = sum(scores) / len(scores)

            if has_cache: self.cache[state] = average
            return average

    def track_branches(self, n):
        self.sum_of_branches += n
        self.number_of_levels += 1

    def add_move_time(self, time):
        self.sum_of_move_times += time
        self.number_of_moves += 1

    def total_number_of_branches(self):
        return self.sum_of_branches

    def average_branching_factor(self):
        return self.sum_of_branches / self.number_of_levels

    def average_time_per_move(self):
        return self.sum_of_move_times / self.number_of_moves

class RandomAgent(Agent):
    def __init__(self, color, config=None, play_opening=False):
        super().__init__(color, config, play_opening)
        self.name = "random"
        
    def move(self, board, dice_values, opening_move=False):
        #Random player ignores opening moves
        # if opening_move: return super().move(board, dice_values, opening_move)

        available_moves = self.get_available_moves(board, dice_values)
        self.track_branches(len(available_moves))

        if not available_moves: return None
        return [random.choice(available_moves)]
    
class GreedyAgent(Agent):    
    def __init__(self, color, config, play_opening=False):
        super().__init__(color, config, play_opening)
        self.name = "shallow_greedy"

    def move(self, board, dice_values, opening_move=False):
        if opening_move and self.play_opening: return super().move(board, dice_values, opening_move)

        available_moves = self.get_available_moves(board, dice_values)
        available_moves = sorted(available_moves, key=lambda x: x.source_point)
        if self.color == DARK_PIECE: available_moves.reverse()

        self.track_branches(len(available_moves))
        if not available_moves: return None
        best_move = max(available_moves, key=lambda x: x.evaluate(self.config))
        return [best_move]

class DepthGreedyAgent(Agent):
    def __init__(self, color, config, play_opening=False):
        super().__init__(color, config, play_opening)
        self.name = 'depth_greedy'

    def move(self, board, dice_values, opening_move=False):
        if opening_move and self.play_opening: return super().move(board, dice_values, opening_move)

        available_moves = self.get_available_moves(board, dice_values)
        sort_order = -1 if self.color == DARK_PIECE else 1
        available_moves.sort(key=lambda x: sort_order * x.source_point)
        self.track_branches(len(available_moves))

        best = float('-inf')
        result = available_moves[0]
        for move in available_moves:
            score = self.recursive_search(move, board, dice_values, 1)
            if best < score:
                best = score
                result = move

        return [result]
    
    def recursive_search(self, move, board, dice_values, depth) :
        result_board, result_dice = brd.move_piece(move, board[:], dice_values, self.color)

        if not result_dice or depth >= len(dice_values):
            return evaluate_position_of_player(result_board, self.color, self.config)

        available_moves = self.get_available_moves(result_board, result_dice, self.config)
        self.track_branches(len(available_moves))
        if not available_moves:
            return evaluate_position_of_player(result_board, self.color, self.config)

        return max(
            self.recursive_search(mv, result_board, result_dice, depth + 1)
            for mv in available_moves
        )
        
class ExpectimaxAgent(Agent):
    def __init__(self, color, config, play_opening=False, max_depth=2):
        super().__init__(color, config, play_opening)
        self.max_depth = max_depth
        self.name = "expectimax"

    def move(self, board, dice_values, opening_move=False):
        if opening_move and self.play_opening: return super().move(board, dice_values, opening_move)
        
        best_score = float('-inf')
        
        board_states = self.get_all_board_states_after_move(board, dice_values)
        best_state = None
        for state in board_states:
            score = self.expectimax(state, is_max_player=False, depth=1)

            if best_score < score:
                best_score = score
                best_state = state

        return best_state.move_history

    def get_all_board_states_after_move(self, board, dice_values, color=None):
        if color is None: color = self.color
        available_moves = self.get_available_moves(board, dice_values, color)
        self.track_branches(len(available_moves))

        result = []
        for move in available_moves:
            board_inst = self.recursive_search(move, board, dice_values, 0, [], color)
            result.extend(board_inst)
        return result

    def recursive_search(self, move, board, dice_values, depth, mvs, color):
        new_mvs = mvs + [move]
        result_board, result_dice = brd.move_piece(move, board[:], dice_values, color)

        if not result_dice:
            return [State(result_board, color, new_mvs)]

        available_moves = self.get_available_moves(result_board, result_dice, color)
        self.track_branches(len(available_moves))
        if not available_moves:
            return [State(result_board, color, new_mvs)]

        result_array = []
        for mv in available_moves:
            result_array.extend(self.recursive_search(mv, result_board, result_dice, depth + 1, new_mvs, color))

        return result_array
    
class CachingExpectimaxAgent(ExpectimaxAgent):
    def __init__(self, color, config, play_opening=False, max_depth=2):
        super().__init__(color, config, play_opening, max_depth)
        self.cache = {}
        self.name = "caching_expectimax"

    def clear_cache(self):
        self.cache.clear() 

    def move(self, board, dice_values, opening_move=False):
        result = super().move(board, dice_values, opening_move)
        return result
        
class BeamExpectimaxAgent(CachingExpectimaxAgent):
    def __init__(self, color, config, play_opening=False, max_depth=2, beam_width=5):
        super().__init__(color, config, play_opening, max_depth)
        self.beam_width = beam_width
        self.cache = {}
        self.name = 'beam_expectimax'

    def clear_cache(self):
        self.cache.clear() 

    def move(self, board, dice_values, opening_move=False):
        if opening_move and self.play_opening: return super().move(board, dice_values, opening_move)
        
        best_score = float('-inf')
        
        board_states = self.get_all_board_states_after_move(board, dice_values)
        board_states = self._apply_beam(board_states, self.beam_width)
        best_state = None
        for state in board_states:
            score = self.expectimax(state, is_max_player=False, depth=1, use_beam=True)

            if best_score < score:
                best_score = score
                best_state = state

        return best_state.move_history
        
class AdaptiveBeamAgent(BeamExpectimaxAgent):
    def __init__(self, color, config, play_opening=False, max_depth=2, beam_width=5):
        super().__init__(color, config, play_opening, max_depth, beam_width)
        self.name = 'adaptive_beam'

    def _beam_width_at_depth(self, k, depth):
        return max(2, k - depth)
    
    def _apply_beam(self, states, k, depth):
        beam_width = self._beam_width_at_depth(k, depth)
        return super()._apply_beam(states, beam_width)

    def move(self, board, dice_values, opening_move=False):
        if opening_move and self.play_opening: return super().move(board, dice_values, opening_move)

        best_score = float('-inf')
        
        board_states = self.get_all_board_states_after_move(board, dice_values)
        board_states = self._apply_beam(board_states, self.beam_width, 0)
        best_state = None
        for state in board_states:
            score = self.expectimax(state, is_max_player=False, depth=1, use_beam=True)

            if best_score < score:
                best_score = score
                best_state = state

        return best_state.move_history