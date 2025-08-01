import pygame
import sys
import random
import math

pygame.init()

WHITE = (255, 255, 255)
BLACK = (30, 30, 30)
DARK_GRAY = (50, 50, 50)
BLUE = (0, 122, 204)
DARK_BLUE = (32, 32, 32)
GREEN = (72, 156, 81)
LIGHT_GREEN = (144, 238, 144)
PURPLE = (100, 0, 150)

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jeu de Plateforme")

clock = pygame.time.Clock()

player_width, player_height = 50, 50
player_speed = 5
player_jump = 15
player_velocity_y = 0
gravity = 0.8

platforms = []
particles = []

level_data = [
    {
        "platforms": [(100, 500, 200, 20), (300, 400, 150, 20), (500, 300, 150, 20), (700, 200, 100, 20)],
        "start": (100, HEIGHT - player_height - 100),
        "end": (750, 100)
    },
    {
        "platforms": [(100, 500, 150, 20), (250,400,20,120), (250, 400, 150, 20), (400,300,20,120), (400, 300, 200, 20), (600,150,20,170), (600, 150, 150, 20)],
        "start": (100, HEIGHT - player_height - 100),
        "end": (350, 500)
    },
    {
        "platforms": [(100, 500, 200, 20), (300, 400, 100, 20), (500, 300, 150, 20), (650, 150, 100, 20)],
        "start": (100, HEIGHT - player_height - 100),
        "end": (700, 50)
    },
    {
        "platforms": [(0, 100, 700, 20), (0, 300, 700, 20), (500, 400, 250, 20), (100, 200, 700, 20)],
        "start": (100, 0),
        "end": (650, 500)
    },
    {
        "platforms": [(800-100-50, 500, 100, 20), (800-200-250, 400, 200, 20), (800-150-450, 300, 150, 20), (800-100-600, 200, 100, 20)],
        "start": (700, HEIGHT - player_height - 100),
        "end": (800-650, HEIGHT - 500)
    },
    {
        "platforms": [(100, 500, 150, 20), (300, 400, 200, 20), (500, 300, 100, 20), (650, 150, 100, 20)],
        "start": (100, HEIGHT - player_height - 100),
        "end": (650, 150)
    },
    {
        "platforms": [(350, 500, 100, 20), (350, 400, 100, 20), (350, 300, 100, 20), (350, 200, 100, 20)],
        "start": (100, HEIGHT - player_height - 100),
        "end": (400, 50)
    },
    {
        "platforms": [(50, 700, 700, 700), (250, 400, 200, 20), (450, 300, 150, 20), (600, 150, 200, 20)],
        "start": (700, HEIGHT - player_height - 100),
        "end": (50, 150)
    }
]

current_level = 0
level = level_data[current_level]

start_time = pygame.time.get_ticks()
game_over = False

def reset_level():
    global player, player_velocity_y, on_ground, platforms, particles
    player = pygame.Rect(level["start"][0], level["start"][1], player_width, player_height)
    player_velocity_y = 0
    on_ground = False
    platforms = [pygame.Rect(x, y, w, h) for x, y, w, h in level["platforms"]]
    ground = pygame.Rect(0, HEIGHT - 50, WIDTH, 50)
    platforms.append(ground)
    particles = []  
    generate_particles_around_end()  

def draw_window():
    screen.fill(BLACK)
    pygame.draw.rect(screen, BLUE, pygame.Rect(0, HEIGHT - 50, WIDTH, 50))
    for plat in platforms:
        pygame.draw.rect(screen, BLUE, plat)
    pygame.draw.rect(screen, GREEN, player)

    draw_end_circle()
    draw_particles()

    elapsed_time = pygame.time.get_ticks() - start_time
    seconds = elapsed_time // 1000
    milliseconds = elapsed_time % 1000
    centiseconds = milliseconds // 10

    font = pygame.font.SysFont("Arial", 30)
    timer_text = font.render(f"Temps : {seconds}.{centiseconds:02d}s", True, WHITE)
    screen.blit(timer_text, (10, 10))

    level_text = font.render(f"Niveau: {current_level + 1}", True, WHITE)
    screen.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, 10))

    pygame.display.update()

def draw_end_circle():
    end_circle_pos = level["end"]
    end_circle_radius = 40
    pygame.draw.circle(screen, PURPLE, end_circle_pos, end_circle_radius)

def draw_particles():
    for particle in particles:
        pygame.draw.circle(screen, particle["color"], particle["pos"], particle["radius"])

def check_collisions():
    global player_velocity_y, on_ground
    on_ground = False
    for plat in platforms:
        if player.colliderect(plat) and player_velocity_y >= 0:
            on_ground = True
            player_velocity_y = 0
            player.y = plat.y - player_height

        if player.colliderect(plat) and player_velocity_y < 0:
            player_velocity_y = 0
            player.y = plat.y + plat.height

        if player.colliderect(plat):
            if player.right > plat.left and player.left < plat.left:
                player.x = plat.left - player.width
            elif player.left < plat.right and player.right > plat.right:
                player.x = plat.right
            player_velocity_y = 0

    if player.colliderect(pygame.Rect(0, HEIGHT - 50, WIDTH, 50)):
        on_ground = True
        player_velocity_y = 0
        player.y = HEIGHT - player_height - 50

def move_player(keys):
    global player_velocity_y
    speed = player_speed
    if keys[pygame.K_DOWN]:
        generate_particles_when_down()
        speed = player_speed * 3
    if keys[pygame.K_LEFT]:
        if player.left > 0:
            player.x -= speed
    if keys[pygame.K_RIGHT]:
        if player.right < WIDTH:
            player.x += speed
    if keys[pygame.K_UP] and on_ground or keys[pygame.K_SPACE] and on_ground:
        if not keys[pygame.K_DOWN]:
            player_velocity_y = -player_jump

def update_player():
    global player_velocity_y
    player_velocity_y += gravity
    player.y += player_velocity_y
    if player.y > HEIGHT:
        reset_level()

def generate_particles_when_down():
    for _ in range(5):
        particle_x = player.centerx + random.uniform(-25, 25)
        particle_y = player.bottom + random.uniform(0, 10)
        particle = {
            "pos": [particle_x, particle_y],
            "radius": random.randint(3, 5),
            "color": LIGHT_GREEN,
            "velocity": [random.uniform(-1, 1), random.uniform(-1, 1)],
            "created_at": pygame.time.get_ticks()
        }
        particles.append(particle)

def generate_particles_around_end():
    global particles
    end_circle_pos = level["end"]
    end_circle_radius = 40
    max_particles = 50

    for _ in range(2):
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(end_circle_radius * 0.5, end_circle_radius)
        particle_x = end_circle_pos[0] + distance * math.cos(angle)
        particle_y = end_circle_pos[1] + distance * math.sin(angle)
        particle = {
            "pos": [particle_x, particle_y],
            "radius": random.randint(3, 5),
            "color": DARK_GRAY,
            "velocity": [random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5)],
            "created_at": pygame.time.get_ticks()
        }
        particles.append(particle)

    for _ in range(10):
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(end_circle_radius * 0.5, end_circle_radius)
        particle_x = end_circle_pos[0] + distance * math.cos(angle)
        particle_y = end_circle_pos[1] + distance * math.sin(angle)
        particle = {
            "pos": [particle_x, particle_y],
            "radius": random.randint(3, 5),
            "color": BLACK,
            "velocity": [random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5)],
            "created_at": pygame.time.get_ticks()
        }
        particles.append(particle)

    if len(particles) > max_particles:
        particles = particles[:max_particles]

def update_particles():
    global particles
    current_time = pygame.time.get_ticks()
    for particle in particles[:]:
        if current_time - particle["created_at"] > 3000:
            particles.remove(particle)
        else:
            particle["pos"][0] += particle["velocity"][0]
            particle["pos"][1] += particle["velocity"][1]

        if particle["pos"][0] < 0 or particle["pos"][0] > WIDTH or particle["pos"][1] < 0 or particle["pos"][1] > HEIGHT:
            particles.remove(particle)

def check_level_end():
    end_circle_pos = level["end"]
    end_circle_radius = 40
    if player.colliderect(pygame.Rect(end_circle_pos[0] - end_circle_radius, end_circle_pos[1] - end_circle_radius, 2 * end_circle_radius, 2 * end_circle_radius)):
        return True
    return False

def next_level():
    global current_level, level
    current_level += 1
    if current_level < len(level_data):
        level = level_data[current_level]
        reset_level()
    else:
        global game_over
        game_over = True
        final_time = pygame.time.get_ticks() - start_time
        display_game_over(final_time)

def display_game_over(final_time):
    seconds = final_time // 1000
    milliseconds = final_time % 1000
    centiseconds = milliseconds // 10
    font = pygame.font.SysFont("Arial", 30)
    game_over_text = font.render(f"Jeu terminé! Temps : {seconds}.{centiseconds:02d}s", True, WHITE)
    restart_text = font.render("Appuyez sur ESPACE pour recommencer.", True, WHITE)
    
    screen.fill(BLACK)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2))
    pygame.display.update()

def reset_game():
    global current_level, game_over, start_time, level
    current_level = 0
    level = level_data[current_level]
    game_over = False
    start_time = pygame.time.get_ticks()
    reset_level()

reset_level()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_SPACE:
                reset_game()

    keys = pygame.key.get_pressed()

    if game_over:
        continue

    move_player(keys)
    update_player()
    check_collisions()

    update_particles()

    draw_window()

    if check_level_end():
        next_level()

    clock.tick(60)