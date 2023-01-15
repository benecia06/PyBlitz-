'''
TODO:
[] Add GUI 
[] Add choice to select fonts?
[] Custom Themes?
[] Figure out a way to get the Wordle wordlist
[] add a virtual keyboard
[] make executable
'''
from tkinter import messagebox, ttk
from pathlib import Path
import tkinter as tk
import random
import sys
import string

BOX_SIZE = 60
COLOR_BORDER = "#565758"
COLOR_BLANK = "#121213"
COLOR_CORRECT = "#538d4e"
COLOR_CLOSE = "#b59f3b"
COLOR_INCORRECT = "#3a3a3c"
PADDING = 5


class Wordle(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.grid(sticky="ns")
        self.master.title("PyBlitz! - A Wordle Game")
        # self.master.iconbitmap("PyBlitz_icon.ico")
        self.master.resizable(False, False)
        self.fullscreen = False
        self.master.bind("<F11>", self.toggle_fullscreen)
        self.master.bind("<Return>", self.check_word)
        self.master.bind("<BackSpace>", self.remove_letter)
        self.master.bind("<Key>", self.add_letter)

        self.init_ui()
        self.new_game()

    def fullscreen_toggle(self, event=None):
        if self.fullscreen:
            self.master.attributes("-fullscreen", False)
            self.fullscreen = False
        else:
            self.master.attributes("-fullscreen", True)
            self.fullscreen = True

    def new_game(self):
        # self.word = CHOOSE TODAYS WORD FROM WORDLIST
        self.words = [""] * 6  # 6 Tries
        self.correct_letters = set()
        self.close_letters = set()
        self.incorrect_letters = set()

        # resetting the board
        for i in range(6):
            self.current_word = i
            self.update_labels()
        self.current_word = 0
        self.update_keyboard()

    def congralutions(self):
        concat_string = "PyBlitz! "
        title = ["Genius", "Magnificent", "Impressive",
                 "Splendid", "Great", "Phew"][self.current_word]
        message = "Do you want to play again?"
        if messagebox.askyesno(concat_string+title, message):
            self.new_game()


if __name__ == "__main__":
    # initializing the app
    root = tk.Tk()
    root.configure(bg=COLOR_BLANK)
    app = Wordle(root, bg=COLOR_BLANK)

    # centering the app
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    # running the app
    app.mainloop()
