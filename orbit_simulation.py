import pygame
import sys
import math


pygame.init()

WIDTH = 1280
HEIGHT = 720
MAX_TRAIL = 600
zoom = 1.0
camera_x = WIDTH/2
camera_y = HEIGHT/2


screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont(None, 28)
clock = pygame.time.Clock()
pygame.display.set_caption("Pygame Playground")

running = True
class Body:
    def __init__(self,x,y,vx,vy,color,radius,mass,):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.ax = 0
        self.ay = 0
        self.color = color
        self.radius = radius
        self.mass = mass
        self.trail = []
planet1 = Body(500,300,6.1,0,(0,0,255),10,1)
sun = Body(500,500,0,0,(255,255,0),30,7500)
planet2 = Body(500,100,4.3,0,(255,0,0),15,1)
planet3 = Body(500,200,5,0,(180,0,255),12.5,1)
planet4 = Body(500,0,3.8,0,(0,255,255),17,1 )
planet5 = Body(500,400,8.66,0,(255,167,0),9,1)
bodies = [sun,planet1,planet2,planet3,planet4,planet5]
G= 1
time_scale = 80
def compute_accelerations(bodies):  #ill start adding comments now as the project is getting bigger and more complex. This is to calc acceleration. 
    for body in bodies:
        total_ax = 0
        total_ay = 0

        for other_body in bodies:
            if body is other_body:
                continue
            dx = other_body.x - body.x
            dy = other_body.y - body.y
            distance_sq = dx**2 + dy**2 + 1 # 1 is added for softnening so planets dont go crazy when distance between them becomes very small or 0
            distance = math.sqrt(distance_sq)
            a = G * other_body.mass / distance_sq
            total_ax += a * dx / distance
            total_ay += a * dy / distance
        body.ax = total_ax
        body.ay = total_ay
def update_velocities(bodies, factor, sim_dt): # This is to calc velocity.
                                               #Velocity update is split into two half-steps for Leapfrog integration which will improve long-term orbital stability. #
                                               # Factor is used to integrate leapfrog method (update things in 2 phases as velocity and position change acceleration will change too.) for cleaner orbiting than the earlier method (semi euler method)
    for body in bodies:
        body.vx += body.ax * sim_dt * factor
        body.vy += body.ay * sim_dt * factor
def update_positions(bodies,sim_dt): #This is to calc position of bodies. pretty understandable i think on its own.
    for body in bodies:
        body.x += body.vx * sim_dt
        body.y += body.vy * sim_dt
        body.trail.append((body.x, body.y))
        if len(body.trail) > MAX_TRAIL: # This so trails dont keep going on forever and use a lot of ram
            body.trail.pop(0)

while running:
    dt = (clock.tick(60)/1000)
    sim_dt = dt * time_scale
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_i]:
            zoom*= 1.01
    if keys[pygame.K_o]:
            zoom/= 1.01  
    if keys[pygame.K_a]:
     camera_x -= 300*dt/ zoom  
    if keys[pygame.K_d]:
     camera_x += 300*dt / zoom
    if keys[pygame.K_w]:
     camera_y -= 300*dt/ zoom
    if keys[pygame.K_s]:
     camera_y += 300*dt / zoom             
    screen.fill((0,0,0))
    compute_accelerations(bodies)          # a(t) 
    update_velocities(bodies, 0.5,sim_dt)  # half step updation of velocity
    update_positions(bodies,sim_dt)        # full position step
    compute_accelerations(bodies)          # a(t+1)
    update_velocities(bodies, 0.5,sim_dt)  # second half step updation of velocity
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
                pygame.draw.line(screen,body.color,(sx1,sy1),(sx2,sy2),1) 
        scaled_radius = max(1, int(body.radius*zoom))               
        pygame.draw.circle(screen,(body.color),(int(sx),int(sy)),scaled_radius)
    hud_lines = [
    f"FPS: {clock.get_fps():.1f}",
    f"Bodies: {len(bodies)}",
    f"Zoom: {zoom:.2f}x",
    f"Time Scale: {time_scale}x",
    f"Integrator: Leapfrog"]
    for i, line in enumerate(hud_lines):
     text_surface = font.render(line, True, (255, 255, 255))
     screen.blit(text_surface, (10, 10 + i * 30))
    pygame.display.flip()
pygame.quit()
sys.exit()