import universal
import game_logic.board as brd
import game_logic.player as player
import debug.time_passed as tp

brd.initialize_board_array()
universal.start_game()
def simulate_move(debug_print=True):
    move = universal.current_player.move(brd.board)
    brd.board, universal.dice_values = brd.move_piece(move, brd.board[:], universal.dice_values, universal.current_player.color)
    player.Player.set_dice_values(universal.dice_values)
    
    if debug_print: 
        print("Dice:", universal.dice_values)
        print("Move:", universal.current_player_index, move)    
        print("Board:", brd.board)
    
    if not universal.dice_values or not universal.current_player.get_available_moves(brd.board): universal.change_player()
    
def simulate_games(n = 1):
    dark = 0
    light = 0
    while n > 0:
        brd.initialize_board_array()
        universal.start_game()
        while brd.board[0] != -15 and brd.board[25] != 15:
            simulate_move(False)
        
        if brd.board[0] == -15: dark += 1
        else: light += 1
        n -= 1
        print(f"n={n}")
        
    print("Light:", light, "Dark:", dark)
    
tp.calculate_function_time(simulate_games, n=3000)