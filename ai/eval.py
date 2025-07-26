from math import fabs

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

def block_counts(board):
    def count_blocks(positive):
        prevWasBlock = False
        result = []
        for idx, value in enumerate(board):
            if idx == 0 or idx == 25: continue

            if positive and value <= 0 or not positive and value >= 0: 
                prevWasBlock = False
                continue
            
            if fabs(value) < 2: 
                prevWasBlock = False
                continue

            if prevWasBlock: result[-1] += 1
            else: result.append(1) 
            prevWasBlock = True
        return result

    light = count_blocks(True)
    dark = count_blocks(False)

    return {'light': light, 'dark': dark}
        