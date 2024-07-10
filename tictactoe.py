def first_board():
    board = []
    for _ in range(3):
        row = []
        for _ in range(3):
            row.append('-')
        board.append(row)
    return board

def print_board(board):
    for row in board:
        print(' '.join(row))
    print()

def is_board_full(board):
    for row in board:
        if '-' in row:
            return False
    return True

def is_win(board, player):
    for row in board:
        if all([cell == player for cell in row]):
            return True
    for col in range(3):
        if all([board[row][col] == player for row in range(3)]):
            return True
    if all([board[i][i] == player for i in range(3)]):
        return True
    if all([board[i][2 - i] == player for i in range(3)]):
        return True
    return False

def play_game():
    board = first_board()
    current_player = 'X'
    
    while not is_board_full(board):
        print_board(board)
        try:
            row = int(input(f"{current_player}، row? (0 , 2): "))
            col = int(input("col? (0 , 2): "))
        except ValueError:
            print("enter your number")
            continue

       
        if row < 0 or row > 2 or col < 0 or col > 2 or board[row][col] != '-':
            print("Re-enter error")
            continue
        board[row][col] = current_player
        if is_win(board, current_player):
            print_board(board)
            print(f"{current_player} is win")
            return
        current_player = 'O' if current_player == 'X' else 'X'

    print_board(board)
    print("equal")
play_game()
