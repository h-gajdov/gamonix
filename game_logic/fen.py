def convert_fen_to_board(fen):
    board = [0] * 24
    info = fen.split(':')
    for position in range(24):
        entry = info[position]
        if entry == '0': continue
        
        number = int(entry[:-1])
        mult = -1 if entry[-1] == 'B' else 1
        board[position] = mult * number

    return board
    
def convert_state_to_fen():
    pass