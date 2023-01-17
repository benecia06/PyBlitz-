from tkinter import messagebox, ttk
from pathlib import Path

import tkinter as tk
import random
import string
import sys


WORD_LEN = 5
MAX_TRIES = 6
COLOR_BORDER_HIGHLIGHT = "#565758"
COLOR_BLANK = "#121213"
COLOR_INCORRECT = "#3a3a3c"
COLOR_HALF_CORRECT = "#b59f3b"
COLOR_CORRECT = "#538d4e"
BOX_SIZE = 55
PADDING = 3

try:
    BASE_PATH = Path(sys._MEIPASS)
except AttributeError:
    BASE_PATH = Path(".")

VALID_WORDS_WORDLIST = BASE_PATH / "wordlists/wordle-allowed-guesses.txt"
ANSWERS_WORDLIST = BASE_PATH / "wordlists/wordle-answers.txt"
APP_ICON = BASE_PATH / "assets/pyblitz.ico"
BACKSPACE_ICON = BASE_PATH / "assets/backspace.png"
HELP_ICON = BASE_PATH / "assets/help.png"
SETTINGS_ICON = BASE_PATH / "assets/settings.png"

ANSWERS = set(word.upper()
              for word in open(ANSWERS_WORDLIST).read().splitlines())
ALL_WORDS = set(word.upper() for word in open(
    VALID_WORDS_WORDLIST).read().splitlines()) | ANSWERS


class Wordle(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.grid(sticky="ns")
        self.master.title("Pyblitz! - A Wordle Game")
        self.master.iconbitmap(APP_ICON)
        self.fullscreen = False

        self.master.bind("<F11>", self.fullscreen_toggle)
        self.master.bind("<Return>", self.check_word)
        self.master.bind("<BackSpace>", self.remove_letter)
        self.master.bind("<Key>", self.enter_letter)

        self.init_ui()
        self.new_game()

    def fullscreen_toggle(self, event=None):
        if self.fullscreen:
            self.master.wm_attributes("-fullscreen", False)
            self.fullscreen = False
        else:
            self.master.wm_attributes("-fullscreen", True)
            self.fullscreen = True

    def new_game(self):
        self.answer = random.choice(list(ANSWERS)).upper()
        self.words = [""] * 6
        self.correct_letters = set()
        self.half_correct_letter = set()
        self.incorrect_letters = set()

        # reset the labels and keyboard
        for i in range(MAX_TRIES):
            self.current_word = i
            self.update_labels()
        self.current_word = 0
        self.update_keyboard()

    def congratulate(self):
        title = ["Genius", "Magnificent", "Impressive",
                 "Splendid", "Great", "Phew"][self.current_word]
        message = "Wanna Play Another Game?"
        if messagebox.askyesno(title, message):
            self.new_game()
        else:
            self.master.destroy()

    def humiliate(self):
        title = "Better Luck Next Time!"
        message = f"One More Game?\n(BTW the word was {self.answer}.)"
        if messagebox.askyesno(title, message):
            self.new_game()
        else:
            self.master.destroy()

    def init_ui(self):
        self.icons = {
            "settings": tk.PhotoImage(file=SETTINGS_ICON),
            "help": tk.PhotoImage(file=HELP_ICON),
            "backspace": tk.PhotoImage(file=BACKSPACE_ICON),
        }

        # TOP BAR STARTS HERE
        container = tk.Frame(self, bg=COLOR_BLANK, height=40)
        container.grid(sticky="we")
        container.grid_columnconfigure(1, weight=1)

        # help button
        tk.Button(
            container,
            image=self.icons["help"],
            bg=COLOR_BLANK,
            border=0,
            cursor="hand2",
        ).grid(row=0, column=0)

        # title
        tk.Label(
            container,
            text="PyBlitz!",
            fg="#d7dadc",
            bg=COLOR_BLANK,
            font=("Helvetica Neue", 28, "bold"),
        ).grid(row=0, column=1)

        # settings button
        tk.Button(
            container,
            image=self.icons["settings"],
            bg=COLOR_BLANK,
            border=0,
            cursor="hand2",
        ).grid(row=0, column=2)
        # TOP BAR ENDS HERE

        # separator
        ttk.Separator(self).grid(sticky="ew")
        tk.Frame(self, bg=COLOR_BLANK, height=40).grid()

        # GAME GRID STARTS HERE
        # if there is extra space then give it to main game grid
        self.rowconfigure(3, weight=1)
        container = tk.Frame(self, bg=COLOR_BLANK)
        container.grid()

        self.labels = []
        for i in range(MAX_TRIES):
            row = []
            for j in range(WORD_LEN):
                cell = tk.Frame(
                    container,
                    width=BOX_SIZE,
                    height=BOX_SIZE,
                    highlightthickness=1,
                    highlightbackground=COLOR_INCORRECT,
                )
                cell.grid_propagate(0)
                cell.grid_rowconfigure(0, weight=1)
                cell.grid_columnconfigure(0, weight=1)
                cell.grid(row=i, column=j, padx=PADDING, pady=PADDING)
                t = tk.Label(
                    cell,
                    text="",
                    justify="center",
                    font=("Helvetica Neue", 24, "bold"),
                    bg=COLOR_BLANK,
                    fg="#d7dadc",
                    highlightthickness=1,
                    highlightbackground=COLOR_BLANK,
                )
                t.grid(sticky="nswe")
                row.append(t)
            self.labels.append(row)
        # GAME GRID ENDS HERE

        # bottom empty separator
        tk.Frame(self, bg=COLOR_BLANK, height=40).grid()

        # VIRTUAL KEYBOARD STARTS HERE
        container = tk.Frame(self, bg=COLOR_BLANK)
        container.grid()

        # adding all the alphabets
        self.keyboard_buttons = {}
        for i, keys in enumerate(["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]):
            row = tk.Frame(container, bg=COLOR_BLANK)
            row.grid(row=i, column=0)

            for j, c in enumerate(keys):
                if i == 2:  # leave one column for the ENTER button in the last row
                    j += 1

                cell = tk.Frame(
                    row,
                    width=40,
                    height=55,
                    highlightthickness=1,
                    highlightbackground=COLOR_INCORRECT,
                )
                cell.grid_propagate(0)
                cell.grid_rowconfigure(0, weight=1)
                cell.grid_columnconfigure(0, weight=1)
                cell.grid(row=0, column=j, padx=PADDING, pady=PADDING)
                btn = tk.Button(
                    cell,
                    text=c,
                    justify="center",
                    font=("Helvetica Neue", 13),
                    bg=COLOR_BLANK,
                    fg="#d7dadc",
                    cursor="hand2",
                    border=0,
                    command=lambda c=c: self.enter_letter(key=c),
                )
                btn.grid(sticky="nswe")
                self.keyboard_buttons[c] = btn

        # adding the enter and delete buttons
        for col, text, func in ((0, "ENTER", self.check_word), (8, "", self.remove_letter)):
            cell = tk.Frame(
                row,
                width=75,
                height=55,
                highlightthickness=1,
                highlightbackground=COLOR_INCORRECT,
            )
            cell.grid_propagate(0)
            cell.grid_rowconfigure(0, weight=1)
            cell.grid_columnconfigure(0, weight=1)
            cell.grid(row=0, column=col, padx=PADDING, pady=PADDING)
            btn = tk.Button(
                cell,
                text=text,
                justify="center",
                font=("Helvetica Neue", 13),
                bg=COLOR_BLANK,
                fg="#d7dadc",
                cursor="hand2",
                border=0,
                command=func,
            )
            btn.grid(row=0, column=0, sticky="nswe")

        # set the image for delete button
        btn.configure(image=self.icons["backspace"])

        # VIRTUAL KEYBOARD ENDS HERE

    def update_keyboard(self):
        for key, btn in self.keyboard_buttons.items():
            if key in self.correct_letters:
                btn["bg"] = COLOR_CORRECT
            elif key in self.half_correct_letter:
                btn["bg"] = COLOR_HALF_CORRECT
            elif key in self.incorrect_letters:
                btn["bg"] = COLOR_INCORRECT
            else:
                btn["bg"] = COLOR_BLANK

    def update_labels(self, colors=None):
        word = self.words[self.current_word]
        for i, label in enumerate(self.labels[self.current_word]):
            try:
                letter = word[i]
            except IndexError:
                letter = ""

            label["text"] = letter
            if colors:
                label["bg"] = colors[i]
                label["highlightbackground"] = colors[i]
            else:
                label["bg"] = COLOR_BLANK
                label["highlightbackground"] = COLOR_BORDER_HIGHLIGHT if letter else COLOR_BLANK

    def check_word(self, event=None):
        print("checking word:", self.words[self.current_word])
        word = self.words[self.current_word]
        # ADD WORDLE LOGIC HERE
        if len(word)<WORD_LEN:
            print("Not enough letters")
        #CHECK IF WORD IS SHORTER THAN 5 letters
        if word not in ALL_WORDS:
            print(f"Not legitimate word. Try again")
        #CHECK IF WORD ENTERED IS A LEGITIMATE WORD
        def find_char_pos(word,char):
            positions=[]
            pos= word.find(char)
            while pos!= -1:
                positions.append(pos)
                pos = word.find(char, pos + 1)
            return positions
        colors = [COLOR_INCORRECT]*len(self.answer)
        counted_pos=set()
        for index,(guess, expected) in enumerate(zip(word,self.answer)):
            if guess==expected:
                counted_pos.add(index)
                colors.append(COLOR_CORRECT)
        for index, guess in enumerate(word):
            if guess in self.answer and colors[index]!=COLOR_CORRECT:
                positions= find_char_pos(self.answer, guess)

                for pos in positions:
                    if pos not in counted_pos:
                        colors.append(COLOR_HALF_CORRECT)

                        break
                
            return colors

        #ITERATE THROUGH ENTERED WORD AND WORDLE WORD
            """
            3 cases
            1) i = j THEN APPEND GREEN TO color array
            2) check frequency of x in wordle word, if it exists then append COLOR_HALF_CORRECT
            3) else incorrect append COLOR_INCORRECT
            """

        if word == self.answer:
            self.congratulate()

        self.current_word += 1
        if self.current_word >= MAX_TRIES:
            self.humiliate()

    def remove_letter(self, event=None):
        if self.words[self.current_word]:
            print(self.words[self.current_word][-1], "was deleted.")
            self.words[self.current_word] = self.words[self.current_word][:-1]
            self.update_labels()

    def enter_letter(self, event=None, key=None):
        key = key or event.keysym.upper()
        if key in string.ascii_uppercase:
            print(key, "was entered.")
            self.words[self.current_word] += key
            # prevent user from entering excess letters
            self.words[self.current_word] = self.words[self.current_word][:WORD_LEN]
            self.update_labels()


if __name__ == "__main__":
    # initialize the app
    root = tk.Tk()
    root.configure(bg=COLOR_BLANK)
    app = Wordle(root, bg=COLOR_BLANK)

    # center the frame
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    # run the app
    app.mainloop()
