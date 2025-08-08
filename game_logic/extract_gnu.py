import base64

def decode_position_id_to_bit_string(position_id: str):
    decoded_bytes = base64.b64decode(position_id)
    
    binary_string = ''.join(f'{byte:08b}' for byte in decoded_bytes)
    byte_chunks = [binary_string[i:i+8] for i in range(0, len(binary_string), 8)]

    for idx in range(len(byte_chunks)):
        byte_chunks[idx] = byte_chunks[idx][::-1]

    return ''.join(byte_chunks)

def parse_bit_string_for_player(bit_string, start):
    board = []
    count = 0
    positions_processed = 0
    prevWasOne = False
    idx = 0
    for bit in bit_string[start:]:
        if positions_processed >= 25: break
        idx += 1
        
        if bit == '1':
            if prevWasOne: count += 1
            else: 
                count = 1
                prevWasOne = True
        else: 
            board.append(count)
            positions_processed += 1
            prevWasOne = False
            count = 0
            
    return board, idx
    
# bit_string = decode_position_id_to_bit_string('4HPwARSA4ANgAw==')    
# bit_string = decode_position_id_to_bit_string('zN6IMQCbOQcAWA==')    
def decode_position(position_id):
    bit_string = decode_position_id_to_bit_string(position_id + "==")    
    board, end = parse_bit_string_for_player(bit_string, 0)
    other, _ = parse_bit_string_for_player(bit_string, end)

    taken_board = board[-1]
    off_board = 15 - sum(board)
    board = board[:-1]
    taken_other = other[-1]
    off_other = 15 - sum(other)
    other = other[:-1]
    print(board)
    print(other)

    final = [0] * 28

    for i in range(1, 25):
        if board[i - 1] != 0:
            final[i] = -board[i - 1]
        else:
            final[i] = other[23 - (i - 1)]
        
    final[26] = taken_other
    final[27] - -taken_board
    final[0] = off_board
    final[25] = off_other
    return final