import pygame
import random
import sys

# Initialize Pygame
pygame.init()
# Clock and Frame Rate
clock = pygame.time.Clock()
FPS = 60
# Screen Setup
WIDTH, HEIGHT = 500, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Subway Surfers Lite")
background_img = pygame.image.load("background.jpg").convert()
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
# Game Variables
speed = 7
speed_timer = 0  # Tracks frames to increment speed

# Player Settings
player_size = 75
player_x = WIDTH // 2
player_y = HEIGHT - player_size - 30
player_velocity = 10
# Invincibility (no collision) timer
invincible = False
invincibility_timer = 0
invincibility_duration = 30  # Half a second at 60 FPS
invincibility_cooldown = 0  # Time until spacebar can be used again
cooldown_duration = 240     # 4 seconds at 60 FPS
# Obstacles
obstacle_width = 150
obstacle_height = 80
obstacles = []
obstacle_left_img = pygame.image.load("ntrain.png").convert_alpha()
obstacle_middle_img = pygame.image.load("rtrain.png").convert_alpha()
obstacle_right_img = pygame.image.load("sirtrain.png").convert_alpha()

# Resize them to fit the lane
obstacle_left_img = pygame.transform.scale(obstacle_left_img, (obstacle_width, obstacle_height))
obstacle_middle_img = pygame.transform.scale(obstacle_middle_img, (obstacle_width, obstacle_height))
obstacle_right_img = pygame.transform.scale(obstacle_right_img, (obstacle_width, obstacle_height))
spawn_timer = 0  # Time between obstacle spawns
speed_timer = 0 # time before the obstacle spawns double
score = 1
class Obstacle:
    def __init__(self, x, y, image):
        self.rect = pygame.Rect(x, y, obstacle_width, obstacle_height)
        self.image = image

    def move(self, speed):
        self.rect.y += speed

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
def spawn_obstacle():
    lane_width = WIDTH // 3
    lanes = [0, 1, 2]  # Lane indices

    lane = random.choice(lanes)
    x_pos = lane * lane_width + (lane_width - obstacle_width) // 2

    # Assign image based on lane
    if lane == 0:
        image = obstacle_left_img
    elif lane == 1:
        image = obstacle_middle_img
    else:
        image = obstacle_right_img

    obstacles.append(Obstacle(x_pos, -obstacle_height, image))


# Main Game Loop
running = True
while running:
    screen.blit(background_img, (0, 0))

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
    spawn_timer += 1
    if spawn_timer > 50:
        spawn_obstacle()
        if speed_timer > 600:
            spawn_obstacle()
        spawn_timer = 0

    # Move Obstacles
    for obstacle in obstacles[:]:
        obstacle.move(speed)
        if obstacle.rect.y  > HEIGHT:
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
     player_image = pygame.image.load("oofyjake.png").convert_alpha()
     player_image = pygame.transform.scale(player_image, (player_size, player_size))
     for obstacle in obstacles:
         if player_rect.colliderect(obstacle.rect):
            score = int(score)
            print(f"Game Over! You ended with a score of {score}")
            pygame.quit()
            sys.exit()

    if invincible:
        player_image = pygame.image.load("invincibleboy.jpg").convert_alpha()
        player_image = pygame.transform.scale(player_image, (player_size, player_size))
        invincibility_timer -= 1
        if invincibility_timer <= 0:
            invincible = False
    if invincibility_cooldown > 0:
       invincibility_cooldown -= 1

    # Draw Player  
    screen.blit(player_image, (player_x, player_y))

    # Draw Obstacles
    for obstacle in obstacles:
       obstacle.draw(screen)

    # Update Display and Tick
    pygame.display.update()
    clock.tick(FPS)
