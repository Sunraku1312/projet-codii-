import pygame
import time

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sunraku Studio")

BEIGE = (245, 245, 220)
LIGHT_BLUE = (173, 216, 230)

font = pygame.font.SysFont("BebasNeue.ttf", 80)

text = "Sunraku Studio"

def animate_text():
    screen.fill(BEIGE)
    for i in range(1, len(text) + 1):
        screen.fill(BEIGE)
        rendered_text = font.render(text[:i], True, LIGHT_BLUE)
        text_rect = rendered_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(rendered_text, text_rect)
        pygame.display.flip()
        pygame.time.delay(100)
    pygame.time.delay(500)

def fade_out():
    for alpha in range(0, 255, 5):
        screen.fill(BEIGE)
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(alpha)
        screen.blit(overlay, (0, 0))
        pygame.display.flip()
        pygame.time.delay(10)

def main():
    running = True
    animate_text()
    fade_out()
    pygame.time.delay(1000)
    pygame.quit()

if __name__ == "__main__":
    main()

import launcharles