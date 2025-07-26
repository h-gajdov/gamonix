class Move:
    def __init__(self, source_point: int, destination_point: int):
        self.source_point = source_point
        self.destination_point = destination_point
    
    def __repr__(self):
        return f"{self.source_point} -> {self.destination_point}"