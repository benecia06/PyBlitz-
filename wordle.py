'''
TODO:
[X] Add GUI
[] Add choice to select fonts?
[] Custom Themes?
[] Figure out a way to get the Wordle wordlist
[X] add a virtual keyboard
[] make executable
'''
from tkinter import messagebox, ttk
from pathlib import Path
import tkinter as tk
import random
import sys
import string

BOX_SIZE = 60
COLOR_BORDER_HIGHLIGHT = "#565758"
COLOR_BLANK = "#121213"
COLOR_CORRECT = "#538d4e"
COLOR_CLOSE = "#b59f3b"
COLOR_INCORRECT = "#3a3a3c"
PADDING = 5

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
MANUAL_IMAGE = BASE_PATH / "assets/manual_image2.png"
ANSWERS = set(word.upper()
              for word in open(ANSWERS_WORDLIST).read().splitlines())
ALL_WORDS = set(word.upper() for word in open(
    VALID_WORDS_WORDLIST).read().splitlines()) | ANSWERS


class Manual(tk.Frame)


def __init__(self, master, *args, **kwargs):
    tk.Frame.__init__(self, master, *args, **kwargs)
    self.grid(sticky="ns")
    self.manual_image = tk.PhotoImage(file=MANUAL_IMAGE)
    tk.Label(self, image=self.manual_image).grid(sticky="nswe")


class Wordle(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.grid(sticky="ns")
        self.master.title("PyBlitz! - A Wordle Game")
        self.master.iconbitmap("APP_ICON")
        # self.master.resizable(False, False)
        self.fullscreen = False
        self.master.bind("<F11>", self.toggle_fullscreen)
        self.master.bind("<Return>", self.check_word)
        self.master.bind("<BackSpace>", self.remove_letter)
        self.master.bind("<Key>", self.add_letter)

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
        # self.word = CHOOSE TODAYS WORD FROM WORDLIST
        self.answer = random.choice(list(ANSWERS)).upper()
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
        else:
            self.master.destroy()

    def humiliate(self):
        title = "Better Luck Next Time"
        message = f"One More Game?\n The word was: {self.answer}."
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
        container = tk.Frame(self, bg=COLOR_BLANK, height=50)
        container.grid(sticky="we")
        container.grid_columnconfigure(1, weight=1)

        # help button
        tk.Button(
            container,
            image=self.icons["help"],
            bg=COLOR_BLANK,
            border=0,
            curson="hand2",
        ).grid(row=0, column=0)

        # TITLE
        tk.Label(
            container,
            text="PyBlitz!",
            fg="#d7dadc",
            bg=COLOR_BLANK,
            font=("Helvetica", 28, "bold"),
        ).grid(row=0, column=1)

        # settings button
        tk.Button(
            container,
            image=self.icons["settings"],
            bg=COLOR_BLANK,
            border=0,
            curson="hand2",
        ).grid(row=0, column=2)
        # END OF TOP BAR

        # SEPARATOR PADDING
        ttk.Separator(self).grid(sticky="ew")
        tk.Frame(self, bg=COLOR_BLANK, height=40).grid()

        # WORDLE BOARD STARTS HERE
        # extra space will be given to main game grid
        self.rowconfigure(3, weight=1)
        container = tk.Frame(self, bg=COLOR_BLANK)
        container.grid()

        self.labels = []
        for i in range(6):
            row = []
            for j in range(5):
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
                    font=("Helvetica", 24, "bold"),
                    bg=COLOR_BLANK,
                    fg="d7dadc",
                    highlightthickness=1,
                    highlightbackground=COLOR_BLANK,
                )
                t.grid(sticky="nswe")
                row.append(t)
            self.labels.append(row)
         # END OF WORDLE BOARD

        # SEPARATOR PADDING
        tk.Frame(self, bg=COLOR_BLANK, height=40).grid()

        # KEYBOARD STARTS HERE
        container = tk.Frame(self, bg=COLOR_BLANK)
        container.grid()

        # adding qwerty keyboard
        self.keyboard_buttons = {}
        for i, keys in enumerate(["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]):
            row = tk.Frame(container, bg=COLOR_BLANK)
            row.grid(row=i, column=0)

            for j, c in enumerate(keys):
                if i == 2:

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
                    font=("Helvetica", 13),
                    bg=COLOR_BLANK,
                    fg="d7dadc",
                    cursor="hand2",
                    border=0,
                    command=lambda c=c: self.enter_letter(key=c),
                )
                btn.grid(sticky="nswe")
                self.keyboard_buttons[c] = btn

        # adding enter and delete buttons
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
                font=("Helvetica", 13),
                bg=COLOR_BLANK,
                fg="d7dadc",
                cursor="hand2",
                border=0,
                command=func,
            )
            btn.grid(row=0, column=0, sticky="nswe")

        # delete button
        btn.configure(image=self.icons["backspace"])
        # END OF KEYBOARD

    def update_keyboard(self):
        for key, btn in self.keyboard_buttons.items():
            if key in self.correct_letters:
                btn["bg"] = COLOR_CORRECT
            elif key in self.close_letters:
                btn["bg"] = COLOR_CLOSE
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
        # word checking logic

    def enter_letter(self, event=None, key=None):
        # letter entering logic
        key = key or event.keysym.upper()
        if key in string.ascii_uppercase:
            print(key, "pressed")
            self.words[self.current_word] += key
            # preventing overflow of letters
            self.words[self.current_word] = self.words[self.current_word][:5]
            self.update_labels()


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
