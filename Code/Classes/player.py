class Player():
    def __init__(self, colour, pieces):
        self.colour = colour
        self.pieces = pieces

    def getPieces(self):
        return self.pieces

    def getColour(self):
        return self.colour