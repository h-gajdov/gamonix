class State:
    def __init__(self, board, last_player_color, move_history=[]):
        self.board = board
        self.last_player_color = last_player_color
        self.move_history = move_history

    def convert_to_tuple(self):
        return (tuple(self.board), self.last_player_color)

    def __hash__(self):
        return hash(self.convert_to_tuple())
    
    def __eq__(self, other):
        if not isinstance(other, State):
            return False
        
        return self.board == other.board and self.last_player_color == other.last_player_color

    def __repr__(self):
        return f"[{self.move_history}] {self.convert_to_tuple()}"