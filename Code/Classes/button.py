import pygame
import os

class Button():
    """
        Class for abstracting away making objects clickable and loading images.
    """
    def __init__(self, x_pos, y_pos, image_path=None):
        """
            Initialize the Button object

            Parameters
            ----------
                x_pos: integer
                    Pixel x-coordinate for the button
                y_pos: integer
                    Pixel y-coordinate for the button
                image_path: string
                    Path for the image to use, leave empty to have a button without an image.
        """

        self.__button_error_handling(x_pos, y_pos, image_path)
        if image_path == None:
            self.__rect = pygame.Rect((x_pos, y_pos), (200, 100))
        else:
            self.__image = pygame.image.load(os.path.join('./', image_path))
            self.__rect = self.__image.get_rect()
            self.__rect.topleft = (x_pos, y_pos)
        self.__clicked = False

    def __button_error_handling(self, x_pos, y_pos, image_path):
        if x_pos == None or y_pos == None or x_pos < 0 or x_pos > 690 or y_pos < 0 or y_pos > 690:
            raise ValueError("Button coordinates outside the screen: ({},{})".format(x_pos, y_pos))
        if(image_path != None and not os.path.isfile(image_path)):
                raise ValueError("Image can't be found: {}".format(image_path))

    def move(self, x_pos, y_pos):
        """
            Update the button's position

            Parameters
            ----------
                x_pos: integer
                    Pixel x-coordinate for the button
                y_pos: integer
                    Pixel y-coordinate for the button
        """
        self.__button_error_handling(x_pos, y_pos, None)
        self.__rect.topleft = (x_pos,  y_pos)

    def update_image(self, image_path):
        """
            Update the button's image (this comes up when a pawn reaches the end of the board and can be swapped for a queen)

            Parameters
            ----------
                image_path: string
                    The path for the new image to use
        """
        if(image_path == None or not os.path.isfile(image_path)):
            raise ValueError("Image can't be found: {}".format(image_path))
        
        self.__image = pygame.image.load(os.path.join('./', image_path))

    def draw(self, screen):
        """
            Draw  the image to the screen using pygame's blit method

            Parameters
            ----------
                screen: pygame display
                    The pygame display image to add the image to.
        """
        screen.blit(self.__image, self.__rect.topleft)

    def click(self):
        """
            Register a click within the button's boundaries. 

            Returns
            -------
                boolean
                    Checks for a click within the button's boundaries and returns True or False accordingly.
        """
        pos = pygame.mouse.get_pos()

        if self.__rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.__clicked:
                self.__clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.__clicked = False

        return self.__clicked