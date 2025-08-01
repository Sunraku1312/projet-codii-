import pygame
import sys
import time
import random
import json

pygame.init()

VS_CODE_THEME = {
    "background": (38, 50, 56),
    "button": (72, 84, 96),
    "text": (255, 255, 255)
}

DARK_THEME = {
    "background": (18, 18, 18),
    "button": (33, 33, 33),
    "text": (255, 255, 255)
}

LIGHT_THEME = {
    "background": (200, 200, 200),
    "button": (200, 200, 200),
    "text": (0, 0, 0)
}

themes = [VS_CODE_THEME, DARK_THEME, LIGHT_THEME]
current_theme_index = 0
current_theme = themes[current_theme_index]

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Clickeur")

font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 28)

click_count = 0
autoclicker_price = 50
autoclicker_count = 0
click_boost_price = 100
click_boost_count = 0

last_autoclick_time = 0
autoclick_interval = 1.0

last_click_time = time.time()
clicks_this_second = 0
cps = 0
last_cps_update_time = time.time()

click_animation_active = False
click_animation_time = 0
click_animation_position = (0, 0)

purchase_particles = []

def draw_button(text, x, y, width, height, color, text_color=(255, 255, 255), hover_color=None):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if x <= mouse_x <= x + width and y <= mouse_y <= y + height:
        pygame.draw.rect(screen, (0,0,160), (x, y, width, height), border_radius=10)
    else:
        pygame.draw.rect(screen, color, (x, y, width, height), border_radius=10)
    label = font.render(text, True, text_color)
    text_rect = label.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(label, text_rect)


def draw_text(text, x, y, font_size=36, color=(255, 255, 255)):
    label = font.render(text, True, color)
    text_rect = label.get_rect(center=(x, y))
    screen.blit(label, text_rect)

def autoclick():
    global click_count, last_autoclick_time, autoclicker_count
    if autoclicker_count > 0:
        current_time = time.time()
        interval = 1.0
        if current_time - last_autoclick_time >= interval:
            click_count += 2 ** (autoclicker_count - 1)
            last_autoclick_time = current_time

def click():
    global click_count, click_boost_count, click_animation_active, click_animation_time, click_animation_position
    click_count += (1 + click_boost_count)

    click_animation_active = True
    click_animation_time = time.time()
    click_animation_position = pygame.mouse.get_pos()

    global last_click_time, clicks_this_second
    clicks_this_second += 1
    last_click_time = time.time()

def purchase_animation(position):
    global purchase_particles
    for _ in range(30):
        particle = {
            "position": [position[0], position[1]],
            "velocity": [random.uniform(-3, 3), random.uniform(-3, 3)],
            "color": current_theme["button"],
            "size": random.randint(2, 5),
            "lifespan": random.uniform(0.5, 1.0)
        }
        purchase_particles.append(particle)

def draw_click_animation():
    global click_animation_active, click_animation_time, click_animation_position
    if click_animation_active:
        current_time = time.time()
        time_elapsed = current_time - click_animation_time
        if time_elapsed < 0.5:
            radius = 20 + 80 * time_elapsed
            pygame.draw.circle(screen, current_theme["text"], click_animation_position, int(radius), 2)
        else:
            click_animation_active = False

def draw_purchase_particles():
    global purchase_particles
    for particle in purchase_particles[:]:
        particle["position"][0] += particle["velocity"][0]
        particle["position"][1] += particle["velocity"][1]
        particle["lifespan"] -= 0.05

        pygame.draw.circle(screen, (0,255,0), (int(particle["position"][0]), int(particle["position"][1])), particle["size"])

        if particle["lifespan"] <= 0:
            purchase_particles.remove(particle)

def draw_quit_button():
    button_width = 150
    button_height = 50
    button_x = WIDTH - button_width - 20
    button_y = HEIGHT - button_height - 20
    draw_button("Quitter", button_x, button_y, button_width, button_height, current_theme["button"])

    return button_x, button_y, button_width, button_height

def draw_theme_button():
    button_width = 190
    button_height = 50
    button_x = WIDTH - button_width - 5
    button_y = HEIGHT - button_height - 80
    draw_button("Changer Thème", button_x, button_y, button_width, button_height, current_theme["button"])

    return button_x, button_y, button_width, button_height

def draw_save_button():
    button_width = 150
    button_height = 50
    button_x = WIDTH - button_width - 20
    button_y = 20
    draw_button("Sauvegarder", button_x, button_y, button_width, button_height, current_theme["button"])

    return button_x, button_y, button_width, button_height

def draw_reset_button():
    button_width = 150
    button_height = 50
    button_x = WIDTH - button_width - 20
    button_y = 80
    draw_button("Réinitialiser", button_x, button_y, button_width, button_height, current_theme["button"])

    return button_x, button_y, button_width, button_height

def save_game():
    game_data = {
        "click_count": click_count,
        "autoclicker_count": autoclicker_count,
        "click_boost_count": click_boost_count,
        "autoclicker_price": autoclicker_price,
        "click_boost_price": click_boost_price
    }
    with open("game_save.json", "w") as save_file:
        json.dump(game_data, save_file)

def load_game():
    global click_count, autoclicker_count, click_boost_count, autoclicker_price, click_boost_price
    try:
        with open("game_save.json", "r") as save_file:
            game_data = json.load(save_file)
            click_count = game_data["click_count"]
            autoclicker_count = game_data["autoclicker_count"]
            click_boost_count = game_data["click_boost_count"]
            autoclicker_price = game_data["autoclicker_price"]
            click_boost_price = game_data["click_boost_price"]
    except FileNotFoundError:
        pass

def reset_game():
    global click_count, autoclicker_count, click_boost_count, autoclicker_price, click_boost_price
    click_count = 0
    autoclicker_count = 0
    click_boost_count = 0
    autoclicker_price = 50
    click_boost_price = 100
    save_game()

def update_cps():
    global clicks_this_second, cps, last_cps_update_time
    current_time = time.time()
    if current_time - last_cps_update_time >= 1.0:
        cps = clicks_this_second
        clicks_this_second = 0
        last_cps_update_time = current_time

def main():
    global click_count, autoclicker_price, autoclicker_count, click_boost_price, click_boost_count, current_theme, current_theme_index

    running = True
    clock = pygame.time.Clock()
    load_game()

    while running:
        screen.fill(current_theme["background"])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = event.pos

                    quit_button_x, quit_button_y, quit_button_width, quit_button_height = draw_quit_button()
                    if (quit_button_x <= mouse_x <= quit_button_x + quit_button_width and
                        quit_button_y <= mouse_y <= quit_button_y + quit_button_height):
                        running = False

                    theme_button_x, theme_button_y, theme_button_width, theme_button_height = draw_theme_button()
                    if (theme_button_x <= mouse_x <= theme_button_x + theme_button_width and
                        theme_button_y <= mouse_y <= theme_button_y + theme_button_height):
                        current_theme_index = (current_theme_index + 1) % len(themes)
                        current_theme = themes[current_theme_index]

                    save_button_x, save_button_y, save_button_width, save_button_height = draw_save_button()
                    if (save_button_x <= mouse_x <= save_button_x + save_button_width and
                        save_button_y <= mouse_y <= save_button_y + save_button_height):
                        save_game()
                        purchase_animation((mouse_x, mouse_y))

                    reset_button_x, reset_button_y, reset_button_width, reset_button_height = draw_reset_button()
                    if (reset_button_x <= mouse_x <= reset_button_x + reset_button_width and
                        reset_button_y <= mouse_y <= reset_button_y + reset_button_height):
                        reset_game()

                    elif 50 <= mouse_x <= 250 and 500 <= mouse_y <= 550:
                        click()
                    elif 300 <= mouse_x <= 500 and 250 <= mouse_y <= 300 and click_count >= autoclicker_price:
                        click_count -= autoclicker_price
                        autoclicker_count += 1
                        autoclicker_price = int(autoclicker_price * 2.3)
                        purchase_animation((mouse_x, mouse_y))
                    elif 300 <= mouse_x <= 500 and 350 <= mouse_y <= 400 and click_count >= click_boost_price:
                        click_count -= click_boost_price
                        click_boost_count += 1
                        click_boost_price = int(click_boost_price * 2.3)
                        purchase_animation((mouse_x, mouse_y))

        draw_save_button()
        draw_quit_button()
        draw_reset_button()
        draw_theme_button()

        draw_button("Clicker!", 50, 500, 200, 50, current_theme["button"])
        draw_button(f"Auto-Clicker (Prix: {autoclicker_price})", 200, 250, 400, 50, current_theme["button"])
        draw_button(f"Boost Clics (Prix: {click_boost_price})", 200, 350, 400, 50, current_theme["button"])

        draw_text(f"Nombre de clics: {click_count}", WIDTH // 2, 100, 48, current_theme["text"])
        draw_text(f"Auto-Clickers: {autoclicker_count}", WIDTH // 2, 150, 36, current_theme["text"])
        draw_text(f"Boost de clics: {click_boost_count}", WIDTH // 2, 200, 36, current_theme["text"])

        draw_text(f"CPS: {cps}", 100, 30, 36, current_theme["text"])

        autoclick()
        update_cps()

        draw_click_animation()
        draw_purchase_particles()

        pygame.display.update()

        clock.tick(60)

    pygame.quit()
    sys.exit()


main()