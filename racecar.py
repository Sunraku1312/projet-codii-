from random import randint
import pygame
import time

pygame.init()

carcolors = (0, 0, 0)
BACKGROUND = (255, 255, 255)

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("jeudevoituretropcool !!!!!!!")
clock = pygame.time.Clock()

car_img = pygame.image.load("image/limagetropcool.png")
background_img = pygame.image.load("image/laroute.webp")

background_img = pygame.transform.scale(background_img, (WIDTH * 2, HEIGHT * 2)) 

def show_score(score):
    font = pygame.font.SysFont("Arial", 30)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10)) 

def game_loop():
    score = 0
    ssuivant = score + 5
    tcar = randint(30, 90)
    yc = 2000
    xc = 0.0
    speedcar = 4
    running = True
    x = (WIDTH * 0.45)
    y = (HEIGHT * 0.8)
    x_change = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_q] and x > 0 or keys[pygame.K_LEFT] and x > 0 or keys[pygame.K_a] and x > 0:
            x_change = -5
        elif keys[pygame.K_d] and x < WIDTH - 70 or keys[pygame.K_RIGHT] and x < WIDTH - 70 or keys[pygame.K_d] and x < WIDTH - 70:
            x_change = 5
        else:
            x_change = 0
        x += x_change

        if yc < y < yc + tcar:
            if x < xc < x + 70:
                running = False
                game_loop()
            elif x < xc + tcar < x + 70:
                running = False
                game_loop()
            elif x < xc + tcar / 2 < x + 70:
                running = False
                game_loop()

        if score == ssuivant:
            speedcar += 0.05

        screen.blit(background_img, (-200, 0))

        show_score(score - 1)

        pygame.draw.rect(screen, carcolors, (xc, yc, tcar, tcar))
        screen.blit(car_img, (x, y))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT] and keys[pygame.K_l] :
            pygame.quit()
            import launcharles as launcharles

        if yc < HEIGHT:
            yc += speedcar
        else:
            xc = x
            tcar = randint(30, 90)
            yc = 0 - tcar
            score += 1

        pygame.display.update()
        clock.tick(60)

game_loop()

pygame.quit()
