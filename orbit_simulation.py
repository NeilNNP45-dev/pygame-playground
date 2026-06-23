import pygame
import sys
import math


pygame.init()

WIDTH = 1000
HEIGHT = 1000


screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Pygame Playground")

running = True
class Body:
    def __init__(self,x,y,vx,vy,color,radius,mass):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.radius = radius
        self.mass = mass
planet1 = Body(500,300,6.1,0,(0,0,255),10,1)
sun = Body(500,500,0,0,(255,255,0),30,7500)
planet2 = Body(500,100,4.3,0,(255,0,0),15,5)
bodies = [sun,planet1,planet2]
G= 1
ax = 1
ay = 1
def update_physics(bodies):
    sun = bodies[0]
    for body in bodies:
        if body is sun:
            continue
        dx = sun.x - body.x
        dy = sun.y - body.y 
        distance = math.sqrt(dx**2 + dy**2 +100)
        a = G*sun.mass/distance**2
        ax = a*dx/distance
        ay = a*dy/distance
        body.vx += ax
        body.x +=  body.vx
        body.vy += ay  
        body.y += body.vy
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0,0,0))
    update_physics(bodies)
    for body in bodies:
        pygame.draw.circle(screen,(body.color),(body.x,body.y),body.radius)
        if body.x+body.radius>=WIDTH or body.x-body.radius<=0:
           body.vx*= -1
        if body.y+body.radius>=HEIGHT or body.y-body.radius<=0:
           body.y = HEIGHT-body.radius
           body.vy*= -1
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
sys.exit()