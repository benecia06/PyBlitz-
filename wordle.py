import tkinter as tk
import tkinter.font as tkFont
from tkinter.constants import DISABLED, NORMAL, END
from math import floor
from typing import List

class App:
    def __init__(self, root, line_submit_callback):

        self.root = root
        self.letter_font = tkFont.Font(family='Times',size=20)
        self.line_submit_callback = line_submit_callback
        self.notif_var = tk.StringVar(root, "Notifications...")

        #setting title
        root.title("undefined")
        #setting window size
        width = 420
        height=500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = f'{width}x{height}+{(screenwidth - width) // 2}+{(screenheight - height) // 2}'
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        title_font = tkFont.Font(family='Times',size=28)
        title_label = tk.Label(root, font=title_font, fg="#333333", justify="center", text="Wordle", relief="flat")
        title_label.place(x=0, y=0, width=width, height=70)

        self._widget_map = []
        for row in range(1, 6): # from 1 to 5 inclusive
            y_pos = 70 * row + 10
            row_map = []
            for col in range(1, 6):
                new_letter_entry = self.generate_letter_widget()
                x_pos = 70 * col - 60
                new_letter_entry.place(x=x_pos, y=y_pos, width=50, height=50)

                row_map.append(new_letter_entry)
            
            self._widget_map.append(tuple(row_map))
    

        credit_font = tkFont.Font(family='Times', size=8)
        credit_label = tk.Label(root, font=credit_font, fg="#333333", justify="center", text="@Baileyac20 & @mrmjrx")
        credit_label.place(x=270, y=470, width=width, height=25)

        notif_font = tkFont.Font(family='Times',size=13)
        notif_label = tk.Label(root, font=notif_font, fg="#cc0000", justify="center", textvariable=self.notif_var)
        notif_label.place(x=0, y=420, width=width, height=50)

        self.submit_btn = tk.Button(root, fg="#333333", justify="center", text="✓")
        self.submit_btn.place(x=360, width=50, height=50)
        self.place_submit_btn_on_line(1)

    def generate_letter_widget(self) -> tk.Entry:
        return tk.Entry(self.root, borderwidth="1px", font=self.letter_font, fg="#333333", justify="center")
    
    def get_widget_map(self) -> tuple:
        return tuple(self._widget_map)

    def place_submit_btn_on_line(self, line_num):
        self.submit_btn.place_configure(y=70 * line_num + 10)
        self.submit_btn.config(command=lambda: self.line_submit_callback(line_num, self))


def on_line_submit(line_num, app):
    widgets: List[tk.Entry] = widget_map[line_num - 1]

    curr_word_letters_remaining = WORD
    word_submitted = ""
        
    for i, widget in enumerate(widgets):
        entered_chr = widget.get().lower()
        
        if len(entered_chr) > 1:
            widget.delete(1, END)
            entered_chr = widget.get().lower()

        word_submitted += entered_chr

        # Getting location info of label
        place_info = widget.place_info()
        x = place_info["x"]
        y = place_info["y"]
        width = place_info["width"]
        height = place_info["height"]

        widget.destroy()
        widget = tk.Label(root, font=app.letter_font, borderwidth="1px", justify="center", text=entered_chr)
        widget.place(x=x, y=y, width=width, height=height)

        # colouring label with info
        if WORD[i] == entered_chr:
            widget.config(fg=CORRECT_LETTER_PLACE_COL)

        elif entered_chr in curr_word_letters_remaining:
            widget.config(fg=CORRECT_LETTER_NPLACE_COL)
        
        else:
            widget.config(fg=INCORRECT_LETTER_COL)


    print(word_submitted)

    if word_submitted == WORD:
        return win()
    elif line_num == 5:
        return lose()
    else:
        app.place_submit_btn_on_line(line_num + 1)


def end_game():
    pass
    
    app.submit_btn.destroy()

def win():
    end_game()
    app.notif_var.set("VICTORY")

def lose():
    end_game()
    app.notif_var.set(f"LOSS - WORD WAS {WORD.upper()}") 

    
FPS = 60
FPS_TIMESTAMP = 1000 // FPS
WORD = "tests"

CORRECT_LETTER_PLACE_COL = "#00cc00"
CORRECT_LETTER_NPLACE_COL = "#cccc00"
INCORRECT_LETTER_COL = "#cc0000"

root = tk.Tk()
app = App(root, on_line_submit)
widget_map = app.get_widget_map()

root.mainloop()