import curses
import sqlite3
from datetime import datetime
import time

class TicTacToe:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.initialize_database()
        self.initial_board()
        self.current_player = 'X'
        self.cursor_row, self.cursor_col = 0, 0

    def initialize_database(self):
        conn = sqlite3.connect('tic_tac_toe.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS game_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                winner TEXT,
                duration REAL,
                date TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def save_game_history(self, winner, duration):
        conn = sqlite3.connect('tic_tac_toe.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO game_history (winner, duration, date)
            VALUES (?, ?, ?)
        ''', (winner, duration, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        conn.close()

    def initial_board(self):
        self.board = [['-' for _ in range(3)] for _ in range(3)]

    def draw(self):
        self.stdscr.clear()
        for r in range(3):
            for c in range(3):
                char = self.board[r][c]
                if (r, c) == (self.cursor_row, self.cursor_col):
                    if char == '-':
                        char = f"[{self.current_player}]"
                    else:
                        char = f"[{char}]"
                else:
                    char = f" {char} " if char == '-' else f" {char} "
                self.stdscr.addstr(r, c * 4, char)
        self.stdscr.addstr(4, 0, "Press 'm' for menu")
        self.stdscr.refresh()

    def is_board_full(self):
        return all(cell != '-' for row in self.board for cell in row)

    def all_equal(self, iterator, player):
        return all(cell == player for cell in iterator)

    def get_diagonals(self):
        main_diagonal = [self.board[i][i] for i in range(3)]
        anti_diagonal = [self.board[i][2 - i] for i in range(3)]
        return main_diagonal, anti_diagonal

    def check_rows(self, player):
        return any(self.all_equal(row, player) for row in self.board)

    def check_columns(self, player):
        return any(self.all_equal((self.board[row][col] for row in range(3)), player) for col in range(3))

    def check_diagonals(self, player):
        main_diagonal, anti_diagonal = self.get_diagonals()
        return self.all_equal(main_diagonal, player) or self.all_equal(anti_diagonal, player)

    def check_all(self, player):
        return self.check_rows(player) or self.check_columns(player) or self.check_diagonals(player)

    def is_win(self, player):
        return self.check_all(player)

    def play_turn(self):
        start_time = time.time()

        while not self.is_board_full():
            self.draw()
            key = self.stdscr.getch()

            if key == curses.KEY_UP:
                self.cursor_row = (self.cursor_row - 1) % 3
            elif key == curses.KEY_DOWN:
                self.cursor_row = (self.cursor_row + 1) % 3
            elif key == curses.KEY_LEFT:
                self.cursor_col = (self.cursor_col - 1) % 3
            elif key == curses.KEY_RIGHT:
                self.cursor_col = (self.cursor_col + 1) % 3
            elif key == 10:  
                if self.board[self.cursor_row][self.cursor_col] == '-':
                    self.board[self.cursor_row][self.cursor_col] = self.current_player
                    if self.is_win(self.current_player):
                        end_time = time.time()
                        game_duration = end_time - start_time
                        self.save_game_history(self.current_player, game_duration)

                        self.draw()
                        self.stdscr.addstr(5, 0, f"{self.current_player} wins!")
                        self.stdscr.refresh()
                        self.stdscr.getch()
                        return
                    self.current_player = 'O' if self.current_player == 'X' else 'X'
            elif key == ord('m'): 
                selected_option = self.show_menu()
                if selected_option == "Exit":
                    return

            self.stdscr.clear()

        self.draw()
        self.stdscr.addstr(5, 0, "Draw!")
        self.stdscr.refresh()
        self.stdscr.getch()

    def show_menu(self):
        menu_items = ["Continue", "History", "Exit"]
        current_row = 0

        while True:
            self.stdscr.clear()
            for idx, item in enumerate(menu_items):
                if idx == current_row:
                    self.stdscr.addstr(idx, 0, item, curses.color_pair(1))
                else:
                    self.stdscr.addstr(idx, 0, item)
            self.stdscr.refresh()

            key = self.stdscr.getch()

            if key == curses.KEY_UP and current_row > 0:
                current_row -= 1
            elif key == curses.KEY_DOWN and current_row < len(menu_items) - 1:
                current_row += 1
            elif key == 10:  
                if current_row == 1:  
                    self.show_history()
                elif current_row == 2:  
                    return "Exit"
                else:
                    return "Continue"

    def show_history(self):
        conn = sqlite3.connect('tic_tac_toe.db')
        cursor = conn.cursor()
        cursor.execute('SELECT winner, duration, date FROM game_history')
        rows = cursor.fetchall()

        self.stdscr.clear()
        
        if not rows:
            self.stdscr.addstr(0, 0, "No history available.")
        else:
            self.stdscr.addstr(0, 0, "Game History:")
            max_y, max_x = self.stdscr.getmaxyx()  

            for idx, (winner, duration, date) in enumerate(rows, start=1):
                history_line = f"Winner: {winner}, Duration: {duration:.2f} sec, Date: {date}"
                if idx < max_y - 2:
                    self.stdscr.addstr(idx, 0, history_line[:max_x - 1])  

        self.stdscr.addstr(max_y - 2, 0, "Press any key to return...")
        self.stdscr.refresh()
        self.stdscr.getch()

        conn.close()

def start_game(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    game = TicTacToe(stdscr)
    game.play_turn()

curses.wrapper(start_game)

