import tkinter as tk
import math

HUMAN = 'X'
AI = 'O'
EMPTY = ''


def init_board():
    global init_board
    board = [[EMPTY for _ in range(3)] for _ in range(3)]




root = tk.Tk()
root.title("Jogo da Velha Misère - Evite vencer!")







#inicia o jogo
init_board()
root.mainloop()