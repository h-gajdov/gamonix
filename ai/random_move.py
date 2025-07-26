import ai.agent as agent
import random

class RandomAI(agent.Agent):
    def __init__(self, color):
        super().__init__(color)
        
    def move(self):
        available_moves = self.get_available_moves()
        if not available_moves: return None
        return random.choice(available_moves)