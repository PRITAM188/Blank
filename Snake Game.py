import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Game window dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game!")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (213, 50, 80)
BLUE = (50, 153, 213)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# Snake and game settings
block_size = 20
snake_speed = 15

# Fonts
font_score = pygame.font.SysFont("comicsansms", 30)
font_main = pygame.font.SysFont("bahnschrift", 25)
font_title = pygame.font.SysFont("comicsansms", 45)

# Clock
clock = pygame.time.Clock()

def draw_snake(snake_list):
    for segment in snake_list:
        pygame.draw.rect(screen, GREEN, [segment[0], segment[1], block_size, block_size], border_radius=5)

def show_score(score):
    value = font_score.render(f"Score: {score}", True, YELLOW)
    screen.blit(value, [10, 10])

def message(msg, color, y_offset=0, font_size=25):
    font = pygame.font.SysFont("bahnschrift", font_size)
    mesg = font.render(msg, True, color)
    rect = mesg.get_rect(center=(width // 2, height // 2 + y_offset))
    screen.blit(mesg, rect)

def intro_screen():
    fade = 0
    while True:
        screen.fill(BLACK)
        title = font_title.render("Welcome to Snake Game", True, (0, fade, 0))
        screen.blit(title, [width // 2 - title.get_width() // 2, height // 4])

        message("Press [SPACE] to Start", WHITE, 60)
        message("Press [Q] to Quit", WHITE, 100)

        pygame.display.update()
        fade = (fade + 2) % 255  # Simple fade animation

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
        clock.tick(30)

def game_over_screen(score):
    while True:
        screen.fill(BLACK)
        message("Game Over!", RED, -30, font_size=40)
        message(f"Final Score: {score}", YELLOW, 10, font_size=30)
        message("Press [R] to Restart or [Q] to Quit", WHITE, 60)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_loop()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

def game_loop():
    x = width // 2
    y = height // 2
    dx = 0
    dy = 0

    snake_list = []
    snake_length = 1

    food_x = round(random.randrange(0, width - block_size) / block_size) * block_size
    food_y = round(random.randrange(0, height - block_size) / block_size) * block_size

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and dx == 0:
                    dx = -block_size
                    dy = 0
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx = block_size
                    dy = 0
                elif event.key == pygame.K_UP and dy == 0:
                    dx = 0
                    dy = -block_size
                elif event.key == pygame.K_DOWN and dy == 0:
                    dx = 0
                    dy = block_size

        x += dx
        y += dy

        # Wall collision
        if x < 0 or x >= width or y < 0 or y >= height:
            game_over_screen(snake_length - 1)

        screen.fill(BLUE)

        # Draw food
        pygame.draw.ellipse(screen, WHITE, [food_x, food_y, block_size, block_size])

        # Snake update
        snake_head = [x, y]
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        # Self collision
        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_over_screen(snake_length - 1)

        # Eating food
        if x == food_x and y == food_y:
            snake_length += 1
            food_x = round(random.randrange(0, width - block_size) / block_size) * block_size
            food_y = round(random.randrange(0, height - block_size) / block_size) * block_size

        draw_snake(snake_list)
        show_score(snake_length - 1)
        pygame.display.update()
        clock.tick(snake_speed)

# --- Run the game ---
intro_screen()
game_loop()
