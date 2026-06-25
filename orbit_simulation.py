import pygame
import sys
import math


pygame.init()

WIDTH = 1000
HEIGHT = 1000
MAX_TRAIL = 580
zoom = 1.0
camera_x = WIDTH/2
camera_y = HEIGHT/2


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
planet1 = Body(500,300,6.1,0,(0,0,255),10,1)
sun = Body(500,500,0,0,(255,255,0),30,7500)
planet2 = Body(500,100,4.3,0,(255,0,0),15,5)
planet3 = Body(500,200,5,0,(180,0,255),12.5,3)
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
    keys = pygame.key.get_pressed()
    if keys[pygame.K_i]:
            zoom*= 1.01
    if keys[pygame.K_o]:
            zoom/= 1.01       
    screen.fill((0,0,0))
    update_physics(bodies)
    for body in bodies:
        sx = (body.x - camera_x)* zoom + WIDTH/2
        sy = (body.y - camera_y)* zoom + HEIGHT/2
        for i in range(len(body.trail)-1):
                x1, y1 = body.trail[i]
                x2, y2 = body.trail[i+1]
                sx1 = (x1 - camera_x) * zoom + WIDTH/2
                sy1 = (y1 - camera_y) * zoom + HEIGHT/2
                sx2 = (x2 - camera_x) * zoom + WIDTH/2
                sy2 = (y2 - camera_y) * zoom + HEIGHT/2
                pygame.draw.line(screen,body.color,(sx1,sy1),(sx2,sy2),2) 
        scaled_radius = max(1, int(body.radius*zoom))               
        pygame.draw.circle(screen,(body.color),(int(sx),int(sy)),body.radius)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
sys.exit()