import pygame 
import math
pygame.init()

WIDTH = 1000
HEIGHT = 650
screen = pygame.display.set_mode([WIDTH, HEIGHT])

fps = 60
timer = pygame.time.Clock()

# Game variables 
wall_thickness = 10
gravity = 0.5
bounce_stop = 0.3

# Track mouse movement
mouse_trajectory = []



# Mass Ball
class Ball: 
    def __init__(self, x_pos, y_pos, radius, color, mass, retention, x_speed, y_speed, id, friction):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.radius = radius 
        self.retention = retention
        self.color = color
        self.mass = mass
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.id = id
        self.circle = ''
        self.selected = False
        self.friction = friction

    def draw(self):
        self.circle = pygame.draw.circle(screen, self.color, (int(self.x_pos), int(self.y_pos)), self.radius)

    def check_gravity(self):
        if not self.selected:
            if self.y_pos < HEIGHT - self.radius - (wall_thickness/2):
                self.y_speed += gravity
            else:
                if self.y_speed > bounce_stop:
                    self.y_speed = self.y_speed * (-1 * self.retention)
                else:
                    if abs(self.y_speed) <= bounce_stop:
                        self.y_speed = 0

            if (self.x_pos < self.radius + (wall_thickness/2) and self.x_speed < 0 or 
                self.x_pos > WIDTH - self.radius - (wall_thickness/2) and self.x_speed > 0):
                self.x_speed = self.x_speed * -1 * self.retention
                if abs(self.x_speed) < bounce_stop:
                    self.x_speed = 0

            if self.y_speed == 0 and self.x_speed != 0:
                if self.x_speed > 0:
                    self.x_speed -= self.friction
                elif self.x_speed < 0:
                    self.x_speed += self.friction
        else:
            self.x_speed = x_push
            self.y_speed = y_push

        return self.y_speed

    def update_pos(self, mouse):
        if not self.selected:
            self.y_pos += self.y_speed
            self.x_pos += self.x_speed
        else:
            self.x_pos = mouse[0]
            self.y_pos = mouse[1]

    def check_select(self, pos):
        self.selected = False
        if self.circle.collidepoint(pos):
            self.selected = True
        return self.selected 
    
    def clamp_inside_walls(self):
        left = self.radius + (wall_thickness / 2)
        right = WIDTH - self.radius - (wall_thickness / 2)
        top = self.radius + (wall_thickness / 2)
        bottom = HEIGHT - self.radius - (wall_thickness / 2)

        if self.x_pos < left:
            self.x_pos = left
            if self.x_speed < 0:
                self.x_speed = -self.x_speed * self.retention
                if abs(self.x_speed) < bounce_stop: self.x_speed = 0
        if self.x_pos > right:
            self.x_pos = right
            if self.x_speed > 0:
                self.x_speed = -self.x_speed * self.retention
                if abs(self.x_speed) < bounce_stop: self.x_speed = 0
        if self.y_pos > bottom:
            self.y_pos = bottom
            if self.y_speed > 0:
                self.y_speed = -self.y_speed * self.retention
                if abs(self.y_speed) < bounce_stop: self.y_speed = 0
        if self.y_pos < top:
            self.y_pos = top
            if self.y_speed < 0:
                self.y_speed = -self.y_speed * self.retention

# Draw visible walls
def draw_walls():
    left = pygame.draw.line(screen, 'white', (0,0), (0,HEIGHT), wall_thickness)
    right = pygame.draw.line(screen, 'white', (WIDTH,0), (WIDTH,HEIGHT), wall_thickness)
    top = pygame.draw.line(screen, 'white', (0,0), (WIDTH, 0), wall_thickness)
    bottom = pygame.draw.line(screen, 'white', (0,HEIGHT), (WIDTH,HEIGHT), wall_thickness)
    return [left, right, top, bottom]

# Calculate mouse push (momentum)
def calc_motion_vector():
    x_speed = 0
    y_speed = 0
    if len(mouse_trajectory) > 10:
        x_speed = (mouse_trajectory[-1][0] - mouse_trajectory[0][0]) / len(mouse_trajectory)
        y_speed = (mouse_trajectory[-1][1] - mouse_trajectory[0][1]) / len(mouse_trajectory)
    return x_speed, y_speed

# ======================================================
# New: Proper 2D Ball-to-Ball collision with momentum
# ======================================================
def check_b2b_collision(balls):
    for i in range(len(balls)):
        for j in range(i+1, len(balls)):
            A = balls[i]
            B = balls[j]

            #check if collision happens or not: 
            dx = B.x_pos - A.x_pos
            dy = B.y_pos - A.y_pos
            centre_distance = math.sqrt(dx*dx + dy*dy)

            if centre_distance <= A.radius + B.radius:

                # overlap concept: 
                overlap = (A.radius + B.radius) - centre_distance
                if centre_distance != 0:
                    nx = dx / centre_distance
                    ny = dy / centre_distance
                else:
                    nx, ny = 1, 0

                # inverse mass concept: 
                inv_m1 = 1.0 / A.mass
                inv_m2 = 1.0 / B.mass
                total_inv = inv_m1 + inv_m2

                moveA = overlap * (inv_m1 / total_inv)
                moveB = overlap * (inv_m2 / total_inv)

                A.x_pos -= nx * moveA
                A.y_pos -= ny * moveA
                B.x_pos += nx * moveB
                B.y_pos += ny * moveB

                # ensure wall boundary suring b2b actions: 
                A.clamp_inside_walls()
                B.clamp_inside_walls()

                # Relative velocity 
                dvx = B.x_speed - A.x_speed #vb-va for x position
                dvy = B.y_speed - A.y_speed #vb-va for y position
                rel_vel = dvx * nx + dvy * ny

                # if balls are already seprarating: 
                if rel_vel > 0:
                    continue

                # Elastic collision impulse
                e = min(A.retention, B.retention)  
                j = -(1 + e) * rel_vel
                j /= (1/A.mass + 1/B.mass)

                # Apply impulse
                impulse_x = j * nx
                impulse_y = j * ny

                A.x_speed -= impulse_x / A.mass
                A.y_speed -= impulse_y / A.mass
                B.x_speed += impulse_x / B.mass
                B.y_speed += impulse_y / B.mass


ball1 = Ball(300, 300, 30, 'blue', 100, 0.9, 0, 0, 1, 0.02)
ball2 = Ball(500, 300, 50, 'green', 300, 0.9, 0, 0, 2, 0.03)
ball3 = Ball(780, 118, 70, 'red', 500, 0.9, 0, 0, 3, 0.05)

balls = [ball1, ball2, ball3]

# Main game loop
run = True
active_select = False
while run:
    timer.tick(fps)
    screen.fill('black')
    mouse_coords = pygame.mouse.get_pos()
    mouse_trajectory.append(mouse_coords)
    if len(mouse_trajectory) > 20:
        mouse_trajectory.pop(0)

    x_push, y_push = calc_motion_vector()

    wall = draw_walls()
    for b in balls:
        b.draw()
        b.y_speed = b.check_gravity()
        b.update_pos(mouse_coords)

    # Check collisions and momentum
    check_b2b_collision(balls)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button ==1:
                if any(b.check_select(event.pos) for b in balls):
                    active_select = True
        
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                active_select = False
                for b in balls:
                    b.check_select((-1000,-1000))

    pygame.display.flip()
pygame.quit()
