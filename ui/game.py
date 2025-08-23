import pygame
import events
import time
import layer
import universal
import console
import sounds
import debug.time_passed as tp

from colors import *
from triangle import *
from options import *

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
transparent_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
pygame.display.set_caption("Gamonix")

layer.intialize_layers()
dice1_text = pygame.font.Font(None, 36)
dice2_text = pygame.font.Font(None, 36)

universal.start_game()
points = initialize_points_array()
events.set_points(points)

table_background = pygame.image.load("ui/assets/table_borders.png").convert_alpha()

def undo_move():
    state = universal.previous_states.pop()
    brd.board = state[0]
    universal.dice_values = state[1]
    points = initialize_points_array()
    events.set_points(points)

def highlight_previous_moves(player):
    for move in player.moves_this_turn:
        if move.source_point not in highlighted:
            points[move.source_point].highlight_made_move()
            highlighted.append(move.source_point)

        if move.destination_point not in highlighted:
            points[move.destination_point].highlight_made_move()
            highlighted.append(move.destination_point)

running = True
sounds.play_sounds = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_u and len(universal.previous_states) > 0:
                undo_move()
            
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            events.move_pieces(event)

    if time.time() > universal.time_to_next_move and universal.ai_is_on_turn():
        console.simulate_move(False)
        sounds.play_sound(sounds.move_sound)
        points = initialize_points_array()
        events.set_points(points)
        universal.time_to_next_move = time.time() + 1

    layer.Layer.clear_layers()
    layer.background_board_layer.surface.fill(BOARD_BACKGROUND)

    #Points
    for point in points:
        is_transparent = not point.compare_pieces_color(universal.players[universal.current_player_index].color)
        point.draw(is_transparent)

    highlighted = []
    if universal.current_player.moves_this_turn:
        highlight_previous_moves(universal.current_player)
    else:
        highlight_previous_moves(universal.get_player_not_on_turn())

    #Borders
    # draw_rect(layer.background_board_layer, BOARD_BORDER, 0, 0, SCREEN_WIDTH, BOARD_HEIGHT)
    # draw_rect(layer.background_board_layer, BOARD_BORDER, 0, SCREEN_HEIGHT - BOARD_HEIGHT, SCREEN_WIDTH, BOARD_HEIGHT)
    # draw_rect(layer.background_board_layer, BOARD_BORDER, 0, 0, BOARD_WIDTH, SCREEN_HEIGHT)
    # draw_rect(layer.background_board_layer, BOARD_BORDER, SCREEN_WIDTH - BOARD_WIDTH, 0, BOARD_WIDTH, SCREEN_HEIGHT)
    
    #Middle Border
    # draw_rect(layer.background_board_layer, BOARD_BORDER, SCREEN_WIDTH / 2 - BOARD_WIDTH / 2, 0, BOARD_WIDTH, SCREEN_HEIGHT)
    
    #Off sections
    down_off_section_y = SCREEN_HEIGHT * 0.6 - OFF_SECTION_ADDED_HEIGHT - BOARD_HEIGHT
    right_off_section_x = SCREEN_WIDTH - BOARD_HEIGHT - OFF_SECTION_WIDTH
    draw_rect(layer.background_board_layer, OFF_SECTION, BOARD_HEIGHT, BOARD_HEIGHT, OFF_SECTION_WIDTH, OFF_SECTION_HEIGHT)
    draw_rect(layer.background_board_layer, OFF_SECTION, BOARD_HEIGHT, down_off_section_y, OFF_SECTION_WIDTH, OFF_SECTION_HEIGHT)
    
    #Draw dice UI
    dice_size = 56
    tmp_width = SCREEN_WIDTH - 2 * BOARD_WIDTH 
    box1 = draw_rect(layer.ui_layer, WHITE, BOARD_WIDTH + 3 * tmp_width / 4 - dice_size, SCREEN_HEIGHT / 2 - dice_size / 2, dice_size, dice_size, 1, 5)
    box2 = draw_rect(layer.ui_layer, WHITE, BOARD_WIDTH + 3 * tmp_width / 4 + dice_size, SCREEN_HEIGHT / 2 - dice_size / 2, dice_size, dice_size, 1, 5)

    text_surface_1 = dice1_text.render(str(universal.dice_values_ui[0]), False, BLACK)
    text_surface_2 = dice1_text.render(str(universal.dice_values_ui[1]), True, BLACK) 
    text_rect_1 = text_surface_1.get_rect(center=box1.center)
    text_rect_2 = text_surface_2.get_rect(center=box2.center)
    layer.ui_layer.surface.blit(text_surface_1, text_rect_1)
    layer.ui_layer.surface.blit(text_surface_2, text_rect_2)

    layer.game_board_layer.surface.blit(table_background, (0, 0))
    layer.Layer.draw_layers(screen)
    pygame.display.flip()

pygame.quit()