def convert_fen_to_board(fen):
    board = [0] * 28
    
    info = fen.split(':')
    for position in range(24):
        entry = info[position]
        if entry == '0': continue
        
        number = int(entry[:-1])
        mult = -1 if entry[-1] == 'B' else 1
        board[position + 1] = mult * number

    light_taken = int(info[24])
    dark_taken = int(info[25])
    light_off = int(info[26])
    dark_off = int(info[27])

    board[0] = -dark_off
    board[25] = light_off

    board[26] = light_taken
    board[27] = -dark_taken

    value1 = int(info[28])
    value2 = int(info[29])
    if value1 == value2:
        dice = tuple([value1] * 4)
    else:
        dice = (value1, value2)
    
    player_idx = int(info[-1])
    return board, dice, player_idx
    
def convert_state_to_fen():
    pass