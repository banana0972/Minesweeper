import tkinter as tk
from tkinter import StringVar

import minesweep
from minesweep import *

difficulties = {
    "easy": (6, 12, 10)
    "medium": (10, 20, 35)
    "hard": (13, 27, 75)
}

difficulty = input()
while difficulty not in difficulies:
    difficulty = input()
config = difficulties[difficulty]
width, height = config[0], config[1]
minesweep.width, minesweep.height = config[0], config[1]

game_board = generate(width, height, -1)
mines = generate(width, height, False)
flags = generate(width, height, False)
populate_field(mines, config[2])
dead = False
first_click = True

window = tk.Tk()
WINDOW_WIDTH, WINDOW_HEIGHT = width*50, (height+1) * 50
window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
window.resizable(False, False)

pixel = tk.PhotoImage(width=1, height=1)

text = StringVar()
text.set("MINESWEEP")
label = tk.Label(textvariable=text)
label.grid(row=0, column=0, columnspan=width)
visual_board: list[list[StringVar]] = []
for x in range(width):
    row = []
    for y in range(height):
        row.append(StringVar())
    visual_board.insert(0, row)


def interact(x: int, y: int):
    global first_click
    if first_click:
        repopulate(mines, x, y)
        first_click = False
    global dead
    if dead:
        return
    dead = minesweep.interact(game_board, mines, flags, x, y, [])
    draw_board()


def flag(x: int, y: int):
    # print("flag")
    global dead
    if dead or get_index(game_board, x, y) != -1:
        return
    set_index(flags, x, y, not get_index(flags, x, y))
    draw_board()

def draw_board():
    if dead:
        text.set("YOU DIED")
    for x in range(width):
        for y in range(height):
            count = minesweep.get_index(game_board, x, y)
            icon = str(count) if count != -1 else " "
            if minesweep.get_index(flags, x, y):
                icon = "🚩"
            if dead and minesweep.get_index(mines, x, y):
                icon = "💣"
            visual_board[y][x].set(icon)


for x in range(width):
    for y in range(height):
        # https://stackoverflow.com/questions/46284901/how-do-i-resize-buttons-in-pixels-tkinter
        button = tk.Button(textvariable=visual_board[y][x], image=pixel, width=25, height=25, compound='c', padx=0, pady=0)
        # https://docs.python.org/3/faq/programming.html#why-do-lambdas-defined-in-a-loop-with-different-values-all-return-the-same-result
        button.bind("<Button-1>", lambda event, i=x, j=y: interact(i, j))
        button.bind("<Button-3>", lambda event, i=x, j=y: flag(i, j))
        button.grid(row=x+1, column=y)

window.mainloop()
