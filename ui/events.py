import math
import sounds
import universal
import game_logic.board as brd

from options import *
from colors import *
from game_logic.move import Move

points = []
can_move_to_points = []
selected_point = None

def set_points(ref):
    global points
    points = ref

def get_clicked_point(click_pos):
    for point in points:
        if point.rect.collidepoint(click_pos): return point
    return None

def get_current_position(point):
    result = points.index(point)
    return result

def select_point(clicked_point):
    global selected_point, can_move_to_points
    def check_condition(positive, idx):
        if positive: 
            if brd.board[26] > 0: return idx == 26
            else: return brd.board[idx] > 0
        else: 
            if brd.board[27] < 0: return idx == 27
            else: return brd.board[idx] < 0

    if clicked_point.compare_pieces_color(universal.players[universal.AI_PLAYER_INDEX].color): return
    if universal.current_player.color == LIGHT_PIECE and not check_condition(True, points.index(clicked_point)): return
    if universal.current_player.color == DARK_PIECE and not check_condition(False, points.index(clicked_point)): return
    
    selected_point = clicked_point

    is_taken = False
    current_position = get_current_position(selected_point)
    if current_position >= 26:
        is_taken = True
        current_position = 25 if universal.current_player.color == DARK_PIECE else 0
    
    indices = brd.get_available_points_from_position(current_position, brd.board, universal.dice_values, universal.current_player.color, is_taken)
    can_move_to_points = [points[idx] for idx in indices]
    for point in can_move_to_points: 
        point.set_highlight(True)
    
    selected_point.pieces[-1].set_highlight(True) # Highlight last piece in point

def deselect_all():
    global selected_point
    if selected_point and selected_point.pieces: 
        selected_point.pieces[-1].set_highlight(False) # Dehiglight last piece in point
    
    selected_point = None
    for point in points: point.set_highlight(False)

def handle_dice_values_after_move(current_position, target_position):
    global dice_values_ui

    move = Move(current_position, target_position, brd.board, universal.dice_values, universal.current_player.color)
    universal.dice_values = brd.update_dice_values(universal.dice_values, move, universal.current_player.color, brd.board)

def move_pieces(event):
    global selected_point, can_move_to_points
    clicked_point = get_clicked_point(event.pos)
    
    if not clicked_point: return
    
    if selected_point and clicked_point in can_move_to_points: 
        current_position = points.index(selected_point)
        target_position = points.index(clicked_point)
        universal.previous_states.append((brd.board[:], universal.dice_values))
        
        taken_piece = False
        if math.fabs(brd.board[target_position]) == 1 and brd.board[current_position] * brd.board[target_position] < 0:
            sounds.play_sound(sounds.capture_sound)
            clicked_point.take(points.index(clicked_point), points)
            if selected_point == points[26] or selected_point == points[27]:
                selected_point.move_piece_to(clicked_point, 0)
            else:
                selected_point.move_piece_to(clicked_point)
        else:
            selected_point.move_piece_to(clicked_point)
        brd.update_board_array(points)
        
        handle_dice_values_after_move(current_position, target_position)
        universal.current_player.add_move_this_turn(Move(current_position, target_position, brd.board, universal.dice_values, universal.current_player.color))
        
        if not taken_piece: 
            sounds.play_sound(sounds.move_sound)
        print(universal.dice_values)

        if not universal.dice_values or not universal.player_has_moves(): universal.change_player()
        deselect_all()
    elif len(clicked_point.pieces) > 0:
        deselect_all()
        select_point(clicked_point)

def debug_select_point(event):
    clicked_point = get_clicked_point(event.pos)
    if clicked_point:
        clicked_point.set_highlight(not clicked_point.is_highlighted)
        print(points.index(clicked_point))