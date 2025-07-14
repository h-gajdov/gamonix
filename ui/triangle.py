import pygame
import math
from options import *
from colors import *
from game_logic.board import get_board

def initialize_triangles_array():
    tris = []
    is_dark = False
    for x in range(1, 14):
        if x == 7: continue
        startX = x * TRIANGLE_WIDTH + TRIANGLE_WIDTH / 2
        tri = Triangle(startX, SCREEN_HEIGHT - BOARD_HEIGHT, LIGHT_TRIANGLES if is_dark else DARK_TRIANGLES, TRIANGLE_WIDTH, TRIANGLE_HEIGHT, True, 0)
        is_dark = not is_dark
        tris.append(tri)
    
    tris.reverse()
    is_dark = not is_dark
    for x in range(1, 14):
        if x == 7: continue
        startX = x * TRIANGLE_WIDTH + TRIANGLE_WIDTH / 2
        tri = Triangle(startX, BOARD_HEIGHT, LIGHT_TRIANGLES if is_dark else DARK_TRIANGLES, TRIANGLE_WIDTH, TRIANGLE_HEIGHT, False, 0)
        is_dark = not is_dark
        tris.append(tri)
        
    for idx, tri in enumerate(tris):
        board = get_board()
        n = math.fabs(board[idx])
        tri.pieceColor = LIGHT_PIECE if board[idx] > 0 else DARK_PIECE
        tri.numberOfPieces = n

    return tris

class Triangle:
    def __init__(self, x: int, y: int, color: tuple, width: int, height: int, isUpsideDown: bool, numberOfPieces: int, pieceColor = (0, 0, 0)):
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.height = height
        self.isUpsideDown = isUpsideDown
        self.numberOfPieces = numberOfPieces
        self.pieceColor = pieceColor
            
    def draw(self, screen):
        p1 = (self.x - self.width / 2, self.y)
        p2 = (self.x + self.width / 2, self.y)
        
        tmp = self.height if not self.isUpsideDown else SCREEN_HEIGHT - self.height
        p3 = (self.x, tmp)
        pygame.draw.polygon(screen, self.color, [p1, p2, p3])
        
        count = 0
        pieceX = self.x
        mult = -1 if self.isUpsideDown else 1
        pieceY = self.y + mult * PIECE_RADIUS
        while count < self.numberOfPieces:
            pygame.draw.circle(screen, self.pieceColor, (pieceX, pieceY), PIECE_RADIUS)
            pygame.draw.circle(screen, (0, 0, 0), (pieceX, pieceY), PIECE_RADIUS, width=1) #Border
            pieceY += mult * 2 * PIECE_RADIUS
            count += 1