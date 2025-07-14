import pygame
from colors import *
from triangle import *
from options import *
from game_logic.board import initialize_board_array, get_off_pieces

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Gamonix")

initialize_board_array()
tris = initialize_triangles_array()

def draw_off_pieces(count, taken_y, color, mult = 1):
    while count > 0:
        pygame.draw.rect(screen, color, (SCREEN_WIDTH - BOARD_HEIGHT - OFF_SECTION_WIDTH, taken_y, OFF_SECTION_WIDTH, TAKEN_PIECE_HEIGHT), border_radius=2)
        pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH - BOARD_HEIGHT - OFF_SECTION_WIDTH, taken_y, OFF_SECTION_WIDTH, TAKEN_PIECE_HEIGHT), width=1, border_radius=2) #Border
        taken_y += mult * TAKEN_PIECE_HEIGHT
        count -= 1

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_UP and number_of_dark_pieces_off < 15: number_of_dark_pieces_off+=1
        #     elif event.key == pygame.K_DOWN and number_of_dark_pieces_off > 0: number_of_dark_pieces_off-=1

        #     if event.key == pygame.K_w and number_of_light_pieces_off < 15: number_of_light_pieces_off+=1
        #     elif event.key == pygame.K_s and number_of_light_pieces_off > 0: number_of_light_pieces_off-=1

    screen.fill(BOARD_BACKGROUND)
    
    #Triangles
    for tri in tris: tri.draw(screen)
    
    #Borders
    pygame.draw.rect(screen, BOARD_BORDER, (0, 0, SCREEN_WIDTH, BOARD_HEIGHT))
    pygame.draw.rect(screen, BOARD_BORDER, (0, SCREEN_HEIGHT - BOARD_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.draw.rect(screen, BOARD_BORDER, (0, 0, BOARD_WIDTH, SCREEN_HEIGHT))
    pygame.draw.rect(screen, BOARD_BORDER, (SCREEN_WIDTH - BOARD_WIDTH, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
    
    #Middle Border
    pygame.draw.rect(screen, BOARD_BORDER, (SCREEN_WIDTH / 2 - BOARD_WIDTH / 2, 0, BOARD_WIDTH, SCREEN_HEIGHT))
    
    #Off sections
    pygame.draw.rect(screen, OFF_SECTION, (BOARD_HEIGHT, BOARD_HEIGHT, OFF_SECTION_WIDTH, OFF_SECTION_HEIGHT))
    pygame.draw.rect(screen, OFF_SECTION, (BOARD_HEIGHT, SCREEN_HEIGHT * 0.6 - OFF_SECTION_ADDED_HEIGHT - BOARD_HEIGHT, OFF_SECTION_WIDTH, OFF_SECTION_HEIGHT))
    pygame.draw.rect(screen, OFF_SECTION, (SCREEN_WIDTH - BOARD_HEIGHT - OFF_SECTION_WIDTH, BOARD_HEIGHT, OFF_SECTION_WIDTH, OFF_SECTION_HEIGHT))
    pygame.draw.rect(screen, OFF_SECTION, (SCREEN_WIDTH - BOARD_HEIGHT - OFF_SECTION_WIDTH, SCREEN_HEIGHT * 0.6 - OFF_SECTION_ADDED_HEIGHT - BOARD_HEIGHT, OFF_SECTION_WIDTH, OFF_SECTION_HEIGHT))
    
    #Off pieces
    off_pieces = get_off_pieces()
    taken_y = SCREEN_HEIGHT * 0.6 - OFF_SECTION_ADDED_HEIGHT + (OFF_SECTION_HEIGHT - TAKEN_PIECE_HEIGHT + 1) - BOARD_HEIGHT
    draw_off_pieces(off_pieces['light'], BOARD_HEIGHT, LIGHT_PIECE) #Light pieces
    draw_off_pieces(off_pieces['dark'], taken_y, DARK_PIECE, -1) #Dark pieces

    pygame.display.flip()

pygame.quit()