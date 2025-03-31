import pygame
import random

# Initialize pygame
pygame.init()

# ------------------------------------------- #
# Game settings
SCREEN_WIDTH, SCREEN_HEIGHT = 300, 600
BLOCK_SIZE = 30
BOARD_WIDTH, BOARD_HEIGHT = 10, 20
FPS = 60
FALL_SPEED = 1.5 # falling speed
MOVE_DELAY = 0.1 # movement delay

# ------------------------------------------- #
# COLORS
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (128, 0, 128)
BLACK = (0, 0, 0)
COLOR_MAP = [CYAN, BLUE, ORANGE, YELLOW, GREEN, RED, PURPLE] # colors palette

# ------------------------------------------- #
# Piece shapes
TETRIS_SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
    [[1, 0, 0], [1, 1, 1]],  # L
    [[0, 0, 1], [1, 1, 1]],  # J
]


# ------------------------------------------- #
# ------------------------------------------- #
# Piece representation
class Piece:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.x = int(BOARD_WIDTH / 2) - 1
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

# Draw game board
def draw_board(screen, board, current_piece=None):
    # Already placed blocks
    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[y][x]: # if cell is not empty
                pygame.draw.rect(screen, board[y][x], 
                               (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(screen, WHITE, 
                           (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)
    
    # Draw falling piece
    if current_piece:
        for y, row in enumerate(current_piece.shape): # for each row in piece
            for x, cell in enumerate(row): # for each cell in row
                if cell:
                    # Draw cell
                    pygame.draw.rect(screen, current_piece.color, 
                                   ((current_piece.x + x) * BLOCK_SIZE, 
                                    (current_piece.y + y) * BLOCK_SIZE, 
                                    BLOCK_SIZE, BLOCK_SIZE))
                    pygame.draw.rect(screen, WHITE, 
                                   ((current_piece.x + x) * BLOCK_SIZE, 
                                    (current_piece.y + y) * BLOCK_SIZE, 
                                    BLOCK_SIZE, BLOCK_SIZE), 1)

# Check for collisions between pieces
def check_collision(board, piece):
    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell:
                if (x + piece.x < 0 or 
                    x + piece.x >= BOARD_WIDTH or 
                    y + piece.y >= BOARD_HEIGHT or 
                    (y + piece.y >= 0 and board[y + piece.y][x + piece.x])):
                    return True
    return False

def place_piece(board, piece):
    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell and y + piece.y >= 0:
                board[y + piece.y][x + piece.x] = piece.color

# Clear completed lines
def clear_lines(board):
    new_board = [row for row in board if any(cell == 0 for cell in row)]
    lines_cleared = BOARD_HEIGHT - len(new_board)
    return [[0] * BOARD_WIDTH for _ in range(lines_cleared)] + new_board, lines_cleared


# ------------------------------------------- #
# ------------------------------------------- #
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris by @valuthringer")
    clock = pygame.time.Clock()

    # INITIALIZE GAME BOARD
    board = [[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]
    current_piece = Piece(random.choice(TETRIS_SHAPES), random.choice(COLOR_MAP))
    game_over = False
    score = 0
    
    # TIMING VARIABLES
    fall_time = 0
    move_time = 0
    last_time = pygame.time.get_ticks()


    while not game_over:
        current_time = pygame.time.get_ticks()
        delta_time = (current_time - last_time) / 1000.0 # in seconds
        last_time = current_time
        
        # Background
        screen.fill(BLACK)
        
        # EVENT HANDLING
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP: # up arrow - rotate piece
                    current_piece.rotate()
                    if check_collision(board, current_piece):
                        # undo rotation if collision occurs
                        current_piece.rotate()
                        current_piece.rotate()
                        current_piece.rotate()
        
        # MOVEMENT KEY HANDLING
        keys = pygame.key.get_pressed()
        move_time += delta_time
        if move_time >= MOVE_DELAY:
            if keys[pygame.K_LEFT]: # left arrow - move left
                current_piece.x -= 1
                if check_collision(board, current_piece):
                    current_piece.x += 1
            if keys[pygame.K_RIGHT]: # right arrow - move right
                current_piece.x += 1
                if check_collision(board, current_piece):
                    current_piece.x -= 1
            if keys[pygame.K_DOWN]: # down arrow - speed up falling
                current_piece.y += 1
                if check_collision(board, current_piece):
                    current_piece.y -= 1
            move_time = 0
        
        # AUTOMATIC PIECE FALLING
        fall_time += delta_time
        if fall_time >= 1.0 / FALL_SPEED:
            current_piece.y += 1
            if check_collision(board, current_piece):
                current_piece.y -= 1
                place_piece(board, current_piece)
                board, lines_cleared = clear_lines(board)
                score += lines_cleared * 100
                current_piece = Piece(random.choice(TETRIS_SHAPES), random.choice(COLOR_MAP))
                if check_collision(board, current_piece):
                    game_over = True
            fall_time = 0
        
        # ------------------------------------ #
        # DRAW GAME
        draw_board(screen, board, current_piece)

        font = pygame.font.SysFont('Arial', 24)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        pygame.display.update()
        
        clock.tick(FPS)


    # -- GAME OVER -- #
    font = pygame.font.SysFont('Arial', 48)
    game_over_text = font.render("GAME OVER", True, WHITE)
    blink_time = 0
    blink_interval = 0.5
    blink_on = True
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        screen.fill(BLACK)
        draw_board(screen, board)
        if blink_time >= blink_interval:
            blink_on = not blink_on
            blink_time = 0
        if blink_on:
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
        pygame.display.update()
        blink_time += delta_time
        clock.tick(FPS)


if __name__ == "__main__":
    main()