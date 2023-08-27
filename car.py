import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (120, 120, 120)
DARK_GRAY = (60, 60, 60)
GREEN = (0, 255, 0)

# Create the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Simulation")

# Road properties
road_width = WIDTH * 2
road_y = 0
road_x = 0

# Car properties
car_x = WIDTH // 2
car_y = HEIGHT - 100
car_speed = 0.0
car_angle = 0.0
car_acceleration = 0.1
car_brake = 0.8
car_drag = 0.02
car_max_speed = 5.0
car_turn_angle = 0.05
car_max_angle = 15.0

# Tree
tree_radius = 50
tree_list = []

# Has collided
has_collided = False

# Font setup
font = pygame.font.Font(None, 36)

# Generate road pattern
road_pattern_white = [random.randint(0, road_width) for _ in range(HEIGHT * 2)]
road_pattern_grey = [random.randint(0, road_width) for _ in range(HEIGHT * 2)]

# Game loop
clock = pygame.time.Clock()
running = True
while running:
    # Clear the screen
    screen.fill(GRAY)


    if has_collided:
        # show game over
        game_over_text = font.render(f"GAME OVER", True, BLACK)
        screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 100))
        car_speed = 0

    tree_random_spawn = random.randint(0, 100)
    if tree_random_spawn > 97 and car_speed > 5:
        tree_list.append([random.randint(0, WIDTH), 0])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not has_collided:
      keys = pygame.key.get_pressed()
      if keys[pygame.K_LEFT]:
          car_angle += car_turn_angle
          car_angle = min(car_max_angle, car_angle)
      if keys[pygame.K_RIGHT]:
          car_angle -= car_turn_angle
          car_angle = max(-car_max_angle, car_angle)
      if keys[pygame.K_UP]:
          car_speed += car_acceleration
      if keys[pygame.K_DOWN]:
          car_speed -= car_brake
    car_speed = max(0, car_speed - car_drag)  # Apply drag

    car_x += car_speed * math.cos(math.radians(car_angle) + math.radians(90))

    # Update road position
    # road_x += car_speed * math.sin(math.radians(car_angle) + math.radians(90))
    if car_speed > 5:
        n = round(car_speed / 5)
        road_pattern_white = road_pattern_white[-n:] + road_pattern_white[:-n]
        road_pattern_grey = road_pattern_grey[-n:] + road_pattern_grey[:-n]

        # Update tree position
        for tree in tree_list:
            tree[1] += n
            if tree[1] > HEIGHT:
                tree_list.remove(tree)


    # Draw road
    for y in range(HEIGHT):
        pygame.draw.rect(screen, WHITE, (road_x + road_pattern_white[y], y, 1, 1))
        pygame.draw.rect(screen, DARK_GRAY, (road_x + road_pattern_grey[y], y, 1, 1))

    # Draw the car
    car_rect = pygame.Rect(car_x, car_y, 20, 40)
    pygame.draw.rect(screen, RED, car_rect)
    pygame.draw.line(screen, BLACK, (car_x + 10, car_y), (car_x + 10 + 20 * math.cos(math.radians(car_angle) + math.radians(90)),
                                                       car_y - 20 * math.sin(math.radians(car_angle) + math.radians(90))), 2)
    
    # Draw the trees
    for tree in tree_list:
        pygame.draw.circle(screen, GREEN, (tree[0], tree[1]), tree_radius)

    # Check for collision
    for tree in tree_list:
        tree_rect = pygame.Rect(tree[0] - tree_radius, tree[1] - tree_radius, tree_radius * 2, tree_radius * 2)
        if car_rect.colliderect(tree_rect):
            has_collided = True

    # Render and draw text
    speed_text = font.render(f"Speed: {car_speed:.2f}", True, BLACK)
    angle_text = font.render(f"Angle: {car_angle:.2f}", True, BLACK)
    screen.blit(speed_text, (10, 10))
    screen.blit(angle_text, (10, 50))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
