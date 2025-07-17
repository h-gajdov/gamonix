import pygame
import random 
from colors import *
from triangle import *
from options import *
from game_logic.board import *
import layer

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
transparent_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
pygame.display.set_caption("Gamonix")

initialize_board_array()
layer.intialize_layers()
tris = initialize_triangles_array()
prev_selected_tri = None
can_move_to_tris = []
off_pieces = get_off_pieces()

dice1_text = pygame.font.Font(None, 36)
dice2_text = pygame.font.Font(None, 36)

dice_values = (1, 1)
dice_sum = 4
is_light_on_turn = False
available_moves = get_available_moves_for_position(dice_values, is_light_on_turn)

def roll_dice():
    global available_moves
    result = (random.randint(1, 6), random.randint(1, 6))
    d_sum = sum(result) if result[0] != result[1] else 4 * result[0]
    available_moves = get_available_moves_for_position(result, is_light_on_turn)
    return result, d_sum

def get_clicked_triangle(click_pos):
    for tri in tris:
        if tri.rect.collidepoint(click_pos): return tri
    return None

def draw_off_pieces(count, y, color, mult = 1):
    while count > 0:
        x = SCREEN_WIDTH - BOARD_HEIGHT - OFF_SECTION_WIDTH
        draw_rect(layer.background_board_layer, color, x, y, TAKEN_PIECE_WIDTH, TAKEN_PIECE_HEIGHT, 1, 2)
        y += mult * TAKEN_PIECE_HEIGHT
        count -= 1

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d: dice_values, dice_sum = roll_dice()
            elif event.key == pygame.K_w: number_of_taken_light_pieces += 1
            elif event.key == pygame.K_s: number_of_taken_light_pieces -= 1
            elif event.key == pygame.K_UP: number_of_taken_dark_pieces += 1
            elif event.key == pygame.K_DOWN: number_of_taken_dark_pieces -= 1
                
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            clicked_tri = get_clicked_triangle(event.pos)
            if clicked_tri: 
                current_position = tris.index(clicked_tri)
                if clicked_tri in can_move_to_tris and prev_selected_tri:
                    delta = current_position - tris.index(prev_selected_tri)
                    transformed_dice_values = tuple([0 if t == math.fabs(delta) else t for t in list(dice_values)])
                    if dice_values[0] != dice_values[1]: available_moves = get_available_moves_for_position(transformed_dice_values, is_light_on_turn)
                    else: available_moves.pop()
                    
                    if clicked_tri.number_of_pieces == 1 and clicked_tri.piece_color != prev_selected_tri.piece_color:
                        if not is_light_on_turn: 
                            number_of_taken_light_pieces += 1
                            clicked_tri.piece_color = DARK_PIECE
                        else:
                            number_of_taken_dark_pieces += 1
                            clicked_tri.piece_color = LIGHT_PIECE 
                    else: clicked_tri.number_of_pieces += 1
                    
                    clicked_tri.piece_color = LIGHT_PIECE if is_light_on_turn else DARK_PIECE 
                    prev_selected_tri.number_of_pieces -= 1
                    dice_sum -= math.fabs(current_position - tris.index(prev_selected_tri))
                    if dice_sum <= 0: 
                        is_light_on_turn = not is_light_on_turn
                        dice_values, dice_sum = roll_dice()
                    can_move_to_tris.clear()
                    prev_selected_tri = None
                elif clicked_tri == prev_selected_tri: 
                    can_move_to_tris.clear()
                    prev_selected_tri = None
                elif clicked_tri.number_of_pieces != 0:
                    can_move_to_tris.clear()
                    prev_selected_tri = clicked_tri
                    for move in available_moves:
                        if move + current_position < 0 or move + current_position >= 24: continue
                        if not tris[current_position + move].check_color(is_light_on_turn): continue
                        can_move_to_tris.append(tris[current_position + move])
        
    layer.Layer.clear_layers()
    layer.background_board_layer.surface.fill(BOARD_BACKGROUND)
    
    #Triangles
    for tri in tris: tri.draw()
    
    #Borders
    draw_rect(layer.background_board_layer, BOARD_BORDER, 0, 0, SCREEN_WIDTH, BOARD_HEIGHT)
    draw_rect(layer.background_board_layer, BOARD_BORDER, 0, SCREEN_HEIGHT - BOARD_HEIGHT, SCREEN_WIDTH, BOARD_HEIGHT)
    draw_rect(layer.background_board_layer, BOARD_BORDER, 0, 0, BOARD_WIDTH, SCREEN_HEIGHT)
    draw_rect(layer.background_board_layer, BOARD_BORDER, SCREEN_WIDTH - BOARD_WIDTH, 0, BOARD_WIDTH, SCREEN_HEIGHT)
    
    #Middle Border
    draw_rect(layer.background_board_layer, BOARD_BORDER, SCREEN_WIDTH / 2 - BOARD_WIDTH / 2, 0, BOARD_WIDTH, SCREEN_HEIGHT)
    
    #Off sections
    down_off_section_y = SCREEN_HEIGHT * 0.6 - OFF_SECTION_ADDED_HEIGHT - BOARD_HEIGHT
    right_off_section_x = SCREEN_WIDTH - BOARD_HEIGHT - OFF_SECTION_WIDTH
    draw_rect(layer.background_board_layer, OFF_SECTION, BOARD_HEIGHT, BOARD_HEIGHT, OFF_SECTION_WIDTH, OFF_SECTION_HEIGHT)
    draw_rect(layer.background_board_layer, OFF_SECTION, BOARD_HEIGHT, down_off_section_y, OFF_SECTION_WIDTH, OFF_SECTION_HEIGHT)
    draw_rect(layer.background_board_layer, OFF_SECTION, right_off_section_x, BOARD_HEIGHT, OFF_SECTION_WIDTH, OFF_SECTION_HEIGHT)
    draw_rect(layer.background_board_layer, OFF_SECTION, right_off_section_x, down_off_section_y, OFF_SECTION_WIDTH, OFF_SECTION_HEIGHT)
    
    #Off pieces
    taken_y = SCREEN_HEIGHT * 0.6 - OFF_SECTION_ADDED_HEIGHT + (OFF_SECTION_HEIGHT - TAKEN_PIECE_HEIGHT + 1) - BOARD_HEIGHT
    draw_off_pieces(off_pieces['light'], BOARD_HEIGHT, LIGHT_PIECE) #Light pieces
    draw_off_pieces(off_pieces['dark'], taken_y, DARK_PIECE, -1) #Dark pieces
    
    #Draw dice UI
    dice_size = 56
    tmp_width = SCREEN_WIDTH - 2 * BOARD_WIDTH 
    box1 = draw_rect(layer.ui_layer, WHITE, BOARD_WIDTH + 3 * tmp_width / 4 - dice_size, SCREEN_HEIGHT / 2 - dice_size / 2, dice_size, dice_size, 1, 5)
    box2 = draw_rect(layer.ui_layer, WHITE, BOARD_WIDTH + 3 * tmp_width / 4 + dice_size, SCREEN_HEIGHT / 2 - dice_size / 2, dice_size, dice_size, 1, 5)

    #Draw taken pieces
    number_of_taken_pieces = number_of_taken_dark_pieces + number_of_taken_light_pieces
    y_coord = SCREEN_HEIGHT / 2 - (number_of_taken_pieces - 1) * PIECE_RADIUS
    for taken_piece in range(number_of_taken_dark_pieces):
        draw_circle(layer.game_board_layer, DARK_PIECE, SCREEN_WIDTH / 2,  y_coord, PIECE_RADIUS, 1)
        y_coord += 2 * PIECE_RADIUS
    for taken_piece in range(number_of_taken_light_pieces):
        draw_circle(layer.game_board_layer, LIGHT_PIECE, SCREEN_WIDTH / 2,  y_coord, PIECE_RADIUS, 1)
        y_coord += 2 * PIECE_RADIUS

    text_surface_1 = dice1_text.render(str(dice_values[0]), False, BLACK)
    text_surface_2 = dice1_text.render(str(dice_values[1]), True, BLACK) 
    text_rect_1 = text_surface_1.get_rect(center=box1.center)
    text_rect_2 = text_surface_2.get_rect(center=box2.center)
    layer.ui_layer.surface.blit(text_surface_1, text_rect_1)
    layer.ui_layer.surface.blit(text_surface_2, text_rect_2)
    
    if prev_selected_tri: prev_selected_tri.select()
    for tri in can_move_to_tris: tri.highlight()
    
    layer.Layer.draw_layers(screen)
    pygame.display.flip()

pygame.quit()