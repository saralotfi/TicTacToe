from os import system
class TicTacToe:
    def __init__(self):
        self.board = self.initialBoard()
        self.current_player = 'X'

    def initialBoard(self):
        board = []
        for _ in range(3):
            row = ['-'] * 3
            board.append(row)
        return board

    def draw(self):
        for row in self.board:
            print(' '.join(row))
        print()

    def isfull(self):
        for row in self.board:
            if '-' in row:
                return False
        return True

    def all_equal(self, iterator, player):
        for cell in iterator:
            if cell != player:
                return False
        return True

    def get_diagonal(self, main=True):
        if main:
            return (self.board[i][i] for i in range(3))
        else:
            return (self.board[i][2 - i] for i in range(3))

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
        if self.all_equal(self.get_diagonal(main=True), player) or self.all_equal(self.get_diagonal(main=False), player):
            return True
        return False

    def iswin(self, player):
        return self.check_rows(player) or self.check_columns(player) or self.check_diagonals(player)

    def playturn(self):
        while not self.isfull():
            self.draw()
            if not self.take_player_turn():
                continue
            
            if self.iswin(self.current_player):
                self.draw()
                print(f"{self.current_player} is win!")
                return
            system( 'cls' )
            self.current_player = 'O' if self.current_player == 'X' else 'X'
        
        self.draw()
        print("It's a draw!")

    def take_player_turn(self):
        try:
            row = int(input(f"{self.current_player}, row? (0 , 2): "))
            col = int(input("col? (0 , 2): "))
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



