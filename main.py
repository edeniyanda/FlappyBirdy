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
        self.counter += 1
        self.cooldown = 5

        if self.counter > self.cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0

        self.image = self.images[self.index]



bird_group = pygame.sprite.Group()
flappybirdy = Bird(100, int(GAME_WIDTH / 2) - 50)

bird_group.add(flappybirdy)


# Game loop
while True:

    # Set sky on the screen
    screen.blit(BACKGROUND, (0,0))

    # Draw Bird Group
    bird_group.draw(screen)
    bird_group.update()

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

