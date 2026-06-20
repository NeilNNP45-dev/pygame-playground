import pygame
import sys

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Pygame Playground")

running = True
x=400
y=300
vx = 5
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0,0,0))
    x +=  vx       
    pygame.draw.circle(screen,(255,255,0),(x,y), 50)
    if x+50>=WIDTH or x-50<=0:
        vx*= -1
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
sys.exit()