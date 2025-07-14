import pygame
from colors import *
from triangle import *
from options import *
from game_logic.board import get_board, initialize_board_array

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Gamonix")

initialize_board_array()
print(get_board())
tris = initialize_triangles_array()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
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
    OFF_SECTION_WIDTH = BOARD_WIDTH - 2 * BOARD_HEIGHT
    OFF_SECTION_HEIGHT = 20
    pygame.draw.rect(screen, OFF_SECTION, (BOARD_HEIGHT, BOARD_HEIGHT, OFF_SECTION_WIDTH, TRIANGLE_HEIGHT + OFF_SECTION_HEIGHT))
    pygame.draw.rect(screen, OFF_SECTION, (BOARD_HEIGHT, SCREEN_HEIGHT * 0.6 - OFF_SECTION_HEIGHT - BOARD_HEIGHT, OFF_SECTION_WIDTH, TRIANGLE_HEIGHT + OFF_SECTION_HEIGHT))
    pygame.draw.rect(screen, OFF_SECTION, (SCREEN_WIDTH - BOARD_HEIGHT - OFF_SECTION_WIDTH, BOARD_HEIGHT, OFF_SECTION_WIDTH, TRIANGLE_HEIGHT + OFF_SECTION_HEIGHT))
    pygame.draw.rect(screen, OFF_SECTION, (SCREEN_WIDTH - BOARD_HEIGHT - OFF_SECTION_WIDTH, SCREEN_HEIGHT * 0.6 - OFF_SECTION_HEIGHT - BOARD_HEIGHT, OFF_SECTION_WIDTH, TRIANGLE_HEIGHT + OFF_SECTION_HEIGHT))
    
    pygame.display.flip()

pygame.quit()