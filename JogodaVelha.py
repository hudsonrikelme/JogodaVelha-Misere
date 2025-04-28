import tkinter as tk
import math
import copy

HUMAN = 'X'
AI = 'O'
EMPTY = ' '

# Representação do nó
class Node:
    def __init__(self, estado, pai=None, acao=None, custo=0):
        self.estado = estado
        self.pai = pai
        self.acao = acao
        self.custo = custo

# Inicializar tabuleiro
def init_board():
    return [[EMPTY for _ in range(3)] for _ in range(3)]

# Checar se o jogador perdeu (formou uma linha de três)
def check_lose(estado, player):
    for i in range(3):
        if estado[i][0] == estado[i][1] == estado[i][2] == player:
            return True
        if estado[0][i] == estado[1][i] == estado[2][i] == player:
            return True
    if estado[0][0] == estado[1][1] == estado[2][2] == player:
        return True
    if estado[0][2] == estado[1][1] == estado[2][0] == player:
        return True
    return False

def is_full(estado):
    return all(EMPTY not in row for row in estado)

# acoes(estado): retorna lista de posições (i, j) possíveis
def acoes(estado):
    return [(i, j) for i in range(3) for j in range(3) if estado[i][j] == EMPTY]

# resultado(estado, acao): retorna novo estado aplicando a ação
def resultado(estado, acao, player):
    new_state = copy.deepcopy(estado)
    i, j = acao
    new_state[i][j] = player
    return new_state

# Minimax usando os nós
def minimax(node, depth, is_ai):
    if check_lose(node.estado, HUMAN):
        return 10 - depth
    if check_lose(node.estado, AI):
        return depth - 10
    if is_full(node.estado):
        return 0

    if is_ai:
        best = -math.inf
        for action in acoes(node.estado):
            new_estado = resultado(node.estado, action, AI)
            child = Node(new_estado, node, action, node.custo + 1)
            score = minimax(child, depth + 1, False)
            best = max(best, score)
        return best
    else:
        best = math.inf
        for action in acoes(node.estado):
            new_estado = resultado(node.estado, action, HUMAN)
            child = Node(new_estado, node, action, node.custo + 1)
            score = minimax(child, depth + 1, True)
            best = min(best, score)
        return best

# IA escolhe movimento
def ai_move():
    global board

    best_val = -math.inf
    best_move = None
    current_node = Node(board)

    for action in acoes(board):
        new_estado = resultado(board, action, AI)
        child = Node(new_estado, current_node, action, current_node.custo + 1)
        move_val = minimax(child, 0, False)
        if move_val > best_val:
            best_val = move_val
            best_move = action

    if best_move:
        i, j = best_move
        board[i][j] = AI
        buttons[i][j]['text'] = AI
        buttons[i][j]['state'] = 'disabled'
        root.update()

        if check_lose(board, AI):
            status_label.config(text="Você venceu!")
            disable_all_buttons()
        elif is_full(board):
            status_label.config(text="Empate!")
        else:
            status_label.config(text="Sua vez!")

# Jogada do humano
def human_move(i, j):
    global board
    if board[i][j] == EMPTY:
        board[i][j] = HUMAN
        buttons[i][j]['text'] = HUMAN
        buttons[i][j]['state'] = 'disabled'

        if check_lose(board, HUMAN):
            status_label.config(text="Você perdeu!")
            disable_all_buttons()
        elif is_full(board):
            status_label.config(text="Empate!")
        else:
            status_label.config(text="IA pensando...")
            root.update()
            ai_move()

def disable_all_buttons():
    for i in range(3):
        for j in range(3):
            buttons[i][j]['state'] = 'disabled'

def reset_game():
    global board
    board = init_board()
    status_label.config(text="Sua vez!")
    for i in range(3):
        for j in range(3):
            buttons[i][j]['text'] = ' '
            buttons[i][j]['state'] = 'normal'

# --- Interface Gráfica com Canvas para as divisões ---
root = tk.Tk()
root.title("Misère - Evite Ganhar!")
root.configure(bg='white')

board = init_board()
buttons = [[None for _ in range(3)] for _ in range(3)]

button_style = {
    'font': ('Helvetica', 36),
    'width': 4,
    'height': 2,
    'bg': 'white',
    'fg': '#333',
    'bd': 0,
    'activebackground': '#eee'
}

# Criar Canvas para desenhar as divisões
canvas = tk.Canvas(root, width=320, height=320, bg='white', bd=0, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=3)

# Desenhar as linhas de divisão sem sobreposição no centro dos botões
def draw_grid():
    # Ajustar as linhas para não se sobrepor ao centro dos botões
    for i in range(1, 3):
        # Linhas verticais (ajustadas para não sobrepor os botões)
        canvas.create_line(i * 105, 5, i * 105, 315, fill="black", width=2)
        # Linhas horizontais (ajustadas para não sobrepor os botões)
        canvas.create_line(5, i * 105, 315, i * 105, fill="black", width=2)

# Chamar função para desenhar a grade
draw_grid()

# Criar botões e posicioná-los sobre a grade
for i in range(3):
    for j in range(3):
        btn = tk.Button(root, text=' ', command=lambda i=i, j=j: human_move(i, j), **button_style)
        btn.place(x=j * 105 + 5, y=i * 105 + 5, width=100, height=100)
        buttons[i][j] = btn

status_label = tk.Label(root, text="Sua vez!", font=('Helvetica', 18), bg='white', fg='#666')
status_label.grid(row=3, column=0, columnspan=3, pady=(10, 0))

reset_button = tk.Button(root, text="Reiniciar", font=('Helvetica', 14), bg='#f5f5f5', fg='#666',
                         bd=0, highlightthickness=1, highlightbackground='#ccc',
                         activebackground='#ddd', command=reset_game)
reset_button.grid(row=4, column=0, columnspan=3, pady=10)

root.mainloop()
