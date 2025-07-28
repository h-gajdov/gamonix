class Config:
    def __init__(self, blocked_point_score, connected_blocks_factor, blots_factor, blots_factor_passed, blots_threshold, run_or_blot_factor):
        self.blocked_point_score = blocked_point_score
        self.connected_blocks_factor = connected_blocks_factor
        self.blots_factor = blots_factor
        self.blots_factor_passed = blots_factor_passed
        self.blots_threshold = blots_threshold
        self.run_or_blot_factor = run_or_blot_factor
        
configs = {
    'untrained': Config(
        blocked_point_score=0,
        connected_blocks_factor=0,
        blots_factor=1,
        blots_factor_passed=1,
        blots_threshold=0,
        run_or_blot_factor=0
    ) 
}