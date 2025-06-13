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
GREEN = (0, 255, 0)
# Game Variables
speed = 7
speed_timer = 0  # Tracks frames to increment speed

# Player Settings
player_size = 75
player_x = WIDTH // 2
player_y = HEIGHT - player_size - 30
player_velocity = 10
player_image = pygame.image.load("oofyjake.png").convert_alpha()
player_image = pygame.transform.scale(player_image, (player_size, player_size))
# Invincibility (no collision) timer
invincible = False
invincibility_timer = 0
invincibility_duration = 30  # Half a second at 60 FPS
invincibility_cooldown = 0  # Time until spacebar can be used again
cooldown_duration = 240     # 4 seconds at 60 FPS
# Obstacles
obstacle_width = 125
obstacle_height = 50
obstacles = []
spawn_timer = 0  # Time between obstacle spawns
notcool_timer = 0 # time before the obstacle spawns double
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
    if keys[pygame.K_SPACE] and not invincible and invincibility_cooldown <= 0:
        invincible = True
        invincibility_timer = invincibility_duration
        invincibility_cooldown = cooldown_duration


    # Spawn Obstacles Periodically
    notcool_timer += 1
    spawn_timer += 1
    if spawn_timer > 50:
        spawn_obstacle()
        if notcool_timer > 600:
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
        score = score*1.2
        if speed != 25:
            speed += 0.5    
            print(f"Speed increased to: {speed:.1f}")

    # Collision Detection
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    if not invincible:
     pygame.draw.rect(screen, BLUE, player_rect)
     for obstacle in obstacles:
        if player_rect.colliderect(obstacle):
            score = int(score)
            print(f"Game Over! You ended with a score of {score}")
            pygame.quit()
            sys.exit()

    if invincible:
        pygame.draw.rect(screen, GREEN, player_rect)
        invincibility_timer -= 1
        if invincibility_timer <= 0:
            invincible = False
    if invincibility_cooldown > 0:
       invincibility_cooldown -= 1

    # Draw Player  
    screen.blit(player_image, (player_x, player_y))

    # Draw Obstacles
    for obstacle in obstacles:
        pygame.draw.rect(screen, RED, obstacle)

    # Update Display and Tick
    pygame.display.update()
    clock.tick(FPS)
