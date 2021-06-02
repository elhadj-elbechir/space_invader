import pygame
from random import randint
from pygame import mixer

# Debut du jeu
pygame.init()
charger = pygame.image
screen = pygame.display.set_mode((800, 600))
background1 = charger.load("assets/background1.jpg")  # Chargement du premier fond
background2 = charger.load("assets/background2.jpg")  # Chargement du second fond
bgY_change = 4  # Vitesse de defilement du fond
bgY1 = -599
bgY2 = -1797
# Titre et icone de la fenetre
pygame.display.set_caption("El Bechir El Hadj 1ere13")  # Titre
pygame.display.set_icon(pygame.image.load('assets/icone.png'))  # Icone

# Chargement des images du vaisseau et position de ses coordonnes initiales
frame_default = charger.load('assets/spaceship_straight.png')
frame_gauche = charger.load('assets/spaceship_left.png')
frame_droite = charger.load('assets/spaceship_right.png')
spaceship = [367, 450]  # Coordonnées x et y
spaceshipX_change = 0  # Variable utilisée pour le déplacement du vaisseau
spaceshipY_change = 0

# Chargement des images des ennemis et position de leur coordonnées initiales
ennemi1 = charger.load('assets/enemy1.png')
ennemi2 = charger.load('assets/enemy2.png')
ennemi3 = charger.load('assets/enemy3.png')
ennemi4 = charger.load('assets/enemy4.png')
ennemi5 = charger.load('assets/enemy5.png')
ennemi6 = charger.load('assets/enemy6.png')
ennemis = [ennemi1, ennemi2, ennemi3, ennemi4, ennemi5, ennemi6]  # Liste contenant toutes les frames
ennemi_base = [70,50,270,50,470,50,670,50]  # Coordonnées des ennemis
ennemi = ennemi_base.copy()
ennemi_change_base = [3, 50,3,50,3, 50,3,50,3, 50,3,50,3, 50,340]  # Déplacement x et y
if randint(1, 2) == 1:
    ennemi_change = ennemi_change_base.copy()
else:
    ennemi_change = [-3, 50, -3, 50, -3, 50, -3, 50, -3, 50, -3, 50, -3, 50, 340]
h = 0       # Variable utilisée pour le changement d'hauteur entre les differentes vagues
conteur = 0  # Variable utilisée pour compter
x = 0  # Variable utilisés pour le choix de frame dans la liste
score_temp = 0 # Le score du joueur

# Projectiles
projectile = []
projectile_active = False  # Variable notant si un projectile existe deja ou pas.
nb_projectiles = 100
bombe_image = charger.load('assets/bombe.png')
bombe_active = False
bombe_change = 6
bombe_coordonnées = [0,0]

# Sons du jeu
tirer = pygame.mixer.Sound("assets/shoot.wav")


# Alternative a range() puisque cette fonction comprends pas les decimales
def range_coordonees(debut, fin, etapes):
    l = []
    for i in range(int(debut * 10), int(fin * 10), int(etapes * 10)):
        l.append((i / 10))
    return l


# Dessin du vaisseau par rapport aux frames choisie.
def vaisseau(x, y):
    # Bords gauche et droite de l'ecran pour le vaisseau
    if spaceship[0] <= 0:
        spaceship[0] = 0
    if spaceship[0] >= 735:
        spaceship[0] = 735
    # Changement de frames vaisseau
    if spaceshipX_change < 0:
        screen.blit(frame_gauche, (x, y))
    elif spaceshipX_change > 0:
        screen.blit(frame_droite, (x, y))
    else:
        screen.blit(frame_default, (x, y))


# Dessin des enemis.
def ennemi_dessin(frame, x, y,e):
    # Bords gauche et droit de l'ecran et déplacement vertical
    if ennemi[e] <= 0:
        ennemi[e] = 0
        ennemi_change[e] = 3
        ennemi[e+1] += ennemi_change[e+1]  # Déplacement vers le bas de l'ennemi
    if ennemi[e] >= 739:
        ennemi[e] = 739
        ennemi_change[e] = -3
        ennemi[e+1] += ennemi_change[e+1]  # Déplacement vers le bas de l'ennemi
    ennemi[e] += ennemi_change[e]
    screen.blit(frame, (x, y))


# Dessin des projectiles
def projectiles(liste):
    pygame.draw.circle(screen, (255, 255, 255), (liste[0], liste[1]), 5)


# Dessin du score
def dessin_du_score(x, y):
    font = pygame.font.Font('assets/Minecraft.ttf', 20)
    score = font.render("Score : " + str(score_temp), True, (255, 255, 255))
    screen.blit(score, (x, y))


# Dessin du nombre restant de projectiles
def nombre_restant_projectiles(x, y):
    font = pygame.font.Font('assets/Minecraft.ttf', 20)
    score = font.render("Projectiles : " + str(nb_projectiles), True, (255, 255, 255))
    screen.blit(score, (x, y))

# Dessin de la bombe
def bombe1(coordonnee):
    screen.blit(bombe_image,(coordonnee[0],coordonnee[1]))



# Horloge permettant de définir la vitesse de rafraichissement de la page
clock = pygame.time.Clock()
# Boucle infinie du jeu
running = True
while running:
    # ici on déclare 60 tours par secondes soit une animation à 50 images par secondes
    clock.tick(60)
    # Detection de l'appui sur les clés
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:  # Quand n'importe quelle touche est pressée
            if event.key == pygame.K_SPACE and nb_projectiles > 0:
                if projectile_active == False:
                    projectile = []
                projectile_active = True
                projectile.append(spaceship[0] + 30)
                projectile.append(spaceship[1])
                nb_projectiles -= 1
                # Son du projectile lors du tir
                tirer.play()
            if event.key == pygame.K_LEFT:  # Quand fleche gauche pressée
                spaceshipX_change = -6
            if event.key == pygame.K_RIGHT:  # Quand fleche droite pressée
                spaceshipX_change = 6
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                spaceshipX_change = 0

    # Arriere plan (en RGB)
    screen.fill((0, 0, 0))
    # defilement du fond du  jeu
    bgY1 += bgY_change
    bgY2 += bgY_change
    if bgY1 >= 599:
        bgY1 = -1797
    if bgY2 >= 599:
        bgY2 = -1797
    # Dessin du fond (composé de deux images qui défilent en boucle)
    screen.blit(background1, (0, bgY1))
    screen.blit(background2, (0, bgY2))

    spaceship[0] += spaceshipX_change
    # Verification qu'un projectile existe bien.
    if projectile_active:
        # Des que les deux premier elements sont des projectiles usé on les supprimes
        if projectile_active:
            if projectile[0] == -1 and projectile[1] == -1:
                projectile.pop(0)
                projectile.pop(0)

        for i in range(0,len(projectile),2):
            # Mouvement vertical du projectile
            if projectile_active:
                projectiles([projectile[i],projectile[i+1]])
                projectile[i+1] -= 6
            # Mechanique de collision des projectiles avec les ennemis
            if projectile[i+1] <= 0:
                projectile[i] = -1
                projectile[i+1] = -1
            for t in range(0,len(ennemi),2):
                if int(ennemi[t]) - 5 <= projectile[i] <= int(ennemi[t]) + 65:
                   if projectile[i+1] in range(int(ennemi[t+1]), int(ennemi[t+1]) + 45):
                        score_temp += 100
                        projectile[i] = -1
                        projectile[i + 1] = -1
                        ennemi[t],ennemi[t+1],ennemi_change[t],ennemi_change[t+1] = 1000,1000,0,0
                        # Son de la mort de l'ennemi
                        mort = mixer.Sound("assets/death.mp3")
                        mort.play()
        if len(projectile) == 0:
            projectile_active = False
    print(ennemi)
    # Regeneration de la ligne d'ennemis
    if ennemi[1] == 1000 and ennemi[3]== 1000 and ennemi[5]== 1000 and ennemi[7]== 1000:
        ennemi = [70,50+h,270,50+h,470,50+h,670,50+h]
        h += 50
        if h>200:
            h = 50
        if randint(1,2) == 1:
            ennemi_change = ennemi_change_base.copy()
        else:
            ennemi_change = [-3, 50,-3,50,-3, 50,-3,50,-3, 50,-3,50,-3, 50,340]
    # Changement de frames de l'ennemi
    conteur += 1
    if conteur == 30:
        x += 1
        conteur = 0
        if x >= 5:
            x = 0
    vaisseau(spaceship[0], spaceship[1])
    for e in range(0,len(ennemi),2):
        ennemi_dessin(ennemis[x], ennemi[e], ennemi[e+1],e)
    if bombe_active == False:
        if randint(1,112) == 12:
            print("une bombe arrive !")
            enemi_number = randint(1,4) # Designation de l'ennemi a partir duquel la bombe va descendre
            g = 0
            # Stockage des coordonées de la bombe
            for t in range(1,5):
                if enemi_number == t and ennemi[g+1] != 1000:
                    bombe_active = True
                    bombe_coordonnées[0] = ennemi[g] + 25
                    bombe_coordonnées[1] = ennemi[g+1] + 39 + bombe_change
                g += 2
    else:
        bombe1(bombe_coordonnées)
        bombe_coordonnées[1] += bombe_change
        if spaceship[0]<=bombe_coordonnées[0]<= spaceship[0] + 64 and spaceship[1] < bombe_coordonnées[1] < spaceship[1] + 64:
            bombe_active = False
        elif bombe_coordonnées[1] > 600:
            bombe_active = False

    dessin_du_score(10, 15)
    nombre_restant_projectiles(10, 45)
    pygame.display.update()
