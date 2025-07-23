import pygame
from game_logic.board import *
from options import *

points = []
selected_point = None

def set_points(ref):
    global points
    points = ref

def get_clicked_point(click_pos):
    for point in points:
        if point.rect.collidepoint(click_pos): return point
    return None

def move_pieces(event):
    global selected_point
    clicked_point = get_clicked_point(event.pos) 
    if not selected_point: 
        selected_point = clicked_point
    else:
        selected_point.move_piece_to(clicked_point)
        selected_point = None

def debug_select_point(event):
    clicked_point = get_clicked_point(event.pos)
    if clicked_point:
        clicked_point.set_highlight(not clicked_point.is_highlighted)
        print(points.index(clicked_point))