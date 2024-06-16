import sys
import pygame
from pygame.locals import *
from random import randint


# Initialize pygame
pygame.init()

# Game Variables and Assets
GAME_WIDTH = 800    
GAME_HEIGHT = 700
BACKGROUND = pygame.image.load("assets/img/bg4.png")
GROUND = pygame.image.load("assets/img/ground.png")
RESTART_BUTTON = pygame.image.load("assets/img/restart.png")
FONT = pygame.font.SysFont("Comic San Serif", 60)
FONT_COLOUR = (255, 255, 255)
START = False
GAMEOVER = False
SCORE = 0


# Set Display
screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("FLappyBirdy")

# Game speed
ground_scroll = 0
scroll_speed = 4

# Pipe properties
pipe_gap = 200 
pipe_freq = 1500 # Milliseconds
last_pipe = pygame.time.get_ticks() - pipe_freq
pass_pipe = False

# TImer 
clock = pygame.time.Clock()


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()
        self.velocity = 0
        self.counter = 0
        self.index = 0
        self.images = []
        for num in range(1, 4):
            img = pygame.image.load(f"assets/img/bird{num}.png")
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    
    def update(self):
        global GAMEOVER, START

        if START:  
            # Bird Gravity
            self.velocity = self.velocity + 0.5 if self.velocity < 8 else 8
            if self.rect.bottom < 532:
                self.rect.y += self.velocity

            # Jumps
            if GAMEOVER == False:
                if pygame.mouse.get_pressed()[0]:
                        self.velocity = - 8 
            
       
        # Bird Boundary
        if self.rect.y <= 0:
            self.rect.y = 0
            GAMEOVER = True

        if GAMEOVER == False:
            self.counter += 1
            self.cooldown = 5

            if self.counter > self.cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0

            self.image = self.images[self.index]

            # Rotate Bird Wwhe falling
            self.image = pygame.transform.rotate(self.images[self.index], self.velocity * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        super().__init__()
        self.image = pygame.image.load("assets/img/pipe.png")
        self.rect = self.image.get_rect()
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - pipe_gap//2]
        if position == -1:
            self.image = pygame.image.load("assets/img/pipe.png")
            self.rect.topleft = [x , y + pipe_gap//2]

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.x < -5:
            self.kill()

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):

        button_action = False
        # Get Mouse Position
        mouse_position = pygame.mouse.get_pos()

        # Check if the postion of the mouse is equal to the Button Position
        if self.rect.collidepoint(mouse_position):
            if pygame.mouse.get_pressed()[0]:
                button_action = True


        screen.blit(self.image, (self.rect.x, self.rect.y))

        return button_action

def render_text(text, font, text_colour, x_pos, y_pos):
    text_img = font.render(text, True, text_colour)
    screen.blit(text_img, (x_pos, y_pos))

# Bird Default Coordinate
bird_x, bird_y = 200, GAME_HEIGHT//2

# Bird sprite Group
bird_group = pygame.sprite.Group()

# Pipe Sprite Group
pipe_group = pygame.sprite.Group()

flappybirdy = Bird(bird_x, bird_y)
buttom_pipe = Pipe(350, int(GAME_HEIGHT / 2)- 65, -1)
top_pipe = Pipe(350, int(GAME_HEIGHT / 2)- 65, 1)

bird_group.add(flappybirdy)
# pipe_group.add(buttom_pipe, top_pipe)

# Restart Button
restart = Button(GAME_WIDTH//2 - 60, GAME_HEIGHT//2 - 50, RESTART_BUTTON)

# Game loop
while True:

    # Set sky on the screen
    screen.blit(BACKGROUND, (0,0))


    # Draw Bird Group
    bird_group.draw(screen)
    bird_group.update()

    # Check if the bird is on the ground
    if flappybirdy.rect.bottom > 532:      
        GAMEOVER = True
        START = False


    # Draw Pipe Group
    pipe_group.draw(screen)

    # Scoring in Game 
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right and pass_pipe == False:
            pass_pipe = True
        if pass_pipe:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                SCORE += 1
                pass_pipe = False

    render_text(str(SCORE), FONT, FONT_COLOUR, GAME_WIDTH//2, 20)
    # Set ground on the screen
    screen.blit(GROUND, (ground_scroll, 532))

    # Check for Collison
    if pygame.sprite.groupcollide(bird_group, pipe_group, 0, 0) or flappybirdy.rect.top == 0:
        GAMEOVER = True
        
    
    if GAMEOVER == False and START == True:
        # Bring new set of pipe on the screen
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_freq:
            pipe_height = randint(-100, 100)
            buttom_pipe = Pipe(GAME_WIDTH, int(GAME_HEIGHT / 2)- pipe_height - 50, -1)
            top_pipe = Pipe(GAME_WIDTH, int(GAME_HEIGHT / 2)- pipe_height -50, 1)
            pipe_group.add(buttom_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now

        ground_scroll -= scroll_speed

        if abs(ground_scroll) > 36:
            ground_scroll = 0
            
        pipe_group.update()

    if GAMEOVER == True:
        if restart.draw():
            GAMEOVER = False
            pipe_group.empty()
            flappybirdy.rect.y = bird_y
            flappybirdy.rect.x = bird_x
            SCORE = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if (event.type == pygame.MOUSEBUTTONDOWN and START == False) and GAMEOVER == False:
            START = True
            GAMEOVER = False
            # flappybirdy.rect.y = bird_y

    pygame.display.update()
    clock.tick(60)

