"""import time
a = time.time()
c=0
while c<100000000:
    c=c+1
b=time.time()
print(b-a)
print(1+2)"""



""""
import pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))

background = pygame.image.load("space.jpg")

pygame.display.set_caption("First")
icon = pygame.image.load("fuse.png")
pygame.display.set_icon(icon)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type in (pygame.KEYDOWN, pygame.KEYUP):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print("space")
                else:
                    print(event.key)

    pygame.display.update()"""


for i in range (0):
    print("test")
