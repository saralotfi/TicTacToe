import os
from os import system

class TicTacToe:
    def __init__(self):
        self.initial_Board()
        self.current_player = 'X'

    def initial_Board(self):
        self.board = []
        for _ in range(3):
            row = ['-'] * 3
            self.board.append(row)

    def draw(self):
        for row in self.board:
            print(' '.join(row))
        print()

    def is_board_full(self):
        for row in self.board:
            if '-' in row:
                return False
        return True

    def all_equal(self, iterator, player):
        for cell in iterator:
            if cell != player:
                return False
        return True

    def get_diagonals(self):
        main_diagonal = [self.board[i][i] for i in range(3)]
        anti_diagonal = [self.board[i][2 - i] for i in range(3)]
        return main_diagonal, anti_diagonal

    def check_rows(self, player):
        for row in self.board:
            if self.all_equal(row, player):
                return True
        return False

    def check_columns(self, player):
        for col in range(3):
            if self.all_equal((self.board[row][col] for row in range(3)), player):
                return True
        return False

    def check_diagonals(self, player):
        main_diagonal, anti_diagonal = self.get_diagonals()
        if self.all_equal(main_diagonal, player) or self.all_equal(anti_diagonal, player):
            return True
        return False

    def is_win(self, player):
        return self.check_rows(player) or self.check_columns(player) or self.check_diagonals(player)

    def play_turn(self):
        while not self.is_board_full():
            self.draw()
            if not self.take_player_turn():
                continue

            if self.is_win(self.current_player):
                self.draw()
                print(f"{self.current_player} wins!")
                return
            system('cls' if os.name == 'nt' else 'clear')
            self.current_player = 'O' if self.current_player == 'X' else 'X'
        
        self.draw()
        print("It's a draw!")

    def take_player_turn(self):
        try:
            row = int(input(f"{self.current_player}, row? (0, 2): "))
            col = int(input("col? (0, 2): "))
        except ValueError:
            print("Enter valid numbers.")
            return False

        if 0 <= row <= 2 and 0 <= col <= 2 and self.board[row][col] == '-':
            self.board[row][col] = self.current_player
            return True
        else:
            print("Invalid input or cell already occupied. Please re-enter.")
            return False

def start_game():
    game = TicTacToe()
    game.play_turn()

start_game()







