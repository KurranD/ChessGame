import pygame
import os

class Button():
    def __init__(self, x, y, image_path=None):
        self.x = x
        self.y = y
        if image_path == None:
            self.rect = pygame.Rect((x, y), (200, 100))
            self.clicked = False
        else:
            self.image = pygame.image.load(os.path.join('./', image_path))
            self.rect = self.image.get_rect()
            self.rect.topleft = (x, y)
            self.clicked = False

    def move(self, x, y):
        self.x = x
        self.y = y
        self.rect.topleft = (x, y)

    def getPos(self):
        return (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def click(self):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        return action