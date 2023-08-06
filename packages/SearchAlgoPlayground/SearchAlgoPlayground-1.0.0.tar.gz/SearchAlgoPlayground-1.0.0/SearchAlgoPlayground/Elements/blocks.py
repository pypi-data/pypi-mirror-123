import pygame
class Block:
    """
    Block defines the world tiles. Blocks represents the world in 2-Dimensional array format.
    ...

    Attribute
    ---------
    x:int
        x coordinate in the window plane of the block

    y:int
        y coordinate in the window plane of the block

    size:int
        size of the block, denotes one side of the square block
    
    id:tuple
        id represents position in the 2D matrix of the block
        (x,y) where x is the row and y is the column
    
    pgObj
        pygame rect object
    
    Methods
    -------
    draw_block(screen)
        draws the block on pygame window
        screen: pygame window

    highlight(val:bool)
        highlights block with highlist color
        val:bool - true to enable highlight
    
    pos() -> tuple
        returns the coordinate of the centre of the block on the pygame window
    
    setHasNode(val:bool)
        sets the value for the flag _hasNode to represent that a block contains a node
    
    hasNode()->bool
        returns true if block has node over it

    to_dict()->dict
        returns the object details with all attribute and values as dictionary

    """
    def __init__(self,x:int,y:int,size:int,id:tuple,grid_color:tuple = (163, 175, 204),grid_width:int = 1):
        """
        Parameters
        ---------
        x:int
            x coordinate in the window plane of the block

        y:int
            y coordinate in the window plane of the block

        size:int
            size of the block, denotes one side of the square block

        id:tuple
            id represents position in the 2D matrix of the block
            (x,y) where x is the row and y is the column

        gird_color:tuple
            rgb color (r,g,b) value for the block boundary default ((163, 175, 204))

        grid_width:int
            width of the boundary default 1
        """
        self.x = x
        self.y = y
        self.size = size
        self._grid_color = grid_color
        self._grid_width = grid_width
        self.id = id
        self._hasNode = False #Tells whether there is a node over the block
        self.pgObj = None #pyGame object
        self._isHighlighted = False #Highlighting the blocks
    def draw_block(self,screen):
        """
        Draws the block on the screen
        """
        self.pgObj = pygame.draw.rect(screen, self._grid_color, pygame.Rect((self.x, self.y, self.size,self.size)), self._grid_width)
        if self._isHighlighted:
            pygame.draw.rect(screen,self._grid_color,pygame.Rect((self.x+2, self.y+2, self.size-4,self.size-4)))
    def highlight(self,val:bool):
        """
        Highlight the block
        Useful to show which block is selected
        """
        self._isHighlighted = val
    def pos(self):
        """
        Returns Exact coordinates in 2D screen space
        """
        if self.pgObj is None:
            raise AttributeError("Block is not yet drawn")
        else:
            return self.pgObj.center
    
    def __str__(self):
        return "<Block id="+str(self.id)+">"

    def setHasNode(self,val:bool):
        """
        Function sets the value whether the block has node or not
        """
        self._hasNode = val
    def hasNode(self)->bool:
        """
        Returns true if the block has a node over it
        """
        return self._hasNode
    def to_dict(self)->dict:
        """
        Returns the attributes and values as dictionary
        """
        block = {
            "x": self.x,
            "y":self.y,
            "id":self.id,
            "size":self.size,
            "gird_color":str(self._grid_color),
            "grid_width": self._grid_width,
            "hasNode": self._hasNode
        }
        return block