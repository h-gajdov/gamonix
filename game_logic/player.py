import game_logic.board as brd
from ui.colors import *

class Player:
    def __init__(self, color):
        self.color = color
        self.available_moves = self.get_available_moves()

    def get_available_moves(self):
        return []
    
    def is_light(self):
        return self.color == LIGHT_PIECE
    
    def handle_distant_dice_values(self, array):
        result = array[:]
        max_value = max(result)
        most_distant = brd.get_most_distant_piece(self.is_light())
        if max_value > most_distant:
            result = [value if value <= most_distant else most_distant for value in result]
        return result