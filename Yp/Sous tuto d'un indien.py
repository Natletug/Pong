import random
import pygame
pygame.init()

screen = pygame.display.set_mode((800, 600))

background = pygame.image.load("space.jpg")

pygame.display.set_caption("First")
icon = pygame.image.load("fuse.png")
pygame.display.set_icon(icon)

playerImg = pygame.image.load("fuse.png")
playerImg45deg = pygame.transform.rotate(playerImg, 45)
playerX = 385
playerY = 500
playerX_change = 0
playerY_change = 0
def player(x,y) :
    screen.blit(playerImg45deg, (x, y))
mobImg = []
mobX = [100, 200, 300, 400, 500, 600]
mobY = [50,150,50,150,50,150]
mobspeedX = [0.8, 0.8, 0.8, 0.8, 0.8, 0.8]
mobspeedY = [64, 64, 64, 64, 64, 64]
nummob = 6
for i in range(nummob):
    mobImg.append(pygame.image.load("mskn.png"))
    '''mobX.append(random.randint(0, 736))
    mobY.append(random.randint(0, 150))
    mobspeedX.append(0.5)
    mobspeedY.append(64)'''
def mob(x,y):
    for i in range(nummob):
        screen.blit (mobImg[i], (x, y))



projImg = pygame.image.load("proj.png")
projX = []
projY = []
projspeed =  5
numproj = 0
shoot = 0 


def proj(x,y):
    for i in range(numproj):
        screen.blit (projImg, (x, y))



running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False



    if event.type in (pygame.KEYDOWN, pygame.KEYUP):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -2
            if event.key == pygame.K_RIGHT:
                playerX_change = 2
            if event.key == pygame.K_UP:
                playerY_change = -1
            if event.key == pygame.K_DOWN:
                playerY_change = 1
            if event.key == pygame.K_RSHIFT:
                shoot += 1

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            playerX_change = 0
        if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
            playerY_change = 0
  
    


    playerX += playerX_change
    playerY += playerY_change
    if playerX <= -15:
        playerX = -15
    elif playerX >= 730:
        playerX = 730
    if playerY <= 336:
        playerY = 336
    elif playerY >= 536:
        playerY = 536
    #colisions wall
    for i in range(nummob):
        mobX[i] += mobspeedX[i]
        if mobX[i] < 0:
            mobX[i] = 1
            mobspeedX[i] *= -1
            mobY[i] += mobspeedY[i]
        elif mobX[i] > 736:
            mobX[i] = 735
            mobspeedX[i] *= -1
            mobY[i] += mobspeedY[i]

    

    projY.append(-100)
    if shoot > 50:
        shoot = 0
        projX.append(playerX+20)
        projY.append(playerY+337)
        numproj += 1
            
    projY.remove(-100)
    asupp = []
    numprojadel = 0
    for i in range(numproj):
        projY[i-1] -= projspeed
        if projY[i-1] + 69 < 0:
            asupp.append(i-1)
            numprojadel += 1
    numproj -= numprojadel
    for j in range (len(asupp)):
        del projY[asupp[j-1]]
        del projX[asupp[j-1]]

    print(playerY , projY)
    for i in range(0,numproj-1):
        proj(projX[i], projY[i])
    #loop
    player(playerX, playerY) 
    for i in range(nummob):
            mob(mobX[i], mobY[i])
    
    pygame.display.update()

