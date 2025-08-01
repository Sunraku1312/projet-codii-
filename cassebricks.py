import pygame
import random

pygame.init()

largeur_fenetre = 800
hauteur_fenetre = 600
screen = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
pygame.display.set_caption("Casse-briques Infini")

BLANC = (255, 255, 255)
ROUGE = (255, 0, 0)
BLEU = (0, 0, 255)
VERT = (0, 255, 0)
NOIR = (0, 0, 0)
ORANGE = (255, 165, 0)

raquette_largeur = 100
raquette_hauteur = 15
raquette_vitesse = 10

balle_radius = 10

raquette = pygame.Rect(largeur_fenetre // 2 - raquette_largeur // 2, hauteur_fenetre - raquette_hauteur - 10, raquette_largeur, raquette_hauteur)

briques = []
nb_briques_lignes = 5
nb_briques_colonnes = 8
brique_largeur = largeur_fenetre // nb_briques_colonnes - 10
brique_hauteur = 30

class Particle:
    def __init__(self, x, y, couleur, taille=5):
        self.x = x
        self.y = y
        self.couleur = couleur
        self.taille = taille
        self.vitesse_x = random.randint(-3, 3)
        self.vitesse_y = random.randint(-3, 3)
        self.duree = random.randint(20, 40)

    def update(self):
        self.x += self.vitesse_x
        self.y += self.vitesse_y
        self.duree -= 1

    def draw(self):
        pygame.draw.circle(screen, self.couleur, (self.x, self.y), self.taille)

def create_briques():
    briques.clear()
    for i in range(nb_briques_lignes):
        for j in range(nb_briques_colonnes):
            brique = pygame.Rect(j * (brique_largeur + 10) + 5, i * (brique_hauteur + 5) + 5, brique_largeur, brique_hauteur)
            briques.append(brique)

def draw_briques():
    for brique in briques:
        pygame.draw.rect(screen, BLEU, brique)

def game():
    balle_dx = random.choice([5, -5])  # Direction X aléatoire
    balle_dy = random.choice([5, -5])  # Direction Y aléatoire
    balle_x = largeur_fenetre // 2
    balle_y = hauteur_fenetre - 50

    raquette_dx = 0
    score = 0
    clock = pygame.time.Clock()

    create_briques()

    particules = []

    while True:
        screen.fill(NOIR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and raquette.left > 0:
            raquette_dx = -raquette_vitesse
        elif keys[pygame.K_RIGHT] and raquette.right < largeur_fenetre:
            raquette_dx = raquette_vitesse
        else:
            raquette_dx = 0

        raquette.x += raquette_dx

        balle_x += balle_dx
        balle_y += balle_dy

        if balle_x - balle_radius <= 0 or balle_x + balle_radius >= largeur_fenetre:
            balle_dx = -balle_dx

        if balle_y - balle_radius <= 0:
            balle_dy = -balle_dy

        if raquette.colliderect(pygame.Rect(balle_x - balle_radius, balle_y - balle_radius, balle_radius * 2, balle_radius * 2)):
            balle_dy = -balle_dy

        for brique in briques[:]:
            if brique.colliderect(pygame.Rect(balle_x - balle_radius, balle_y - balle_radius, balle_radius * 2, balle_radius * 2)):
                balle_dy = -balle_dy
                briques.remove(brique)
                score += 10

                for _ in range(20):
                    particules.append(Particle(brique.centerx, brique.centery, ORANGE))

                if len(briques) == 0:
                    create_briques()

        if balle_y > hauteur_fenetre:
            game()  # Relancer le jeu quand la balle tombe

        for p in particules[:]:
            p.update()
            if p.duree <= 0:
                particules.remove(p)

        pygame.draw.rect(screen, VERT, raquette)
        pygame.draw.circle(screen, ROUGE, (balle_x, balle_y), balle_radius)

        for p in particules:
            p.draw()

        draw_briques()

        font = pygame.font.SysFont('Arial', 24)
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        pygame.display.update()

        clock.tick(60)

game()

pygame.quit()
