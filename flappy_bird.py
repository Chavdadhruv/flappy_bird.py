import pygame
import random

# Initialize the Pygame library
pygame.init()

# Set up display
width, height = 400, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flappy Bird")

# Load and resize images
background = pygame.image.load('Background.png')
bird = pygame.image.load('Bird.png')
bird = pygame.transform.scale(bird, (50, 30))  # Resize bird image
pipe = pygame.image.load('Pipe.png')
pipe = pygame.transform.scale(pipe, (80, 500))  # Resize pipe image

# Game variables
gravity = 0.5
pipe_gap = 150  # Gap between top and bottom pipes
pipe_velocity = -4
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

def display_text(text, font, color, x, y):
    screen_text = font.render(text, True, color)
    window.blit(screen_text, [x, y])

def game_loop():
    bird_x = 50
    bird_y = 300
    bird_y_change = 0
    bird_width, bird_height = bird.get_width(), bird.get_height()
    
    pipe_width = pipe.get_width()
    pipe_height = pipe.get_height()
    pipe_x = width
    pipe_top = pipe_height - pipe_gap - random.randint(0, 100)
    pipe_bottom = pipe_top + pipe_gap
    score = 0
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_y_change = -10

        bird_y_change += gravity
        bird_y += bird_y_change

        pipe_x += pipe_velocity

        # Pipe reset
        if pipe_x < -pipe_width:
            pipe_x = width
            pipe_top = pipe_height - pipe_gap - random.randint(0, 100)
            pipe_bottom = pipe_top + pipe_gap
            score += 1

        # Bird boundaries
        if bird_y < 0 or bird_y + bird_height > height:
            show_game_over_menu(score)
            return

        # Collision detection
        bird_rect = pygame.Rect(bird_x, bird_y, bird_width, bird_height)
        top_pipe_rect = pygame.Rect(pipe_x, 0, pipe_width, pipe_top)
        bottom_pipe_rect = pygame.Rect(pipe_x, pipe_bottom, pipe_width, height - pipe_bottom)

        if bird_rect.colliderect(top_pipe_rect) or bird_rect.colliderect(bottom_pipe_rect):
            show_game_over_menu(score)
            return

        # Drawing
        window.blit(background, (0, 0))
        window.blit(bird, (bird_x, bird_y))
        window.blit(pipe, (pipe_x, pipe_top - pipe_height))
        window.blit(pipe, (pipe_x, pipe_bottom))
        display_text(f'Score: {score}', font, (255, 255, 255), 10, 10)

        pygame.display.update()
        clock.tick(30)

def show_game_over_menu(score):
    while True:
        window.blit(background, (0, 0))
        display_text(f'Game Over! Score: {score}', font, (255, 255, 255), width // 4, height // 3)
        display_text('Press C to Continue or Q to Quit', font, (255, 255, 255), width // 4, height // 2)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()
                if event.key == pygame.K_c:
                    return

# Run the game loop
while True:
    game_loop()
