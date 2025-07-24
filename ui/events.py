import math
import universal
import random
import game_logic.board as brd
from options import *
from colors import *

points = []
can_move_to_points = []
selected_point = None
dice_values_ui = (1, 1)

def set_points(ref):
    global points
    points = ref

def roll_dice():
    global dice_values_ui
    value1 = random.randint(1, 6)
    value2 = random.randint(1, 6)
    if value1 != value2: result = [value1, value2]
    else: result = [value1] * 4
    
    result = handle_distant_dice_values(result)
    dice_values_ui = (value1, value2)
    return tuple(result)

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
    
    if universal.is_light_on_turn and not check_condition(True, points.index(clicked_point)): return
    if not universal.is_light_on_turn and not check_condition(False, points.index(clicked_point)): return
    
    selected_point = clicked_point
    
    is_taken = False
    current_position = get_current_position(selected_point)
    if current_position >= 26:
        is_taken = True
        current_position = 25 if not universal.is_light_on_turn else 0
    
    indices = brd.get_available_points_from_position(current_position, universal.dice_values, universal.is_light_on_turn, is_taken)
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

def change_player():
    universal.is_light_on_turn = not universal.is_light_on_turn
    universal.dice_values = roll_dice() 

def handle_distant_dice_values(array):
    result = array[:]
    max_value = max(result)
    most_distant = brd.get_most_distant_piece(universal.is_light_on_turn)
    if max_value > most_distant:
        result = [value if value <= most_distant else most_distant for value in result]
    return result

def handle_dice_values_after_move(current_position, target_position):
    if current_position < 26:
        delta = int(math.fabs(current_position - target_position))
    else: 
        delta = target_position if universal.is_light_on_turn else 25 - target_position
        
    if len(universal.dice_values) != 1:
        tmp = list(universal.dice_values)
        if universal.dice_values[0] == universal.dice_values[1]: 
            count = delta / universal.dice_values[0]
            while count:
                tmp.pop()
                count -= 1
            universal.dice_values = tuple(tmp)
        else:
            tmp.remove(delta)
            universal.dice_values = tuple(tmp)
    else: change_player()
    universal.dice_values = handle_distant_dice_values(universal.dice_values)

def move_pieces(event):
    global selected_point, can_move_to_points
    clicked_point = get_clicked_point(event.pos)
    
    if not clicked_point: return
    
    if selected_point and clicked_point in can_move_to_points: 
        current_position = points.index(selected_point)
        target_position = points.index(clicked_point)
        
        if math.fabs(brd.board[target_position]) == 1 and brd.board[current_position] * brd.board[target_position] < 0:
            clicked_point.take(points.index(clicked_point), points)
            if selected_point == points[26] or selected_point == points[27]:
                selected_point.move_piece_to(clicked_point, 0)
            else:
                selected_point.move_piece_to(clicked_point)
        else:
            selected_point.move_piece_to(clicked_point)
        brd.update_board_array(points)
        
        handle_dice_values_after_move(current_position, target_position)
        print(universal.dice_values)
        deselect_all()
    elif len(clicked_point.pieces) > 0:
        deselect_all()
        select_point(clicked_point)

def debug_select_point(event):
    clicked_point = get_clicked_point(event.pos)
    if clicked_point:
        clicked_point.set_highlight(not clicked_point.is_highlighted)
        print(points.index(clicked_point))