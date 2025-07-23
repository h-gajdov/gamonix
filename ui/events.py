import math
import universal
import random
from game_logic.board import *
from options import *

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
    if value1 != value2: result = [value1, value2, value1 + value2]
    else: result = [value1] * 4
    
    dice_values_ui = (value1, value2)
    return tuple(result)

def get_clicked_point(click_pos):
    for point in points:
        if point.rect.collidepoint(click_pos): return point
    return None

def select_point(clicked_point):
    global selected_point, can_move_to_points
    selected_point = clicked_point
    
    current_position = points.index(selected_point)
    indices = get_available_points_from_position(current_position, universal.dice_values, universal.is_light_on_turn)
    can_move_to_points = [points[idx] for idx in indices]
    for point in can_move_to_points: 
        point.set_highlight(True)

def deselect_all():
    global selected_point
    selected_point = None
    for point in points: point.set_highlight(False)

def change_player():
    universal.is_light_on_turn = not universal.is_light_on_turn
    universal.dice_values = roll_dice() 

def handle_dice_values_after_move(current_position, target_position):
    delta = int(math.fabs(current_position - target_position))
        
    if len(universal.dice_values) != 1:
        tmp = list(universal.dice_values)
        if universal.dice_values[0] == universal.dice_values[1]: 
            count = delta / universal.dice_values[0]
            while count:
                tmp.pop()
                count -= 1
            universal.dice_values = tuple(tmp)
        else:
            if delta == max(tmp):
                change_player()
            else: 
                tmp.pop()
                tmp.remove(delta)
                universal.dice_values = tuple(tmp)
    else: change_player()

def move_pieces(event):
    global selected_point, can_move_to_points
    clicked_point = get_clicked_point(event.pos)
    
    if selected_point and clicked_point in can_move_to_points: 
        current_position = points.index(selected_point)
        target_position = points.index(clicked_point)
        handle_dice_values_after_move(current_position, target_position)
        
        selected_point.move_piece_to(clicked_point)
        deselect_all()
    elif len(clicked_point.pieces) > 0:
        deselect_all()
        select_point(clicked_point)

def debug_select_point(event):
    clicked_point = get_clicked_point(event.pos)
    if clicked_point:
        clicked_point.set_highlight(not clicked_point.is_highlighted)
        print(points.index(clicked_point))