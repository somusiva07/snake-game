import pygame
import random
from enum import Enum
from collections import deque

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
FPS = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Direction Enum
class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class Snake:
    def __init__(self):
        # Start in the middle of the grid
        start_x = GRID_WIDTH // 2
        start_y = GRID_HEIGHT // 2
        self.body = deque([(start_x, start_y)])
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT
        self.grow_pending = False
    
    def update(self):
        # Update direction
        self.direction = self.next_direction
        
        # Get head position
        head_x, head_y = self.body[0]
        
        # Calculate new head position
        dx, dy = self.direction.value
        new_x = (head_x + dx) % GRID_WIDTH
        new_y = (head_y + dy) % GRID_HEIGHT
        
        # Add new head
        self.body.appendleft((new_x, new_y))
        
        # Remove tail only if not growing
        if not self.grow_pending:
            self.body.pop()
        else:
            self.grow_pending = False
    
    def eat_food(self):
        # Mark that snake should grow on next update
        self.grow_pending = True
    
    def check_collision(self):
        head = self.body[0]
        # Check if head collides with body
        return head in list(self.body)[1:]
    
    def draw(self, screen):
        for i, (x, y) in enumerate(self.body):
            color = GREEN if i == 0 else YELLOW  # Head is green, body is yellow
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)

class Food:
    def __init__(self):
        self.spawn()
    
    def spawn(self):
        self.x = random.randint(0, GRID_WIDTH - 1)
        self.y = random.randint(0, GRID_HEIGHT - 1)
    
    def draw(self, screen):
        rect = pygame.Rect(self.x * GRID_SIZE, self.y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, RED, rect)
        pygame.draw.rect(screen, BLACK, rect, 1)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.reset_game()
    
    def reset_game(self):
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.game_over = False
    
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.snake.direction != Direction.DOWN:
                    self.snake.next_direction = Direction.UP
                elif event.key == pygame.K_DOWN and self.snake.direction != Direction.UP:
                    self.snake.next_direction = Direction.DOWN
                elif event.key == pygame.K_LEFT and self.snake.direction != Direction.RIGHT:
                    self.snake.next_direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT and self.snake.direction != Direction.LEFT:
                    self.snake.next_direction = Direction.RIGHT
                elif event.key == pygame.K_SPACE and self.game_over:
                    self.reset_game()
        return True
    
    def update(self):
        if not self.game_over:
            self.snake.update()
            
            # Check if snake ate food
            if self.snake.body[0] == (self.food.x, self.food.y):
                self.score += 10
                # Mark snake to grow
                self.snake.eat_food()
                # Spawn new food
                self.food.spawn()
            
            # Check collision
            if self.snake.check_collision():
                self.game_over = True
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw grid
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, (40, 40, 40), (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, (40, 40, 40), (0, y), (SCREEN_WIDTH, y))
        
        # Draw game objects
        self.snake.draw(self.screen)
        self.food.draw(self.screen)
        
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Draw game over message
        if self.game_over:
            game_over_text = self.font.render("GAME OVER! Press SPACE to restart", True, RED)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(game_over_text, text_rect)
        
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            running = self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
