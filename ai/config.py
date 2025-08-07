import random

class Config:
    def __init__(self, blocked_point_score, connected_blocks_factor, blots_factor, blots_factor_passed, blots_threshold, run_or_block_factor):
        self.blocked_point_score = blocked_point_score
        self.connected_blocks_factor = connected_blocks_factor
        self.blots_factor = blots_factor
        self.blots_factor_passed = blots_factor_passed
        self.blots_threshold = blots_threshold
        self.run_or_block_factor = run_or_block_factor
        # self.taking_pieces_factor = taking_pieces_factor
        
    def to_dict(self):
        return {
            "blocked_point_score": self.blocked_point_score,
            "connected_blocks_factor": self.connected_blocks_factor,
            "blots_factor": self.blots_factor,
            "blots_factor_passed": self.blots_factor_passed,
            "blots_threshold": self.blots_threshold,
            "run_or_block_factor": self.run_or_block_factor
        }
    
    def __repr__(self):
        return f"{self.to_dict()}"

    @staticmethod
    def random_config():
        return Config(
            blocked_point_score=random.uniform(0, 3),
            connected_blocks_factor=random.uniform(0, 2),
            blots_factor=random.uniform(0, 3),
            blots_factor_passed=random.uniform(0, 3),
            blots_threshold=random.randint(0, 5), 
            run_or_block_factor=random.uniform(0, 1),
            # taking_pieces_factor=random.uniform(0, 15)
        )
    
configs = {
    'untrained': Config(
        blocked_point_score=0,
        connected_blocks_factor=0,
        blots_factor=1,
        blots_factor_passed=1,
        blots_threshold=0,
        run_or_block_factor=0
    ),
    'trained': Config(
        blocked_point_score=1.608432,
        connected_blocks_factor=0.739531007,
        blots_factor=1.225,
        blots_factor_passed=1.925,
        blots_threshold=3,
        run_or_block_factor=0.262721103
    ),
    '50gens30popgreedy': Config(
        blocked_point_score=0.013473197299744943,
        connected_blocks_factor=1.660276243960727,
        blots_factor=0.8092524360770296,
        blots_factor_passed=0.5611325421587715,
        blots_threshold=1,
        run_or_block_factor=0.2746299033248154
    )
}