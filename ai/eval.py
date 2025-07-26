def evaluate_points(board):
    light = 0
    dark = 0
    for idx, value in enumerate(board):
        if value <= 0: continue
        light += 25 - idx
    
    for idx, value in enumerate(board):
        if value >= 0: continue
        dark += idx
    
    return {'light': light, 'dark': dark}