import pygame
import random
import time

SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

COLORS = [RED, GREEN, BLUE, CYAN, MAGENTA, YELLOW, ORANGE]

TETRIS_SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1], [1, 1]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 0], [0, 1, 1]]
]

class Tetris:
    def __init__(self):
        self.board = [[0] * 10 for _ in range(20)]
        self.game_over = False
        self.current_piece = None
        self.current_position = None
        self.score = 0
        self.lines_cleared = 0
        self.fall_speed = 1000
        self.last_fall_time = time.time()

    def new_piece(self):
        shape = random.choice(TETRIS_SHAPES)
        color = random.choice(COLORS)
        self.current_piece = Piece(shape, color)
        self.current_position = [0, 4]
        if not self.valid_move((0, 0)):  # Vérifie si la pièce touche le haut du plateau (Game Over)
            self.game_over = True

    def valid_move(self, offset):
        for y, row in enumerate(self.current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = self.current_position[1] + x + offset[1]
                    new_y = self.current_position[0] + y + offset[0]
                    if new_x < 0 or new_x >= 10 or new_y >= 20 or self.board[new_y][new_x]:
                        return False
        return True

    def lock_piece(self):
        for y, row in enumerate(self.current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    self.board[self.current_position[0] + y][self.current_position[1] + x] = self.current_piece.color
        self.clear_lines()
        self.new_piece()

    def clear_lines(self):
        full_lines = [i for i, row in enumerate(self.board) if all(cell != 0 for cell in row)]
        for i in full_lines:
            self.board.pop(i)
            self.board.insert(0, [0] * 10)
        self.score += len(full_lines) * 100
        self.lines_cleared += len(full_lines)

    def rotate_piece(self):
        new_shape = [list(row) for row in zip(*self.current_piece.shape[::-1])]
        original_shape = self.current_piece.shape
        self.current_piece.shape = new_shape
        if not self.valid_move((0, 0)):
            self.current_piece.shape = original_shape

    def increase_fall_speed(self):
        if self.fall_speed > 100:
            self.fall_speed -= 10

    def update_fall(self):
        current_time = time.time()
        if current_time - self.last_fall_time >= self.fall_speed / 1000.0:
            self.last_fall_time = current_time
            if self.valid_move((1, 0)):
                self.current_position[0] += 1
            else:
                self.lock_piece()

class Piece:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color

    def get_width(self):
        return len(self.shape[0])

    def get_height(self):
        return len(self.shape)

def draw_board(screen, tetris):
    for y in range(20):
        for x in range(10):
            color = tetris.board[y][x] if tetris.board[y][x] != 0 else BLACK
            pygame.draw.rect(screen, color, pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(screen, WHITE, pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

def draw_piece(screen, tetris):
    for y, row in enumerate(tetris.current_piece.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, tetris.current_piece.color, pygame.Rect((tetris.current_position[1] + x) * BLOCK_SIZE,
                                                                              (tetris.current_position[0] + y) * BLOCK_SIZE,
                                                                              BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(screen, WHITE, pygame.Rect((tetris.current_position[1] + x) * BLOCK_SIZE,
                                                          (tetris.current_position[0] + y) * BLOCK_SIZE,
                                                          BLOCK_SIZE, BLOCK_SIZE), 1)

def draw_score(screen, tetris):
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {tetris.score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def draw_game_over(screen, tetris):
    font = pygame.font.Font(None, 48)
    game_over_text = font.render("GAME OVER", True, WHITE)
    score_text = font.render(f"Score: {tetris.score}", True, WHITE)
    screen.blit(game_over_text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 3))
    screen.blit(score_text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()

    tetris = Tetris()
    tetris.new_piece()

    while not tetris.game_over:
        screen.fill(BLACK)
        draw_board(screen, tetris)
        draw_piece(screen, tetris)
        draw_score(screen, tetris)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                tetris.game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if tetris.valid_move((0, -1)):
                        tetris.current_position[1] -= 1
                elif event.key == pygame.K_RIGHT:
                    if tetris.valid_move((0, 1)):
                        tetris.current_position[1] += 1
                elif event.key == pygame.K_DOWN:
                    if tetris.valid_move((1, 0)):
                        tetris.current_position[0] += 1
                    tetris.increase_fall_speed()
                elif event.key == pygame.K_UP:
                    tetris.rotate_piece()

        tetris.update_fall()

        pygame.display.flip()
        clock.tick(60)

    screen.fill(BLACK)
    draw_game_over(screen, tetris)
    pygame.display.flip()

    time.sleep(3)
    pygame.quit()

main()