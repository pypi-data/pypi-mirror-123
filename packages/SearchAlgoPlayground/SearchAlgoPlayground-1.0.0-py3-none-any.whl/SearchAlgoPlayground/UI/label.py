import pygame

class Label:
    """
    Label to add on pygame screens

    Method
    ------
    draw(screen):
        Draws the label on the pygame screen
        screen: pygame screen
    
    setValue(text:str):
        Set the value for label


    """
    def __init__(self,color:tuple,size:int,pos:tuple,text:str=""):
        """
        color:tuple
            color of the label in (r,g,b) format
        size:int
            size of the label
        pos:tuple
            (x,y) coordinates for the position of label
        """
        self._color = color
        self._size = size
        self._font = pygame.font.SysFont("Arial", self._size)
        self._pos = pos
        self._text = text
    def draw(self,screen):
        """
        Draws the label on the pygame screen
        """
        text = self._font.render(self._text,True, self._color)
        text_rect = text.get_rect(center = self._pos)
        screen.blit(text, text_rect)
    def setValue(self,text):
        """
        Set the value for label
        """
        self._text = text
