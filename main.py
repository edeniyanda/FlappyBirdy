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

# Set Display
screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("FLappyBirdy")

# Game speed
ground_scroll = 0
scroll_speed = 4

# TImer
clock = pygame.time.Clock()


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()
        self.image = pygame.image.load("assets/img/bird1.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


bird_group = pygame.sprite.Group()
flappybirdy = Bird(100, int(GAME_WIDTH / 2))

bird_group.add(flappybirdy)


# Game loop
while True:

    # Set sky on the screen
    screen.blit(BACKGROUND, (0,0))

    # Draw Bird Group
    bird_group.draw(screen)

    # Set ground on the screen
    screen.blit(GROUND, (ground_scroll,532))

    ground_scroll -= scroll_speed

    if abs(ground_scroll) > 36:
        ground_scroll = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    clock.tick(60)

