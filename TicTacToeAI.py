import tkinter as tk
from tkinter import ttk
import random

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe with AI")
        self.root.geometry("600x700")
        self.root.resizable(True, True)

        self.style = ttk.Style()
        self.root.configure(bg="#2e3440")
        self.style.theme_use("clam")
        self.style.configure("TLabel", background="#2e3440", foreground="white", font=("Helvetica", 14))
        self.style.configure("TButton", font=("Helvetica", 14), padding=10)
        self.style.configure("TCombobox", fieldbackground="#434c5e", background="#3b4252", foreground="white")

        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.player = "X"
        self.difficulty = tk.StringVar(value="Medium")
        self.player_score = 0
        self.ai_score = 0

        self.create_widgets()

    def create_widgets(self):
        header = ttk.Label(self.root, text="Tic Tac Toe", font=("Helvetica", 28, "bold"), anchor="center")
        header.grid(row=0, column=0, columnspan=3, sticky="nsew", pady=(20, 10))

        ttk.Label(self.root, text="Choose Difficulty:").grid(row=1, column=0, columnspan=3, pady=5)
        difficulty_box = ttk.Combobox(self.root, textvariable=self.difficulty, values=["Easy", "Medium", "Hard"], state="readonly", font=("Helvetica", 14))
        difficulty_box.grid(row=2, column=0, columnspan=3, sticky="nsew", padx=80, pady=10)

        self.player_score_label = ttk.Label(self.root, text=f"Player (X): {self.player_score}")
        self.player_score_label.grid(row=3, column=0, sticky="w", padx=20)
        self.ai_score_label = ttk.Label(self.root, text=f"AI (O): {self.ai_score}")
        self.ai_score_label.grid(row=3, column=2, sticky="e", padx=20)

        for i in range(3):
            self.root.grid_rowconfigure(i + 4, weight=1)
            for j in range(3):
                self.root.grid_columnconfigure(j, weight=1)
                btn = tk.Button(self.root, text="", font=("Helvetica", 36, "bold"),
                                bg="#4c566a", fg="white", activebackground="#81a1c1",
                                relief="raised", bd=6, command=lambda x=i, y=j: self.player_move(x, y))
                btn.grid(row=i + 4, column=j, padx=5, pady=5, sticky="nsew")
                self.buttons[i][j] = btn

        ttk.Button(self.root, text="New Game", command=self.reset_game).grid(row=7, column=0, columnspan=3, pady=20, padx=100, sticky="nsew")

        self.message_label = ttk.Label(self.root, text="", font=("Helvetica", 16, "bold"), anchor="center")
        self.message_label.grid(row=8, column=0, columnspan=3, pady=(10, 30), sticky="nsew")

        for i in range(9):
            self.root.grid_rowconfigure(i, weight=1)

    def player_move(self, x, y):
        if self.board[x][y] == "" and self.check_winner(self.board) is None:
            self.board[x][y] = "X"
            self.buttons[x][y].config(text="X", bg="#bf616a", relief="sunken")

            winner = self.check_winner(self.board)
            if winner == "X":
                self.player_score += 1
                self.player_score_label.config(text=f"Player (X): {self.player_score}")
                self.display_message("You win!")
            elif self.check_draw():
                self.display_message("It's a draw!")
            else:
                self.root.after(500, self.ai_move)

    def ai_move(self):
        level = self.difficulty.get()
        move = (
            self.get_random_move() if level == "Easy" else
            self.get_medium_move() if level == "Medium" else
            self.get_best_move()
        )
        if move:
            x, y = move
            self.board[x][y] = "O"
            self.buttons[x][y].config(text="O", bg="#a3be8c", relief="sunken")

        winner = self.check_winner(self.board)
        if winner == "O":
            self.ai_score += 1
            self.ai_score_label.config(text=f"AI (O): {self.ai_score}")
            self.display_message("AI wins!")
        elif self.check_draw():
            self.display_message("It's a draw!")

    def get_random_move(self):
        empty = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == ""]
        return random.choice(empty) if empty else None

    def get_medium_move(self):
        for symbol in ["O", "X"]:
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == "":
                        self.board[i][j] = symbol
                        if self.check_winner(self.board) == symbol:
                            self.board[i][j] = ""
                            return (i, j)
                        self.board[i][j] = ""
        return self.get_random_move()

    def get_best_move(self):
        best_score = -float('inf')
        best_move = None
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "":
                    self.board[i][j] = "O"
                    score = self.minimax(self.board, False)
                    self.board[i][j] = ""
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        return best_move

    def minimax(self, board, is_maximizing):
        winner = self.check_winner(board)
        if winner == "O": return 1
        if winner == "X": return -1
        if all(cell != "" for row in board for cell in row): return 0

        if is_maximizing:
            return max(self.minimax(self.try_move(board, i, j, "O"), False)
                       for i in range(3) for j in range(3) if board[i][j] == "")
        else:
            return min(self.minimax(self.try_move(board, i, j, "X"), True)
                       for i in range(3) for j in range(3) if board[i][j] == "")

    def try_move(self, board, i, j, symbol):
        new_board = [row[:] for row in board]
        new_board[i][j] = symbol
        return new_board

    def check_winner(self, board):
        for row in board:
            if row[0] == row[1] == row[2] != "":
                return row[0]
        for col in range(3):
            if board[0][col] == board[1][col] == board[2][col] != "":
                return board[0][col]
        if board[0][0] == board[1][1] == board[2][2] != "":
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] != "":
            return board[0][2]
        return None

    def check_draw(self):
        return all(all(cell != "" for cell in row) for row in self.board)

    def reset_game(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="", bg="#4c566a", relief="raised")
        self.message_label.config(text="")

    def display_message(self, message):
        self.message_label.config(text=message)
        self.root.after(2500, lambda: self.message_label.config(text=""))


if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToe(root)
    root.mainloop()
