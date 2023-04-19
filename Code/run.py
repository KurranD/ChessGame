import pygame
import sys
import os
import time

from pygame.locals import *

from Classes.button import Button
from gamelogic import Game

"""
    Script that starts the game. Initializes the board and runs everything within
    the main game's while loop.
"""

pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((690, 690))

game_state = ['menu']
pygame.display.set_caption('Chess')

start_button = Button(220, 315)
exit_button = Button(220, 440)

game = Game()

while True:
    screen.fill((0,0,0))
    clock.tick(60)
    if 'menu' in game_state:
        background = game.menu_display(game_state, start_button, exit_button)
        screen.blit(background, (0, 0))
    elif 'game' in game_state:
        screen.blit(background, (0, 0))
        game.draw_pieces(screen)
        game.game()
    elif 'gameOver' in game_state:
        # Recreates new instance of game to play again.
        game = Game()
        # sleep is added because without the delay the click that ended the game can carry over to the menu, starting a new game.
        time.sleep(0.2)
        game.game_state_manager(game_state, 'menu')
    
    x, y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    pygame.display.update()