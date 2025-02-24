import random
import time
import numpy as np
from copy import deepcopy

NUM_ROWS = 6
NUM_COLS = 7

class State:
    def __init__(self):
        self.board = np.zeros((NUM_ROWS, NUM_COLS))  # Tabuleiro vazio
        self.column_heights = [NUM_ROWS - 1] * NUM_COLS  # Índices disponíveis para cada coluna
        self.available_moves = list(range(NUM_COLS))  # Colunas disponíveis para jogar
        self.player = 1
        self.winner = -1  # -1 = em jogo, 0 = empate, 1 = jogador 1, 2 = jogador 2
    
    def move(self, column):
        """Executa um movimento na coluna escolhida."""
        state_copy = deepcopy(self)
        row = state_copy.column_heights[column]
        state_copy.board[row][column] = self.player
        state_copy.column_heights[column] -= 1
        
        if state_copy.column_heights[column] < 0:
            state_copy.available_moves.remove(column)
        
        state_copy.update_winner()
        state_copy.player = 3 - self.player  # Alternar jogadores
        return state_copy
    
    def update_winner(self):
        """Verifica se há um vencedor ou empate."""
        for row in range(NUM_ROWS):
            for col in range(NUM_COLS):
                if col < NUM_COLS - 3 and all(self.board[row][col + i] == self.player for i in range(4)):
                    self.winner = self.player
                    return
                if row < NUM_ROWS - 3 and all(self.board[row + i][col] == self.player for i in range(4)):
                    self.winner = self.player
                    return
                if row < NUM_ROWS - 3 and col < NUM_COLS - 3 and all(self.board[row + i][col + i] == self.player for i in range(4)):
                    self.winner = self.player
                    return
                if row > 2 and col < NUM_COLS - 3 and all(self.board[row - i][col + i] == self.player for i in range(4)):
                    self.winner = self.player
                    return
        if all(self.column_heights[col] < 0 for col in range(NUM_COLS)):
            self.winner = 0  # Empate
    
    def count_lines(self, n, player):
        """Conta quantas sequências de tamanho n existem no tabuleiro."""
        num_lines = 0
        for row in range(NUM_ROWS):
            for col in range(NUM_COLS):
                if col < NUM_COLS - 3 and self._check_line(n, player, [self.board[row][col + i] for i in range(4)]):
                    num_lines += 1
                if row < NUM_ROWS - 3 and self._check_line(n, player, [self.board[row + i][col] for i in range(4)]):
                    num_lines += 1
        return num_lines
    
    def _check_line(self, n, player, values):
        return values.count(player) == n and values.count(0) == 4 - n
    
    def central(self, player):
        """Atribui mais pontos às peças centrais."""
        score = 0
        for row in range(NUM_ROWS):
            for col in range(NUM_COLS):
                if self.board[row][col] == player:
                    score += 2 if col == 3 else 1 if col in [2, 4] else 0
        return score

# Implementação do Minimax com Poda Alpha-Beta
def minimax(state, depth, alpha, beta, maximizing, evaluate_func):
    if depth == 0 or state.winner != -1:
        return evaluate_func(state), None
    
    best_move = None
    if maximizing:
        max_eval = float('-inf')
        for move in state.available_moves:
            new_state = state.move(move)
            eval, _ = minimax(new_state, depth-1, alpha, beta, False, evaluate_func)
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in state.available_moves:
            new_state = state.move(move)
            eval, _ = minimax(new_state, depth-1, alpha, beta, True, evaluate_func)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move

def execute_minimax_move(game, evaluate_func, depth=4):
    _, best_move = minimax(game.state, depth, float('-inf'), float('inf'), True, evaluate_func)
    if best_move is not None:
        game.state = game.state.move(best_move)

def execute_random_move(game):
    move = random.choice(game.state.available_moves)
    game.state = game.state.move(move)

# Funções de avaliação (heurísticas)
def evaluate_f1(state):
    return state.count_lines(4, 1) - state.count_lines(4, 2)

def evaluate_f2(state):
    return evaluate_f1(state) * 100 + state.count_lines(3, 1) - state.count_lines(3, 2)

def evaluate_f3(state):
    return 100 * evaluate_f1(state) + state.central(1) - state.central(2)

def evaluate_f4(state):
    return 5 * evaluate_f2(state) + evaluate_f3(state)

# Classe do jogo Connect Four
class ConnectFourGame:
    def __init__(self, player_1_ai, player_2_ai):
        self.state = State()
        self.player_1_ai = player_1_ai
        self.player_2_ai = player_2_ai
    
    def run_n_matches(self, n, log_moves=False):
        results = [0, 0, 0]
        for _ in range(n):
            self.state = State()
            while self.state.winner == -1:
                (self.player_1_ai if self.state.player == 1 else self.player_2_ai)(self)
                if log_moves:
                    print(self.state.board)
            results[self.state.winner] += 1
        print(f"Resultados: {results[1]} vitórias do Jogador 1, {results[2]} do Jogador 2, {results[0]} empates")

# Testes - Minimax vs Random
print("Minimax (EvalF1) vs Random")
game = ConnectFourGame(lambda g: execute_minimax_move(g, evaluate_f1, 4), execute_random_move)
game.run_n_matches(10)

print("Minimax (EvalF4) vs Random")
game = ConnectFourGame(lambda g: execute_minimax_move(g, evaluate_f4, 4), execute_random_move)
game.run_n_matches(10)
