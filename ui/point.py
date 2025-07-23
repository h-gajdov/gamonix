from abc import ABC, abstractmethod

class Point(ABC):
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.rect = None

    @abstractmethod
    def draw(self):
        pass