import pygame 
pygame.init()

WIDTH = 1000
HEIGHT = 650  #800
screen = pygame.display.set_mode([WIDTH,HEIGHT])

fps = 60
timer = pygame.time.Clock()

# game variables 

wall_thickness = 10
gravity = 0.5
bounce_stop = 0.3

# track position of mouse to get movement-vector
mouse_trajectory = []

# Mass Ball
class Ball: 

    # assign parameters to ball which it should be initilized (constructor)
    # retention : how much to bounce, how much energy to lose, (between 0 to 0.9)
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


    # function of ball where it can draw itself in screen
    def draw(self):
        self.circle = pygame.draw.circle(screen, self.color, (self.x_pos, self.y_pos), self.radius)

    # gravity function
    def check_gravity(self):

        # if object is not selected gravity acts one way and if selected by mouse pointer, gravity behaves differently
        if not self.selected:
            # if y coodn < height then mass is in air, so we accelarate, refer to concept.jpg for below: 
            if self.y_pos < HEIGHT - self.radius - (wall_thickness/2):
                self.y_speed += gravity
            else:
                if self.y_speed > bounce_stop:
                    self.y_speed = self.y_speed * (-1 * self.retention)
                else:
                    if abs(self.y_speed) <= bounce_stop:
                        self.y_speed = 0

            # collision with boundary,             
            if (self.x_pos < self.radius + (wall_thickness/2) and self.x_speed <0 or self.x_pos > WIDTH - self.radius - (wall_thickness/2) and self.x_speed > 0):
                self.x_speed = self.x_speed * -1 * self.retention
                if abs(self.x_speed) < bounce_stop:
                    self.x_speed = 0
            
            # friction:
            if self.y_speed == 0 and self.x_speed != 0:
                if self.x_speed > 0:
                    self.x_speed -= self.friction
                elif self.x_speed < 0:
                    self.x_speed += self.friction

        else:

            # when mouse pointer swings the balls, we need to perform momentum, so we need to calculate push given by mouse
            self.x_speed = x_push
            self.y_speed = y_push

        return self.y_speed

    def update_pos(self, mouse):
        # if no mouse pointer then do movement like this: 
        if not self.selected:
            self.y_pos += self.y_speed
            self.x_pos += self.x_speed

        # if there is mouse pointer, do movement like this:
        else:
            self.x_pos = mouse[0]
            self.y_pos = mouse[1]


    def check_select(self, pos):
        self.selected = False
        # if mouse pointer and circle are collided or not ?
        if self.circle.collidepoint(pos):
            self.selected = True
        return self.selected 
    

# add walls to show a visible boundary
# pygame.draw.line(screen, (color), (Xi , Yi), (Xf , Yf))
def draw_walls():
    left = pygame.draw.line(screen, 'white', (0,0), (0,HEIGHT), wall_thickness)
    right = pygame.draw.line(screen, 'white', (WIDTH,0), (WIDTH,HEIGHT), wall_thickness)
    top = pygame.draw.line(screen, 'white', (0,0), (WIDTH, 0), wall_thickness)
    bottom = pygame.draw.line(screen, 'white', (0,HEIGHT), (WIDTH,HEIGHT), wall_thickness)

    wall_list = [left, right, top, bottom]
    return wall_list

# function to calculate push (momentum) given by mouse pointer
def calc_motion_vector():
    x_speed = 0
    y_speed = 0
    if len(mouse_trajectory) > 10:
        x_speed = (mouse_trajectory[-1][0] - mouse_trajectory[0][0]) / len(mouse_trajectory)
        y_speed = (mouse_trajectory[-1][1] - mouse_trajectory[0][1]) / len(mouse_trajectory)

        # trajectory list stores items like : [(x,y), (x,y), ....], so "[-1][0]" represents last element's x coordinate. 

    return x_speed, y_speed

# instance (initilizing ball)
ball1 = Ball(50, 50, 30,'blue', 100, 0.9, 0, 0, 1, 0.02)
ball2 = Ball(300,300,50, 'green', 300, 0.9, 0, 0, 2, 0.03)

balls = [ball1, ball2]


# main game loop
run = True
while run:
    timer.tick(fps)
    screen.fill('black')
    mouse_coords = pygame.mouse.get_pos()\
    # storing mouse coordinates and deleting it using QUEUE if num_elements > 20
    mouse_trajectory.append(mouse_coords)
    if len(mouse_trajectory) > 20:
        mouse_trajectory.pop(0)

    x_push, y_push = calc_motion_vector()

    # logics and implementation =====================================================================

    wall = draw_walls()
    ball1.draw()
    ball2.draw()

    ball1.y_speed = ball1.check_gravity()
    # passing mouse coordinates to update circle pos
    ball1.update_pos(mouse_coords)

    ball2.y_speed = ball2.check_gravity()
    ball2.update_pos(mouse_coords)

    ball1.check_gravity()


    # ===============================================================================================
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button ==1:
                if ball1.check_select(event.pos) or ball2.check_select(event.pos):
                    active_select =True
        
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                active_select = False
                for i in range(len(balls)):
                    balls[i].check_select((-1000,-1000))


    pygame.display.flip()
pygame.quit()
