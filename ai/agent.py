import game_logic.player as player
import game_logic.board as brd
import random
from ai.eval import evaluate_position_of_player
from ai.state import State
from ui.colors import *
from abc import ABC, abstractmethod

class Agent(player.Player):
    def __init__(self, color, config):
        super().__init__(color)
        self.config = config
    
    @abstractmethod
    def move(self, board, dice_values): pass

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
    
class RandomAgent(Agent):
    def __init__(self, color, config=None):
        super().__init__(color, config)
        
    def move(self, board, dice_values):
        available_moves = self.get_available_moves(board, dice_values)
        if not available_moves: return None
        return random.choice(available_moves)
    
class GreedyAgent(Agent):    
    def __init__(self, color, config):
        super().__init__(color, config)
    
    def move(self, board, dice_values):
        available_moves = self.get_available_moves(board, dice_values)
        available_moves = sorted(available_moves, key=lambda x: x.source_point)
        if self.color == DARK_PIECE: available_moves.reverse()
        if not available_moves: return None
        best_move = max(available_moves, key=lambda x: x.evaluate(self.config))
        return best_move

class DepthGreedyAgent(Agent):
    def __init__(self, color, config):
        super().__init__(color, config)

    def move(self, board, dice_values):
        available_moves = self.get_available_moves(board, dice_values)
        sort_order = -1 if self.color == DARK_PIECE else 1
        available_moves.sort(key=lambda x: sort_order * x.source_point)
        
        best = float('-inf')
        result = available_moves[0]
        for move in available_moves:
            score = self.recursive_search(move, board, dice_values, 1)
            if best < score:
                best = score
                result = move
        return result
    
    def recursive_search(self, move, board, dice_values, depth) :
        result_board, result_dice = brd.move_piece(move, board[:], dice_values, self.color)

        if not result_dice or depth >= len(dice_values):
            return evaluate_position_of_player(result_board, self.color, self.config)

        available_moves = self.get_available_moves(result_board, result_dice, self.config)
        if not available_moves:
            return evaluate_position_of_player(result_board, self.color, self.config)

        return max(
            self.recursive_search(mv, result_board, result_dice, depth + 1)
            for mv in available_moves
        )
        
class ExpectimaxAgent(Agent):
    def __init__(self, color, config, max_depth=2):
        super().__init__(color, config)
        self.max_depth = max_depth

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
    
class CachingExpectimaxAgent(ExpectimaxAgent):
    def __init__(self, color, config, max_depth=2):
        super().__init__(color, config, max_depth)
        self.cache = {}

    def clear_cache(self):
        self.cache.clear() 

    def move(self, board, dice_values):
        result = super().move(board, dice_values)
        return result
        
class BeamExpectimaxAgent(CachingExpectimaxAgent):
    def __init__(self, color, config, max_depth=2, beam_width=5):
        super().__init__(color, config, max_depth)
        self.beam_width = beam_width
        self.cache = {}

    def clear_cache(self):
        self.cache.clear() 

    def move(self, board, dice_values):
        best_score = float('-inf')
        best_move = None
        
        board_states = self.get_all_board_states_after_move(board, dice_values)
        board_states = self._apply_beam(board_states, self.beam_width)
        for state in board_states:
            score = self.expectimax(state, is_max_player=False, depth=1, use_beam=True)

            if best_score < score:
                best_score = score
                best_move = state.move_history[0]

        return best_move
        
class AdaptiveBeamAgent(BeamExpectimaxAgent):
    def __init__(self, color, config, max_depth=2, beam_width=5):
        super().__init__(color, config, max_depth, beam_width)

    def _beam_width_at_depth(self, k, depth):
        return max(2, k - depth)
    
    def _apply_beam(self, states, k, depth):
        beam_width = self._beam_width_at_depth(k, depth)
        return super()._apply_beam(states, beam_width)

    def move(self, board, dice_values):
        best_score = float('-inf')
        best_move = None
        
        board_states = self.get_all_board_states_after_move(board, dice_values)
        board_states = self._apply_beam(board_states, self.beam_width, 0)
        for state in board_states:
            score = self.expectimax(state, is_max_player=False, depth=1, use_beam=True)

            if best_score < score:
                best_score = score
                best_move = state.move_history[0]

        return best_move