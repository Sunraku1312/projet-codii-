import pygame 
import random

pygame.init()
  
largeur = 400
hauteur = 600
ecran = pygame.display.set_mode((largeur, hauteur)) 
pygame.display.set_caption("Flappy Bird")
 
noir = (0, 0, 255)
jaune = (255, 255, 0)
vert = (0, 255, 0)

def reset_game():
    global x_oiseau, y_oiseau, vitesse_oiseau, pipes, score
    x_oiseau = 50
    y_oiseau = hauteur // 2
    vitesse_oiseau = 0
    pipes = []
    score = 0

x_oiseau = 50
y_oiseau = hauteur // 2
vitesse_oiseau = 0

pipes = []
vitesse_pipes = 3
ecart_pipe = 150
score = 0

clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 30)

def dessiner():
    ecran.fill(noir)
    pygame.draw.rect(ecran, jaune, (x_oiseau, y_oiseau, 30, 30))
    for pipe in pipes:
        pygame.draw.rect(ecran, vert, pipe) 
    texte_score = font.render(str(score), True, (255, 255, 255))
    ecran.blit(texte_score, (largeur // 2 - texte_score.get_width() // 2, 20))
    pygame.display.update()

def mouvement_oiseau():
    global y_oiseau, vitesse_oiseau
    vitesse_oiseau += 0.5
    y_oiseau += vitesse_oiseau

def creer_pipes():
    hauteur_pipe = random.randint(100, 400)
    pipe_haut = pygame.Rect(largeur, 0, 50, hauteur_pipe)
    pipe_bas = pygame.Rect(largeur, hauteur_pipe + ecart_pipe, 50, hauteur - hauteur_pipe - ecart_pipe)
    pipes.append(pipe_haut)
    pipes.append(pipe_bas)

def deplacer_pipes():
    global score
    for pipe in pipes:
        pipe.x -= vitesse_pipes
        if pipe.x + pipe.width < 0:
            pipes.remove(pipe)
            if pipe.y < hauteur / 2:
                score += 1

def collision():
    if y_oiseau <= 0 or y_oiseau >= hauteur - 30:
        return True
    for pipe in pipes:
        if pygame.Rect(x_oiseau, y_oiseau, 30, 30).colliderect(pipe):
            return True
    return False

en_cours = True
while en_cours:
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            en_cours = False 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_z or event.key == pygame.K_SPACE or event.key == pygame.K_w:
                vitesse_oiseau = -10

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LSHIFT] and keys[pygame.K_l] :
        pygame.quit()
        import launcharles as launcharles

    mouvement_oiseau()
    deplacer_pipes()

    if len(pipes) == 0 or pipes[-1].x < largeur - 200:
        creer_pipes()

    dessiner()

    if collision():
        reset_game()

pygame.quit()
