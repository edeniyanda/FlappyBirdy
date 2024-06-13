import sys
import pygame
from pygame.locals import *

pygame.init()

# Game Variables
GAME_WIDTH = 800    
GAME_HEIGHT = 600

# Set Display
screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("FLappyBirdy")


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

