import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe Game")
        self.root.attributes('-fullscreen', True)  # Open as fullscreen
        self.current_player = "X"
        self.player_symbol = ""
        self.ai_symbol = ""
        self.board = [""] * 9
        self.hint_used = False

        self.create_widgets()
        self.style_window()

    def style_window(self):
        self.root.configure(bg="black")  # Set window background color
        self.root.option_add('*TLabel.background', 'black')  # Set label background color
        self.root.option_add('*TLabel.foreground', 'white')  # Set label text color

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def create_widgets(self):
        self.frame = tk.Frame(self.root, bg="black")
        self.frame.pack(expand=True, fill="both")

        self.buttons = []
        for i in range(9):
            button = tk.Button(self.frame, text="", font=("Arial", 36), width=6, height=3,
                               bg="black", fg="white", command=lambda i=i: self.make_move(i))
            button.grid(row=i//3, column=i%3, padx=5, pady=5)
            self.buttons.append(button)

        self.options_frame = tk.Frame(self.root, bg="black")
        self.options_frame.pack(side="bottom", pady=20)

        self.label = tk.Label(self.options_frame, text="Choose your symbol:", font=("Arial", 14), fg="white", bg="black")
        self.label.pack(side="left")

        self.x_button = tk.Button(self.options_frame, text="X", font=("Arial", 14), width=3, command=lambda: self.set_player_symbol("X"))
        self.x_button.pack(side="left", padx=10)

        self.o_button = tk.Button(self.options_frame, text="O", font=("Arial", 14), width=3, command=lambda: self.set_player_symbol("O"))
        self.o_button.pack(side="left", padx=10)

        self.hint_button = tk.Button(self.options_frame, text="Hint", font=("Arial", 14), command=self.show_hint)
        self.hint_button.pack(side="left", padx=20)

    def set_player_symbol(self, symbol):
        self.player_symbol = symbol
        self.ai_symbol = "O" if symbol == "X" else "X"
        self.label.config(text=f"You are {self.player_symbol}. Your turn!")
        if self.ai_symbol == "O":
            self.current_player = self.ai_symbol
            self.ai_move()
        else:
            self.current_player = self.player_symbol

    def make_move(self, index):
        if self.board[index] == "" and self.current_player == self.player_symbol:
            self.board[index] = self.player_symbol
            self.buttons[index].config(text=self.player_symbol, fg="red" if self.player_symbol == "X" else "white", bg="#DBB3FF")  # Lilac color
            if self.check_winner(self.player_symbol):
                self.end_game(f"{self.player_symbol} wins!")
            elif "" not in self.board:
                self.end_game("It's a draw!")
            else:
                self.current_player = self.ai_symbol
                self.ai_move()

    def ai_move(self):
        empty_indices = [i for i, x in enumerate(self.board) if x == ""]
        if empty_indices:
            # Try to win if possible
            for index in empty_indices:
                self.board[index] = self.ai_symbol
                if self.check_winner(self.ai_symbol):
                    self.buttons[index].config(text=self.ai_symbol, fg="red" if self.ai_symbol == "X" else "white", bg="#E8D2F2")  # Light purple color
                    self.current_player = self.player_symbol
                    self.end_game(f"{self.ai_symbol} wins!")
                    return
                self.board[index] = ""

            # Block player from winning
            for index in empty_indices:
                self.board[index] = self.player_symbol
                if self.check_winner(self.player_symbol):
                    self.board[index] = self.ai_symbol
                    self.buttons[index].config(text=self.ai_symbol, fg="red" if self.ai_symbol == "X" else "white", bg="#E8D2F2")  # Light purple color
                    self.current_player = self.player_symbol
                    return
                self.board[index] = ""

            # Choose a random move if no immediate win or block
            ai_index = random.choice(empty_indices)
            self.board[ai_index] = self.ai_symbol
            self.buttons[ai_index].config(text=self.ai_symbol, fg="red" if self.ai_symbol == "X" else "white", bg="#E8D2F2")  # Light purple color
            if self.check_winner(self.ai_symbol):
                self.end_game(f"{self.ai_symbol} wins!")
            elif "" not in self.board:
                self.end_game("It's a draw!")
            else:
                self.current_player = self.player_symbol

    def show_hint(self):
        if not self.hint_used:
            empty_indices = [i for i, x in enumerate(self.board) if x == ""]
            if empty_indices:
                hint_index = random.choice(empty_indices)
                self.buttons[hint_index].config(bg="green")
                self.hint_used = True
                self.hint_button.config(state="disabled")

    def check_winner(self, symbol):
        win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
        return any(self.board[a] == self.board[b] == self.board[c] == symbol for a, b, c in win_conditions)

    def end_game(self, message):
        messagebox.showinfo("Game Over", message)
        self.reset_game()

    def reset_game(self):
        self.board = [""] * 9
        for button in self.buttons:
            button.config(text="", bg="black")
        self.hint_used = False
        self.hint_button.config(state="normal")
        self.label.config(text="Choose your symbol:")

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToe(root)
    root.mainloop()
