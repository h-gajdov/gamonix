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
taken_pieces = []
off_pieces = get_off_pieces()

dice1_text = pygame.font.Font(None, 36)
dice2_text = pygame.font.Font(None, 36)

dice_values = (1, 1)
dice_sum = 4
is_light_on_turn = False
available_moves = get_available_moves_for_position(dice_values, is_light_on_turn)

dark_off_seciont_rect = None
light_off_seciont_rect = None
highlight_dark_off_section = False
highlight_light_off_section = False

def get_number_of_pieces_in_base():
    light_count = 0
    dark_count = 0
    for light_base_index in range(18, 24):
        if tris[light_base_index].piece_color == LIGHT_PIECE:
            light_count += len(tris[light_base_index].pieces)
    for dark_base_index in range(0, 6):
        if tris[dark_base_index].piece_color == DARK_PIECE:
            dark_count += len(tris[dark_base_index].pieces)
    return {'light': light_count, 'dark': dark_count}
    
def select_taken_piece(click_pos):
    result = None
    for piece in taken_pieces:
        if piece.rect and piece.rect.collidepoint(click_pos):
            result = piece
            piece.set_highlight(not piece.is_highlighted)
    return result

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

def move_piece_event(source_tri, destination_tri, piece=None, piece_position=None):
    global is_light_on_turn, available_moves, dice_values, dice_sum, number_of_taken_light_pieces, number_of_taken_dark_pieces
    current_position = tris.index(destination_tri)
    if piece_position == None: delta = math.fabs(current_position - tris.index(source_tri))
    else: delta = math.fabs(current_position - piece_position)
    
    if dice_values[0] != dice_values[1]:
        if len(available_moves) == 3: 
            move = available_moves.pop()
            if delta == math.fabs(move): available_moves.clear()
        available_moves = [move for move in available_moves if math.fabs(move) != delta]
    else:
        count = delta // dice_values[0]
        for _ in range(int(count)): available_moves.pop()
    
    source_color = piece.color if piece else source_tri.piece_color
    if destination_tri.number_of_pieces == 1 and destination_tri.piece_color != source_color:
        taken_pieces.append(destination_tri.pop_piece())
        if destination_tri.piece_color == LIGHT_PIECE: 
            number_of_taken_light_pieces += 1
        else:
            number_of_taken_dark_pieces += 1

    if piece: destination_tri.add_specific_piece(piece)
    else: source_tri.pieces[-1].move_between_triangles(source_tri, destination_tri)
    
    if not available_moves:
        is_light_on_turn = not is_light_on_turn
        dice_values, dice_sum = roll_dice()
    can_move_to_tris.clear()

taken_piece = None
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d: dice_values, dice_sum = roll_dice()
            if event.key == pygame.K_z: highlight_light_off_section = not highlight_light_off_section
            if event.key == pygame.K_x: highlight_dark_off_section = not highlight_dark_off_section
                
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if prev_selected_tri and light_off_seciont_rect and light_off_seciont_rect.collidepoint(event.pos):
                off_pieces['light'] += 1
                prev_selected_tri.pop_piece()
                prev_selected_tri = None
                highlight_light_off_section = False
                can_move_to_tris.clear()
            elif dark_off_seciont_rect and dark_off_seciont_rect.collidepoint(event.pos):
                off_pieces['dark'] += 1
                prev_selected_tri.pop_piece()
                prev_selected_tri = None
                highlight_dark_off_section = False
                can_move_to_tris.clear()

            clicked_tri = get_clicked_triangle(event.pos)
            if not taken_piece: taken_piece = select_taken_piece(event.pos)
            if taken_piece:
                can_move_to_tris.clear()
                for move in available_moves:
                    idx = move - 1 if taken_piece.color == LIGHT_PIECE else 24 + move
                    can_move_to_tris.append(tris[idx])

            if clicked_tri: 
                current_position = tris.index(clicked_tri)
                if clicked_tri in can_move_to_tris:
                    if taken_piece:
                        if taken_piece.color == LIGHT_PIECE: 
                            number_of_taken_light_pieces -= 1
                            piece_position = -1 if taken_piece.color == LIGHT_PIECE else 24 
                        else:
                            number_of_taken_dark_pieces -= 1
                            
                        move_piece_event(source_tri=None, destination_tri=clicked_tri, piece=taken_piece, piece_position=piece_position)
                        taken_pieces.remove(taken_piece)
                        taken_piece.set_highlight(False)
                        taken_piece=None
                    if prev_selected_tri:
                        move_piece_event(prev_selected_tri, clicked_tri)
                        prev_selected_tri = None            
                elif clicked_tri == prev_selected_tri: 
                    can_move_to_tris.clear()
                    highlight_dark_off_section = False
                    highlight_light_off_section = False
                    prev_selected_tri.deselect()
                    prev_selected_tri = None
                elif clicked_tri.number_of_pieces != 0:
                    if is_light_on_turn and number_of_taken_light_pieces != 0: pass
                    elif not is_light_on_turn and number_of_taken_dark_pieces != 0: pass
                    else:
                        can_move_to_tris.clear()
                        highlight_dark_off_section = False
                        highlight_light_off_section = False
                        
                        if prev_selected_tri: prev_selected_tri.deselect()
                        prev_selected_tri = clicked_tri
                        prev_selected_tri.select()
                        for move in available_moves:
                            if move + current_position < -1 or move + current_position > 24: continue

                            if move + current_position == -1:
                                highlight_dark_off_section = True
                                continue
                            elif move + current_position == 24:
                                highlight_light_off_section = True
                                continue

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
    if highlight_light_off_section: 
        light_off_seciont_rect = draw_rect(layer.highlight_pieces_layer, (0, 255, 0, 128), right_off_section_x, BOARD_HEIGHT, OFF_SECTION_WIDTH, OFF_SECTION_HEIGHT)
    if highlight_dark_off_section: 
        dark_off_seciont_rect = draw_rect(layer.highlight_pieces_layer, (0, 255, 0, 128), right_off_section_x, down_off_section_y, OFF_SECTION_WIDTH, OFF_SECTION_HEIGHT)

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
    for piece in taken_pieces:
        piece.set_position(SCREEN_WIDTH / 2, y_coord)
        y_coord += 2 * PIECE_RADIUS
        piece.draw()

    text_surface_1 = dice1_text.render(str(dice_values[0]), False, BLACK)
    text_surface_2 = dice1_text.render(str(dice_values[1]), True, BLACK) 
    text_rect_1 = text_surface_1.get_rect(center=box1.center)
    text_rect_2 = text_surface_2.get_rect(center=box2.center)
    layer.ui_layer.surface.blit(text_surface_1, text_rect_1)
    layer.ui_layer.surface.blit(text_surface_2, text_rect_2)
    
    for tri in can_move_to_tris: tri.highlight()
    
    # print(get_number_of_pieces_in_base())
    
    layer.Layer.draw_layers(screen)
    pygame.display.flip()

pygame.quit()