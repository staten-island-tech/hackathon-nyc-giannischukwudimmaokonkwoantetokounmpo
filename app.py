import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen Setup
WIDTH, HEIGHT = 500, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Subway Surfers Lite")

# Clock and Frame Rate
clock = pygame.time.Clock()
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 102, 204)
RED = (255, 0, 0)

# Game Variables
speed = 7
speed_timer = 0  # Tracks frames to increment speed

# Player Settings
player_size = 50
player_x = WIDTH // 2
player_y = HEIGHT - player_size - 30
player_velocity = 10

# Jump Mechanics
gravity = 1
jump_strength = 20
is_jumping = False
velocity_y = 0

# Obstacles
obstacle_width = 125
obstacle_height = 50
obstacles = []
spawn_timer = 0  # Time between obstacle spawns
score = 1
def spawn_obstacle():
    lane_width = WIDTH // 3
    lanes = [i * lane_width for i in range(3)]  # [0, 166, 332]
    x_pos = random.choice(lanes)
    obstacles.append(pygame.Rect(x_pos, -obstacle_height, obstacle_width, obstacle_height))
    x_pos += (lane_width - obstacle_width) // 2


# Main Game Loop
running = True
while running:
    screen.fill(WHITE)

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Input Handling
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_velocity
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
        player_x += player_velocity
    if keys[pygame.K_SPACE] and not is_jumping:
        is_jumping = True
        velocity_y = -jump_strength

    # Jump Physics
    if is_jumping:
        player_y += velocity_y
        velocity_y += gravity
        if player_y >= HEIGHT - player_size - 30:
            player_y = HEIGHT - player_size - 30
            is_jumping = False

    # Spawn Obstacles Periodically
    spawn_timer += 1
    if spawn_timer > 50:
        spawn_obstacle()
        spawn_timer = 0

    # Move Obstacles
    for obstacle in obstacles[:]:
        obstacle.y += speed
        if obstacle.y > HEIGHT:
            obstacles.remove(obstacle)

    # Speed Increases Over Time
    speed_timer += 1
    if speed_timer % 60 == 0:  # Every 1 second at 60 FPS
        speed += 0.5
        print(f"Speed increased to: {speed:.1f}")
        score = score*1.2

    # Collision Detection
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    for obstacle in obstacles:
        if player_rect.colliderect(obstacle):
            score = int(score)
            print(f"Game Over! You ended with a score of {score}")
            pygame.quit()
            sys.exit()

    # Draw Player
    pygame.draw.rect(screen, BLUE, player_rect)

    # Draw Obstacles
    for obstacle in obstacles:
        pygame.draw.rect(screen, RED, obstacle)

    # Update Display and Tick
    pygame.display.update()
    clock.tick(FPS)
