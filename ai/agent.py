import game_logic.player as player
from abc import ABC, abstractmethod

class Agent(player.Player, ABC):
    def __init__(self, color):
        super().__init__(color)
    
    @abstractmethod
    def move(self): pass