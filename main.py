import sys
import pygame
from pygame.locals import *


# Initialize pygame
pygame.init()

# Game Variables and Assets
GAME_WIDTH = 800    
GAME_HEIGHT = 700
BACKGROUND = pygame.image.load("assets/img/bg4.png")
GROUND = pygame.image.load("assets/img/ground.png")
START = False
GAMEOVER = False


# Set Display
screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("FLappyBirdy")

# Game speed
ground_scroll = 0
scroll_speed = 4

# Pipe Gap
pipe_gap = 70 

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
            else:
                GAMEOVER = True
                START = False


        # Jumps 
        if pygame.mouse.get_pressed()[0]:
            self.velocity = - 8 
       
        # Bird Boundary
        if self.rect.y <= 0:
            self.rect.y = 0

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




# Bird Default Coordinate
bird_x, bird_y = 200, int(GAME_WIDTH / 2) - 300

# Bird sprite Group
bird_group = pygame.sprite.Group()

# Pipe Sprite Group
pipe_group = pygame.sprite.Group()

flappybirdy = Bird(bird_x, bird_y)
buttom_pipe = Pipe(350, int(GAME_HEIGHT / 2)- 65, -1)
top_pipe = Pipe(350, int(GAME_HEIGHT / 2)- 65, 1)

bird_group.add(flappybirdy)
pipe_group.add(buttom_pipe, top_pipe)


# Game loop
while True:

    # Set sky on the screen
    screen.blit(BACKGROUND, (0,0))


    # Draw Bird Group
    bird_group.draw(screen)
    bird_group.update()

    # Draw Pipe Group
    pipe_group.draw(screen)
    pipe_group.update()

    # Set ground on the screen
    screen.blit(GROUND, (ground_scroll, 532))
    
    if GAMEOVER == False:
        ground_scroll -= scroll_speed

        if abs(ground_scroll) > 36:
            ground_scroll = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if (event.type == pygame.MOUSEBUTTONDOWN and START == False) or GAMEOVER == True:
            START = True
            GAMEOVER = False
            # flappybirdy.rect.y = bird_y

    pygame.display.update()
    clock.tick(60)

