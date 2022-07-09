import pygame
import sys
import os

from pygame.locals import *

from Classes.button import Button
from gamelogic import Game

def menu_display(game_state):
    bg = pygame.image.load(os.path.join('./', 'Images/Menu.png'))
    if start_button.click():
        bg = pygame.image.load(os.path.join('./', 'Images/chess_board.jpg'))
        game_state_manager(game_state, 'game')
    if exit_button.click():
        sys.exit()
    return bg

def game_display():
    return False

def game_state_manager(game_state, new_state):
    game_state.clear()
    game_state.append(new_state)

pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((690, 690))

game_state = ['menu']
pygame.display.set_caption('Chess')

start_button = Button(220, 315)
exit_button = Button(220, 440)

game = Game(screen)

while True:
    screen.fill((0,0,0))
    clock.tick(60)
    if 'menu' in game_state:
        bg = menu_display(game_state)
        screen.blit(bg, (0, 0))
    elif 'game' in game_state:
        screen.blit(bg, (0, 0))
        game.draw_pieces(screen)
        game.game(screen)
    
    x, y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    pygame.display.update()