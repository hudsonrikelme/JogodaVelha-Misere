import tkinter as tk
import math

HUMAN = 'X'
AI = 'O'
EMPTY = ''

# Representação do nó
class Node:
    def __init__(self, estado, pai = None, acao = None, custo = 0):
        self.estado = estado
        self.pai = pai
        self.acao = acao
        self.custo = custo

# inicializa tabuleiro
def init_board():
    return [[EMPTY for _ in range(3)] for _ in range(3)]

# checar se o jogador perdeu
def check_lose(estado, player):
    for i in range(3):
        if estado[i][0] == estado[i][1] == estado[i][2] == player:
            return True
        if estado[0][i] == estado [1][i] == estado[2][i] == player:
            return True
    if estado[0][0] == estado[1][1] == estado[2][2] == player:
        return True
    if estado[0][2] == estado[1][1] == estado[2][0] == player:
        return True
    return False

# acoes(estado): retorna lista de posições (i, j) possíveis
def acoes(estado):
    moves = []
    for i in range(3):
        for j in range(3):
            if estado[i][j] == EMPTY:
                moves.append((i,j))
    return moves



def human_move(i, j):
    global board
    if board[i][j] == EMPTY:
        board[i][j] = HUMAN
        buttons[i][j]['text'] = HUMAN
        buttons[i][j]['state'] = 'disable'

        if check_lose(board, HUMAN):
            status_label.config(text = "Você perdeu! Formou uma linha!")
            disable_all_buttons()


def disable_all_buttons():
    for i in range(3):
        for j in range(3):
            buttons[i][j]['state'] = 'disabled'


def reset_game():
    global board
    board = init_board()
    status_label.config(text = "Sua Vez!")
    for i in range(3):
        for j in range(3):
            buttons[i][j]['text'] = ''
            buttons[i][j]['state'] = 'normal'

root = tk.Tk()
root.title("Jogo da Velha Misère - Evite vencer!")

buttons = [[None for _ in range(3)] for _ in range(3)]
board = init_board()

for i in range(3):
    for j in range(3):
        btn = tk.Button(root, text='', font = ('Helvetica', 40), width= 4, height=1,
                        command=lambda i = i, j = j: human_move(i, j))
        btn.grid(row = i, column =j)
        buttons[i][j] = btn


status_label = tk.Label(root, text = "Sua Vez!", font = ('Helvetica', 16))
status_label.grid(row=3, column=0, columnspan=3)

reset_button = tk.Button(root, text="Reiniciar", font = ('Helvetica', 16), command=reset_game)
reset_button.grid(row=4, column=0, columnspan=3, pady=10)

root.mainloop()