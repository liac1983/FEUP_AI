import pygame
import numpy as np

# Configurações do jogo
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 5  # Tamanho do tabuleiro
CELL_SIZE = WIDTH // GRID_SIZE
COLORS = [(255, 0, 0), (0, 0, 255), (255, 255, 0)]  # Vermelho, Azul, Amarelo

def next_color(color_index):
    return (color_index + 1) % len(COLORS)

def draw_board(screen, board, cursor_pos):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            pygame.draw.rect(screen, COLORS[board[row, col]],
                             (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, (0, 0, 0), (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 2)
    
    # Destacar cursor
    cursor_x, cursor_y = cursor_pos
    pygame.draw.rect(screen, (0, 255, 0), (cursor_x * CELL_SIZE, cursor_y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Jogo Amado")
    
    # Tabuleiro inicial aleatório
    board = np.random.randint(0, len(COLORS), (GRID_SIZE, GRID_SIZE))
    cursor_pos = [0, 0]  # Posição inicial do cursor
    
    running = True
    while running:
        screen.fill((255, 255, 255))
        draw_board(screen, board, cursor_pos)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    cursor_pos[1] = max(0, cursor_pos[1] - 1)
                elif event.key == pygame.K_DOWN:
                    cursor_pos[1] = min(GRID_SIZE - 1, cursor_pos[1] + 1)
                elif event.key == pygame.K_LEFT:
                    cursor_pos[0] = max(0, cursor_pos[0] - 1)
                elif event.key == pygame.K_RIGHT:
                    cursor_pos[0] = min(GRID_SIZE - 1, cursor_pos[0] + 1)
                elif event.key == pygame.K_SPACE:
                    x, y = cursor_pos
                    board[y, x] = next_color(board[y, x])  # Mudar cor da peça atual
    
    pygame.quit()

if __name__ == "__main__":
    main()


