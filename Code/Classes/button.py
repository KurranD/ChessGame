import pygame
import os

class Button():
    """
        Class for abstracting away making objects clickable and loading images.

        Suggestions:
        In the constructor, you set the size of the button to a fixed size of (200, 100) if no image is provided. It would be more flexible to allow the caller to specify the size of the button as a parameter.
When loading the image in the constructor, you use a relative path to the image file. This could potentially cause problems if the caller is not running the program from the same working directory as the script. It would be better to use an absolute path or provide a way for the caller to specify the path to the image file.
In the update_image() method, you reload the image from the file each time the method is called. This could potentially slow down the program if the image needs to be updated frequently. It would be more efficient to load the image once in the constructor and store it as a member variable, then update the member variable when the image needs to be changed.
In the click() method, you use pygame.mouse.get_pressed()[0] to check if the left mouse button is pressed. This assumes that the left mouse button is the only button that can be used to click the button. It would be better to check if any mouse button is pressed using pygame.mouse.get_pressed() and then check if the button that was pressed was the left button using event.button == 1.
It's generally a good practice to have a __repr__() method for your classes, so that you can print out a human-readable representation of the object for debugging purposes.
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
        if x_pos < 0 or x_pos > 690 or y_pos < 0 or y_pos > 690:
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
        self.__rect.topleft = (x_pos,  y_pos)

    def update_image(self, image_path):
        """
            Update the button's image (this comes up when a pawn reaches the end of the board and can be swapped for a queen)

            Parameters
            ----------
                image_path: string
                    The path for the new image to use
        """
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