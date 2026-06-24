import pygame
import sys
import math


pygame.init()

WIDTH = 1000
HEIGHT = 1000
MAX_TRAIL = 600


screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Pygame Playground")

running = True
class Body:
    def __init__(self,x,y,vx,vy,color,radius,mass,):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.radius = radius
        self.mass = mass
        self.trail = []
planet1 = Body(500,300,6.1,0,(0,0,255),10,10)
sun = Body(500,500,0,0,(255,255,0),30,7500)
planet2 = Body(500,100,4.3,0,(255,0,0),15,50)
planet3 = Body(500,200,5,0,(180,0,255),12.5,30)
bodies = [sun,planet1,planet2,planet3]
G= 1
def update_physics(bodies):
    for body in bodies:
        total_ax = 0
        total_ay = 0
        for other_body in bodies:
            if body is other_body:
                continue
            dx = other_body.x - body.x
            dy = other_body.y - body.y 
            distance = math.sqrt(dx**2 + dy**2 +100)
            a = G*other_body.mass/distance**2
            ax = a*dx/distance
            ay = a*dy/distance
            total_ax += ax
            total_ay += ay
        body.vx += total_ax
        body.vy += total_ay
        body.x += body.vx
        body.y += body.vy         
        body.trail.append((body.x, body.y))
        if len(body.trail)>MAX_TRAIL:
            body.trail.pop(0)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0,0,0))
    update_physics(bodies)
    for body in bodies:
        for i in range(len(body.trail)-1):
                pygame.draw.line(screen,body.color,body.trail[i],body.trail[i+1],2)
        pygame.draw.circle(screen,(body.color),(body.x,body.y),body.radius)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
sys.exit()