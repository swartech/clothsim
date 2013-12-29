import pygame, sys, math
from pygame.locals import *

#declare constants
DAMPING = 1
GRAVITY = -10
RESTING_DISTANCE = 10
STIFFNESS = 0.45
ROWS = 32
COLUMNS = 100
cloth = []
dt = 0.1

def satisfy_constraints(p1, p2):
    dist_x = p1.x - p2.x
    dist_y = p1.y - p2.y
    dist = math.sqrt((dist_x ** 2) + (dist_y ** 2))
    if dist != 0:
        difference = (RESTING_DISTANCE - dist) / dist
        if not p1.fixed:
            p1.x += dist_x * STIFFNESS * difference
            p1.y += dist_y * STIFFNESS * difference
        if not p2.fixed:
            p2.x -= dist_x * STIFFNESS * difference
            p2.y -= dist_y * STIFFNESS * difference

class particle():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.old_x = x
        self.old_y = y
        self.accel_x = 0
        self.accel_y = 0
        self.fixed = False
        self.check_bounds()

    def apply_force(self, force_x, force_y):
        self.accel_x += force_x #assuming mass is 1
        self.accel_y -= force_y #assuming mass is 1

    def check_bounds(self):
        #bounds checking
        if self.x < 0:
            self.x = 1
        if self.x > 800:
            self.x = 799
        if self.y < 0:
            self.y = 1
        if self.y >700:
            self.y = 699

    def update(self):
        if not self.fixed:
            self.apply_force(0, GRAVITY)

            vel_x = self.x - self.old_x
            vel_y = self.y - self.old_y

            self.accel_x -= (vel_x * DAMPING)
            self.accel_y -= (vel_y * DAMPING)

            next_x = self.x + vel_x + (self.accel_x * 0.5 * dt * dt)
            next_y = self.y + vel_y + (self.accel_y * 0.5 * dt * dt)

            self.old_x = self.x
            self.old_y = self.y
            self.x = next_x
            self.y = next_y
            self.accel_x = 0
            self.accel_y = 0

        self.check_bounds()

pygame.init()
fps_clock = pygame.time.Clock()

window = pygame.display.set_mode((800, 700))
pygame.display.set_caption('Cloth Simulation')


def init():
    for r in range(ROWS):
        temp = []
        for c in range(COLUMNS):
            temp.append(particle(int(c * RESTING_DISTANCE * 0.8), int(0))) #/2 so it moves
        cloth.append(temp)

init()
cloth[0][0].fixed = True
cloth[0][10].fixed = True
cloth[0][20].fixed = True
cloth[0][40].fixed = True
cloth[0][79].fixed = True
cloth[0][99].fixed = True

#rendering loop
while True:

    window.fill(pygame.Color(255, 255, 255)) #clear the screen
    #satisfy constraints

    #first row and coloumn
    for c in range(1, len(cloth[0])):
         satisfy_constraints(cloth[0][c-1], cloth[0][c])
    for r in range(1, len(cloth)):
         satisfy_constraints(cloth[r-1][0], cloth[r][0])

    for r in range(1, len(cloth)):
        for c in range(1, len(cloth[0])):
            satisfy_constraints(cloth[r][c-1], cloth[r][c])
            satisfy_constraints(cloth[r-1][c], cloth[r][c])

    #draw lines
    #first row and coloumn
    for c in range(1,len(cloth[0])):
        pygame.draw.aaline(window, (55, 55, 55), (cloth[0][c-1].x, cloth[0][c-1].y), (cloth[0][c].x, cloth[0][c].y))
    for r in range(1, len(cloth)):
        pygame.draw.aaline(window, (55, 55, 55), (cloth[r-1][0].x, cloth[r-1][0].y), (cloth[r][0].x, cloth[r][0].y))

    for r in range(1, len(cloth)):
        for c in range(1,len(cloth[0])):
            pygame.draw.aaline(window, (55, 55, 55), (cloth[r][c-1].x, cloth[r][c-1].y), (cloth[r][c].x, cloth[r][c].y))
            pygame.draw.aaline(window, (55, 55, 55), (cloth[r-1][c].x, cloth[r-1][c].y), (cloth[r][c].x, cloth[r][c].y))

    #event handling
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
                init()
            elif event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

    #update
    for r in range(len(cloth)):
        for c in range(len(cloth[0])):
            cloth[r][c].update()

    pygame.display.update()
    fps_clock.tick(30)