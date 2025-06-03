import numpy as np
import random
import pygame
import time
import json
from copy import deepcopy
import math
import csv

# Constants for players and cell states
WHITE = 1
BLACK = -1
EMPTY = 0
# Board and display settings
CELL_SIZE = 25  
MARGIN = 50  
SCREEN_COLOR = (30, 30, 30)  
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)
GRID_COLOR = (200, 200, 200)
TEXT_COLOR = (255, 255, 255)

class PartitionsGame:
    def __init__(self, board_size=5):
        self.board_size = board_size
        self.board = []
        # Create a hexagonal board structure
        for row in range(2 * board_size - 1):  
            num_cols = board_size + min(row, 2 * board_size - row - 2)  
            self.board.append([EMPTY] * num_cols)

        self.current_player = WHITE 
        self.game_over = False 
    
    def is_valid_move(self, x, y):
        # Check if the move is inside the board and the cell is empty
        return 0 <= x < len(self.board) and 0 <= y < len(self.board[x]) and self.board[x][y] == EMPTY 


    def make_move(self, x, y):
        # Make a move if valid, then switch the player
        if self.is_valid_move(x, y):
            self.board[x][y] = self.current_player
            self.current_player *= -1  
            return True
        return False


    def get_empty_cells(self):
        """Return a list of all empty cells on the board."""
        empty_cells = []
        for row in range(len(self.board)):  
            for col in range(len(self.board[row])):  
                if self.board[row][col] == EMPTY:
                    empty_cells.append((row, col))
        return empty_cells

    
    
    def check_game_end(self):
        # Check if there are no more empty cells
        return len(self.get_empty_cells()) == 0
    
    def evaluate_score(self):
        visited = set()
        white_fragments = []
        black_fragments = []
        # Internal function to find all connected cells of the same color
        def get_group(x, y, color):
            group = set()
            stack = [(x, y)]
            while stack:
                cx, cy = stack.pop()
                if (cx, cy) in group or self.board[cx][cy] != color:
                    continue
                group.add((cx, cy))
                # Hexagonal neighbors
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, 1), (1, -1)]:
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < len(self.board) and 0 <= ny < len(self.board[nx]):
                        stack.append((nx, ny))
            return group
        
        def is_board_connected(exclude_cells):
            """Check if the board remains connected when excluding certain cells"""
            total_cells = [(x, y) for x in range(len(self.board)) for y in range(len(self.board[x])) if self.board[x][y] != EMPTY and (x, y) not in exclude_cells]
            if not total_cells:
                return True  

            visited = set()
            stack = [total_cells[0]]
            while stack:
                cx, cy = stack.pop()
                if (cx, cy) in visited:
                    continue
                visited.add((cx, cy))
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, 1), (1, -1)]:
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < len(self.board) and 0 <= ny < len(self.board[nx]):
                        if self.board[nx][ny] != EMPTY and (nx, ny) not in exclude_cells and (nx, ny) not in visited:
                            stack.append((nx, ny))

            return len(visited) == len(total_cells)
        # Iterate through all cells to identify and classify fragments
        for x in range(len(self.board)):
            for y in range(len(self.board[x])):
                if self.board[x][y] != EMPTY and (x, y) not in visited:
                    group = get_group(x, y, self.board[x][y])
                    visited.update(group)

                    if not is_board_connected(group):
                        continue

                    if self.board[x][y] == WHITE:
                        black_fragments.extend(group)
                    else:
                        white_fragments.extend(group)

        # Return the score as the difference between white and black fragment sizes
        return len(white_fragments) - len(black_fragments)

    def get_winner(self):
        score = self.evaluate_score()
        if score > 0:
            return WHITE
        elif score < 0:
            return BLACK
        else:
            # Tie-breaker by inverting fragment groups
            new_game = deepcopy(self) 

            visited = set()
            fragments_to_invert = []
            # Helper function to get a group of connected same-colored pieces
            def get_group(x, y, color):
                group = set()
                stack = [(x, y)]
                while stack:
                    cx, cy = stack.pop()
                    if (cx, cy) in group or new_game.board[cx][cy] != color:
                        continue
                    group.add((cx, cy))
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, 1), (1, -1)]:
                        nx, ny = cx + dx, cy + dy
                        if 0 <= nx < len(new_game.board) and 0 <= ny < len(new_game.board[nx]):
                            stack.append((nx, ny))
                return group
            # Check if the board remains connected without the given group
            def is_board_connected(exclude_cells):
                total_cells = [
                    (x, y)
                    for x in range(len(new_game.board))
                    for y in range(len(new_game.board[x]))
                    if new_game.board[x][y] != EMPTY and (x, y) not in exclude_cells
                ]
                if not total_cells:
                    return True

                visited_local = set()
                stack = [total_cells[0]]
                while stack:
                    cx, cy = stack.pop()
                    if (cx, cy) in visited_local:
                        continue
                    visited_local.add((cx, cy))
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, 1), (1, -1)]:
                        nx, ny = cx + dx, cy + dy
                        if (
                            0 <= nx < len(new_game.board)
                            and 0 <= ny < len(new_game.board[nx])
                            and new_game.board[nx][ny] != EMPTY
                            and (nx, ny) not in exclude_cells
                            and (nx, ny) not in visited_local
                        ):
                            stack.append((nx, ny))
                return len(visited_local) == len(total_cells)

            # Find all fragment groups on the board
            for x in range(len(new_game.board)):
                for y in range(len(new_game.board[x])):
                    if new_game.board[x][y] != EMPTY and (x, y) not in visited:
                        color = new_game.board[x][y]
                        group = get_group(x, y, color)
                        visited.update(group)
                        # If removing this group keeps the board connected, mark it for inversion
                        if is_board_connected(group):
                            fragments_to_invert.extend([(gx, gy, color) for gx, gy in group])

            # Invert the color of all marked fragments
            for x, y, color in fragments_to_invert:
                new_game.board[x][y] = -color  

            # Re-evaluate score after inversion and decide the winner
            final_score = new_game.evaluate_score()
            return WHITE if final_score > 0 else BLACK


class MinimaxAI:
    def __init__(self, depth=3):
        self.depth = depth

    def heuristic_bonus(self, game, x, y, current_player):
        opponent = -current_player
        bonus = 0
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, 1), (1, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(game.board) and 0 <= ny < len(game.board[nx]):
                if game.board[nx][ny] == current_player:
                    bonus += 2
                elif game.board[nx][ny] == opponent:
                    bonus += 1
        return bonus

    def minimax(self, game, depth, alpha, beta, maximizing_player):
        if depth == 0 or game.check_game_end():
            return game.evaluate_score(), None

        best_move = None
        moves = game.get_empty_cells()
        moves.sort(key=lambda move: self.heuristic_bonus(game, move[0], move[1], game.current_player), reverse=True)

        if maximizing_player:
            max_eval = float('-inf')
            for (x, y) in moves:
                new_game = deepcopy(game)
                new_game.make_move(x, y)
                eval, _ = self.minimax(new_game, depth - 1, alpha, beta, False)
                eval += self.heuristic_bonus(game, x, y, game.current_player)
                if eval > max_eval:
                    max_eval = eval
                    best_move = (x, y)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for (x, y) in moves:
                new_game = deepcopy(game)
                new_game.make_move(x, y)
                eval, _ = self.minimax(new_game, depth - 1, alpha, beta, True)
                eval -= self.heuristic_bonus(game, x, y, game.current_player)
                if eval < min_eval:
                    min_eval = eval
                    best_move = (x, y)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def best_move(self, game):
        empty_cells = len(game.get_empty_cells())
        # Defines the depth according to the board size
        size = game.board_size
        if size <= 5:
            self.depth = 4
        elif size <= 7:
            self.depth = 3
        elif size <= 9:
            self.depth = 2
        else:
            self.depth = 1  

        _, move = self.minimax(game, self.depth, float('-inf'), float('inf'), True)
        if move is None:
            empty_cells = game.get_empty_cells()
            if empty_cells:
                return random.choice(empty_cells)
        return move



import math

class MCTSNode:
    def __init__(self, game, parent=None):
        # Save a copy of the game state at this node
        self.game = deepcopy(game)
        self.parent = parent
        self.visits = 0      # Number of times this node was visited
        self.value = 0       # Total value from simulations
        self.children = []   # List of child nodes
        self.untried_moves = game.get_empty_cells()  # Moves not yet tried from this state

    def select_child(self):
        # Select the best child using UCB1 formula (exploitation + exploration)
        return max(self.children, key=lambda c: c.value / (c.visits + 1e-6) +
                   math.sqrt(2 * math.log(self.visits + 1) / (c.visits + 1e-6)))

    def expand(self):
        # Expand the node by trying one of the untried moves
        if self.untried_moves:
            move = self.untried_moves.pop()
            new_game = deepcopy(self.game)
            new_game.make_move(*move)
            child_node = MCTSNode(new_game, parent=self)
            self.children.append(child_node)
            return child_node
        return None

    def simulate(self):
        # Perform a random  playout from the current state
        temp_game = deepcopy(self.game)
        max_simulated_moves = 20 
        moves_played = 0
        while not temp_game.check_game_end() and moves_played < max_simulated_moves:
            move = self.heuristic_simulated_move(temp_game)
            temp_game.make_move(*move)
            moves_played += 1
        return temp_game.get_winner()

    def heuristic_simulated_move(self, game):
        # Choose a move based on proximity to friendly or enemy pieces 
        best_score = -float('inf')
        best_move = None
        for x, y in game.get_empty_cells():
            score = 0
            opponent = -game.current_player
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, 1), (1, -1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(game.board) and 0 <= ny < len(game.board[nx]):
                    if game.board[nx][ny] == game.current_player:
                        score += 2
                    elif game.board[nx][ny] == opponent:
                        score += 1
            if score > best_score:
                best_score = score
                best_move = (x, y)
        return best_move if best_move else random.choice(game.get_empty_cells())

    def backpropagate(self, result):
        # Update this node and its ancestors with the simulation result
        self.visits += 1
        if result == self.game.current_player:
            self.value += 1
        if self.parent:
            self.parent.backpropagate(result)


def mcts_best_move(game, simulations=None):
    # Determine board size for simulation 
    size = game.board_size
    if simulations is None:
        if size <= 5:
            simulations = 300
        elif size <= 7:
            simulations = 150
        elif size <= 9:
            simulations = 800
        elif size <= 11:
            simulations = 1000
        else:
            simulations = 1500

    root = MCTSNode(game)

    if not root.untried_moves:
        return None

    # Run MCTS simulations
    for _ in range(simulations):
        node = root
        while node.children and not node.untried_moves:
            node = node.select_child()
        new_node = node.expand() if node.untried_moves else node
        result = new_node.simulate() if new_node else node.simulate()
        (new_node or node).backpropagate(result)

    # If no children plays a random move
    if not root.children:
        empty = game.get_empty_cells()
        return random.choice(empty) if empty else None

    # Return the move that leads to the most visited child
    best_child = max(root.children, key=lambda c: c.visits)
    for x in range(len(game.board)):
        for y in range(len(game.board[x])):
            if game.board[x][y] != best_child.game.board[x][y]:
                return (x, y)

    return random.choice(game.get_empty_cells())


class AIPlayer:
    def __init__(self, difficulty, algorithm='minimax'):
        self.difficulty = difficulty 
        self.algorithm = algorithm  

    def best_move(self, game):
        if self.algorithm == 'minimax':
            if self.difficulty == 'easy':
                return random.choice(game.get_empty_cells())  
            elif self.difficulty == 'medium':
                ai = MinimaxAI()
                return ai.best_move(game)
            else:  # hard
                ai = MinimaxAI(depth=4)
                return ai.best_move(game)
        elif self.algorithm == 'mcts':
            return mcts_best_move(game, simulations=100 if self.difficulty == 'medium' else 500)


def suggest_move(game):
    ai = MinimaxAI(depth=2) 
    move = ai.best_move(game)
    
    # If minimax fails, return a random empty cell
    if move is None:
        empty_cells = game.get_empty_cells()
        if empty_cells:
            return random.choice(empty_cells)  
    return move



def draw_hexagonal_board(screen, game, hint_cell=None):
    """Draw a hexagonal game board, with optional hint highlighting."""
    screen.fill(SCREEN_COLOR)
    font = pygame.font.Font(None, 36)
    
    rows = len(game.board)
    cell_radius = CELL_SIZE // 2 
    hex_height = math.sqrt(3) * cell_radius 
    center_x = screen.get_width() // 2
    center_y = screen.get_height() // 2

    for row in range(rows):
        num_cols = len(game.board[row])
        offset_x = (rows - num_cols) * cell_radius 

        for col in range(num_cols):
            # Calculate screen position for each cell
            x = center_x + (col * 2 * cell_radius) - (num_cols - 1) * cell_radius
            y = center_y + (row - rows // 2) * hex_height

            pos = (int(x), int(y))
            # Highlight suggested move 
            if hint_cell == (row, col):
                pygame.draw.circle(screen, (0, 255, 0), pos, cell_radius+2, 3)  # Green highlight
            # Draw cell background and border
            pygame.draw.circle(screen, GRID_COLOR, pos, cell_radius)
            pygame.draw.circle(screen, BLACK_COLOR, pos, cell_radius, 2)
            # Draw the player's piece if the cell is occupied
            if game.board[row][col] == WHITE:
                pygame.draw.circle(screen, WHITE_COLOR, pos, cell_radius - 5)
            elif game.board[row][col] == BLACK:
                pygame.draw.circle(screen, BLACK_COLOR, pos, cell_radius - 5)
    # Display current player's turn
    text = f"Player's turn: {'White' if game.current_player == WHITE else 'Black'}"
    text_render = font.render(text, True, TEXT_COLOR)
    screen.blit(text_render, (MARGIN, 10))

    #Exit button
    menu_button_rect = pygame.Rect(screen.get_width() - 120, screen.get_height() - 50, 100, 35)
    pygame.draw.rect(screen, (180, 50, 50), menu_button_rect, border_radius=8)

    font = pygame.font.Font(None, 24)
    exit_text = font.render("Exit", True, (255, 255, 255))
    screen.blit(exit_text, (menu_button_rect.x + 25, menu_button_rect.y + 7))



    return menu_button_rect  #


def draw_board(screen, game):
    # Fill the screen with background color
    screen.fill(SCREEN_COLOR)
    font = pygame.font.Font(None, 36)
    # Draw the game grid and pieces
    for x in range(game.board_size):
        for y in range(game.board_size):
            # Define the rectangle for each cell
            rect = pygame.Rect(MARGIN + y * CELL_SIZE, MARGIN + x * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            # Draw the cell border
            pygame.draw.rect(screen, GRID_COLOR, rect, 2)
            # Draw pieces on the board
            if game.board[x][y] == WHITE:
                pygame.draw.circle(screen, WHITE_COLOR, rect.center, CELL_SIZE // 3)
            elif game.board[x][y] == BLACK:
                pygame.draw.circle(screen, BLACK_COLOR, rect.center, CELL_SIZE // 3)

    # Show current player's turn
    text = f"Player's turn: {'White' if game.current_player == WHITE else 'Black'}"
    text_render = font.render(text, True, TEXT_COLOR)
    screen.blit(text_render, (MARGIN, 10))



def get_cell_from_mouse(pos, game):
    """
    Converts the mouse click position to board coordinates
    """
    mouse_x, mouse_y = pos
    cell_radius = CELL_SIZE // 2
    hex_height = math.sqrt(3) * cell_radius
    center_x = pygame.display.get_surface().get_width() // 2
    center_y = pygame.display.get_surface().get_height() // 2
    rows = len(game.board)

    for row in range(rows):
        num_cols = len(game.board[row])
        offset_x = (rows - num_cols) * cell_radius
        for col in range(num_cols):
            x = center_x + (col * 2 * cell_radius) - (num_cols - 1) * cell_radius
            y = center_y + (row - rows // 2) * hex_height
            dist = math.hypot(mouse_x - x, mouse_y - y)
            if dist <= cell_radius:
                return row, col
    return None


# Initialize pygame and create the main screen
pygame.init()
screen = pygame.display.set_mode((500, 400))
pygame.display.set_caption("Partitions Game - Menu")

def draw_text(screen, text, pos, font_size=36, color=TEXT_COLOR):
    # Utility function to render text on screen
    font = pygame.font.Font(None, font_size)
    text_render = font.render(text, True, color)
    screen.blit(text_render, pos)

def show_start_screen():
    """
    Displays the initial screen with the game title and Start/Quit buttons.
    Waits for the user to click one of the buttons.
    """
    screen.fill(SCREEN_COLOR)
    font = pygame.font.Font(None, 50)

    title_text = font.render("Partitions", True, TEXT_COLOR)
    screen.blit(title_text, (175, 100))

    font = pygame.font.Font(None, 36)
    start_text = font.render("Start", True, TEXT_COLOR)
    quit_text = font.render("Quit", True, TEXT_COLOR)

    start_rect = pygame.Rect(200, 180, 100, 40)
    quit_rect = pygame.Rect(200, 250, 100, 40)

    pygame.draw.rect(screen, GRID_COLOR, start_rect, border_radius=10)
    pygame.draw.rect(screen, GRID_COLOR, quit_rect, border_radius=10)

    screen.blit(start_text, (start_rect.x + 25, start_rect.y + 5))
    screen.blit(quit_text, (quit_rect.x + 25, quit_rect.y + 5))

    pygame.display.flip()

    # Wait for user input
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(event.pos):
                    return  # Start the game
                elif quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    exit()

def get_user_choice(screen, options):
    """
    Displays a menu with a list of options.
    Returns the index of the option chosen by the user via mouse click.
    """
    screen.fill(SCREEN_COLOR)
    font = pygame.font.Font(None, 36)

    for i, option in enumerate(options):
        text_render = font.render(option, True, TEXT_COLOR)
        screen.blit(text_render, (MARGIN, MARGIN + i * 50))

    pygame.display.flip()

    # Loop to capture user choice
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for i in range(len(options)):
                    if MARGIN <= y <= MARGIN + (i + 1) * 50:
                        return i  

def main():
    pygame.init() # Initialize Pygame
    screen = pygame.display.set_mode((500, 400))  
    pygame.display.set_caption("Partitions Game - Menu") 
    show_start_screen() 
    screen.fill(SCREEN_COLOR) 

    board_input = ""
    moves_log = []
    # Ask user to input board size (odd number ≥ 5)
    selecting_size = True
    while selecting_size:
        screen.fill(SCREEN_COLOR)
        draw_text(screen, "Enter the board size (odd ≥ 5):", (MARGIN, 50), font_size=28)
        draw_text(screen, board_input, (MARGIN, 100), font_size=48)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if board_input.isdigit():
                        value = int(board_input)
                        if value >= 5 and value % 2 == 1:
                            board_size = value
                            selecting_size = False
                elif event.key == pygame.K_BACKSPACE:
                    board_input = board_input[:-1]
                elif event.unicode.isdigit():
                    board_input += event.unicode

    # Create game with selected board size
    game = PartitionsGame(board_size=board_size)

    # Game mode
    mode_choice = get_user_choice(screen, ["Choose game mode:", "Human vs Human", "Human vs Computer", "Computer vs Computer"])
    mode = mode_choice

    # Difficulty
    difficulty = None
    if mode in [2, 3]:  
        difficulty_choice = get_user_choice(screen, ["Choose difficulty:", "Easy", "Average", "Difficulty"])
        difficulty = {1: 'easy', 2: 'medium', 3: 'hard'}[difficulty_choice]

        # Algorithm
        algorithm_choice = get_user_choice(screen, ["Choose algorithm for AI:", "Minimax", "Monte Carlo Tree Search"])
        algorithm = 'minimax' if algorithm_choice == 1 else 'mcts'

    # Initialize AI players based on the game mode
    ai_white = AIPlayer(difficulty, algorithm) if mode == 3 or (mode == 2 and game.current_player == WHITE) else None
    ai_black = AIPlayer(difficulty, algorithm) if mode == 3 or (mode == 2 and game.current_player == BLACK) else None

    # Resize window to match board size
    screen_size = (MARGIN * 2 + board_size * CELL_SIZE + 200, MARGIN * 2 + board_size * CELL_SIZE + 200)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Partitions Game")
    
    # Gameplay setup
    moves = []
    start_time = time.time()
    hint_cell = None  
    clock = pygame.time.Clock()
    running = True
    
    # Main game loop
    while running:
        screen.fill(SCREEN_COLOR)
        menu_button_rect = draw_hexagonal_board(screen, game, hint_cell=hint_cell)
        
        font = pygame.font.Font(None, 30)

        # Show hint option if humans are playing
        if not (ai_white and ai_black):  
            hint_text = "Press 'H' for a hint"
            hint_render = font.render(hint_text, True, TEXT_COLOR)
            screen.blit(hint_render, (MARGIN, screen_size[1] - 70))

        font = pygame.font.Font(None, 36)
        if game.check_game_end():
            winner_text = f'Winner: {game.get_winner()}'
            text_render = font.render(winner_text, True, TEXT_COLOR)
            screen.blit(text_render, (MARGIN, screen_size[1] - 40))
        else:
            current_player_text = f"Player's turn: {'White' if game.current_player == WHITE else 'Black'}"
            text_render = font.render(current_player_text, True, TEXT_COLOR)
            screen.blit(text_render, (MARGIN, 10))

        # Show score for both players
        score = game.evaluate_score()
        white_score = max(score, 0)  
        black_score = max(-score, 0)  
        
        score_text = f"Black: {black_score}    White: {white_score}"
        score_render = font.render(score_text, True, TEXT_COLOR)
        screen.blit(score_render, (MARGIN, 50))  

        pygame.display.flip()
    
        if game.check_game_end():
            time.sleep(3)
            running = False
            break

        # AI turn 
        if (game.current_player == WHITE and ai_white) or (game.current_player == BLACK and ai_black):
            if not game.check_game_end():  
                time.sleep(1) 
                move_start = time.time()
                move = ai_white.best_move(game) if game.current_player == WHITE else ai_black.best_move(game)
                
                if move is not None:  
                    x, y = move
                    move_time = round(time.time() - move_start, 4)
                    game.make_move(x, y)
                    moves.append((x, y))
                    hint_cell = None  
                    # Update scores
                    score = game.evaluate_score()
                    white_score = max(score, 0)
                    black_score = max(-score, 0)
                    # Log move info
                    moves_log.append({
                        "play": len(moves),
                        "player": "White" if game.board[x][y] == WHITE else "Black",
                        "algorithm": ai_white.algorithm if game.board[x][y] == WHITE else ai_black.algorithm,
                        "position": f"({x},{y})",
                        "time (s)": move_time,
                        "score_white": white_score,
                        "score_black": black_score
                    })
                else :
                    time.sleep(3)
                    running = False
                    break

            screen.fill(SCREEN_COLOR)  
            draw_hexagonal_board(screen, game)  

            # Display AI move
            ai_move_text = f"Computer played: ({x}, {y})"
            font = pygame.font.Font(None, 36)
            text_render = font.render(ai_move_text, True, TEXT_COLOR)
            screen.blit(text_render, (MARGIN, screen_size[1] - 80))

            pygame.display.flip()  
            time.sleep(1)  

      
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and not game.check_game_end():
                if menu_button_rect.collidepoint(event.pos):
                    print("Exiting game...")
                    main()  
                    return  

                cell = get_cell_from_mouse(event.pos, game)
                print(f"Click detected at: {event.pos}, converted to cell: {cell}")
                if cell and game.is_valid_move(*cell):
                    print(f"Valid play in {cell}")
                    move_start = time.time()
                    game.make_move(*cell)
                    move_time = round(time.time() - move_start, 4)
                    moves.append(cell)
                    hint_cell = None  
                    # Update scores
                    score = game.evaluate_score()
                    white_score = max(score, 0)
                    black_score = max(-score, 0)
                    
                    moves_log.append({
                        "play": len(moves),
                        "player": "White" if game.board[cell[0]][cell[1]] == WHITE else "Black",
                        "algorithm": "Human",
                        "position": f"{cell}",
                        "time (s)": move_time,
                        "score_white": white_score,
                        "score_black": black_score
                    })

            elif event.type == pygame.KEYDOWN:
                # Show hint when 'H' is pressed 
                if event.key == pygame.K_h and not game.check_game_end() and not (ai_white and ai_black):
                    hint_cell = suggest_move(game)
                    print(f"Play tip: {hint_cell}")

    # Game finished
    end_time = time.time()
    time_taken = round(end_time - start_time, 2)
    screen.fill(SCREEN_COLOR)
    draw_hexagonal_board(screen, game)  
    
    pygame.display.flip()
    time.sleep(3)

    export_game_log_to_csv(moves_log, total_time=time_taken, winner=game.get_winner(), board_size=board_size)

    pygame.quit()

#  Save the full game log to a CSV file
def export_game_log_to_csv(moves_log, total_time, winner, board_size, filename="game_log.csv"):

    fieldnames = ["play", "player", "algorithm", "position", "time (s)", "score_white", "score_black"]

    with open(filename, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for move in moves_log:
            writer.writerow(move)

        writer.writerow({})
        writer.writerow({"play": "Board Size", "algorithm": board_size})
        writer.writerow({"play": "Total", "time (s)": total_time, "player": "Winner", "algorithm": "White" if winner == WHITE else "Black"})


if __name__ == '__main__':
    main()