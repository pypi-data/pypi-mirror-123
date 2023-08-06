import pygame
from SearchAlgoPlayground.config import *
from .blocks import Block


COLOR_ACTIVE = config["ELEMENT_ACTIVE_COLOR"]
class Node(Block):
    """
    A node is a type of block that is important to the world 
    Node class inherits the Block class
    ...

    Attributes
    ----------
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
    
    pos:tuple
        coordinate in pygame window for center of the node

    Methods
    -------
    draw_block(screen)
        draws the node on pygame window
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
    
    set_label(label:str,screen)
        sets the label on the node
        screen - a pygame window
        label:str - a string value that'll be displayed on node

    selected(val:bool)
        sets isSelected flag value

    set_color(color:tuple)
        sets the color of the node
        color:tuple - A rgb value in the form (r,g,b)
    
    get_label()->str
        returns value of label of the node

    setLocation(block:Block)
        sets the location to the new block
        block:Block - A Block class object
        NOTE: Location for nodes are defined by the block they resides on

    handle_event(world:World,event,infoLabel)
        Internal method to handle the pygame events
    
    add_neighbour(node:Node)
        Adds the given node as neighbouring node if it's not already a neighbouring node, should be used when it has an edge with the given node
        node:Node - A Node class object

    remove_neighbour(node:Node)
        Removes the given node from neighbouring node if it's in neighbouring node
        node:Node - A Node class object
    
    get_neighbour()->list
        Returns list of neighbouring nodes(Node class objects) which is sorted in order with their label
    

    """
    def __init__(self, block:Block,label:str,colorOutline:tuple,colorNode:tuple,outlineWidth:int=2,specialNodeStatus:bool = False):
        super().__init__(block.x,block.y,block.size,block.id,block._grid_color,block._grid_width)
        """
        Parameters
        -----------
        block:Block
            A Block class object on which the node will be drawn

        label:str
            Label of the node
        
        colorOutline:tuple
            A rgb value of the form (r,g,b) represents outline color of the node

        colorNode:tuple
            A rgb value of the form (r,g,b) represents color of the node

        outlineWidth:int
            Width of the outline of the node default 2

        specialNodeStatus:bool
            sets whether the node is special default is False
            NOTE: A special node must be present on playground all time, i.e. delete is not allowed

        """
        self._label = label
        self._colorOutline = colorOutline
        self._colorNode = colorNode
        self._defaultOutlineColor = colorOutline
        self.pos = block.pos()
        self._font = pygame.font.Font(None, int(self.size*0.80))
        self._txt_surface = self._font.render(label, True, self._colorOutline)
        self._outlineWidth = outlineWidth
        self._oldLabel = None #Label before editing happened
        self._active = False #A node is active when it's selected
        self._specialNodeStatus = specialNodeStatus #Tells whether the node is special or not, Goal and Start nodes must be special
        self._isSelected = False

        self._neighbourNodes = [] #Neighbour nodes that are connected with an edge

    def draw_block(self,screen):
        """
        Draws the node on the screen
        """
        pygame.draw.circle(screen, self._colorNode, self.pos,int(self.size/2))
        outlineColor = config["SELECTED_NODE_COLOR"] if self._isSelected and not self._active else self._colorOutline
        self.pgObj = pygame.draw.circle(screen, outlineColor, self.pos,int(self.size/2),self._outlineWidth)
        self.set_label(self._label,screen)
    def set_label(self,label:str,screen):
        """
        Set the label for the node
        """
        self._label = label
        text = self._font.render(self._label, True, self._colorOutline)
        text_rect = text.get_rect(center = self.pgObj.center)
        screen.blit(text, text_rect)

    def selected(self,val:bool):
        """
        Set the node selected 
        """
        self._isSelected = val
    
    def set_color(self,color:tuple):
        """
        Set the color for the node
        NOTE: Color is triplet of rgb i.e. (255,255,255)
        """
        self._colorNode = color
    def get_label(self)->str:
        return self._label
    def setLocation(self,block:Block):
        """
        A location in grid is defined by the block
        Set location to a particular block position
        """
        self.pos = block.pos()
        self.id = block.id
    def handle_event(self,world, event,infoLabel):
        """
        Function handles the event happening in the world
        Allows to edit the label of node using keypress
        Once deleted function returns False
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the node rect.
            if self.pgObj.collidepoint(event.pos):
                helpText = "Use your keyboard to add/edit label to the node. Press DELETE to remove the node"
                #print(helpText)
                infoLabel.setValue(helpText)
                # Toggle the active variable.
                self._active = not self._active
                if self._active:
                    self._oldLabel = self._label
                else:
                    infoLabel.setValue(str(self))
                    self._isSelected = True
            else:
                self._active = False
            #Change the label to new value after checking validity
            if not self._active and (self._oldLabel is not None and self._oldLabel != self._label):
                #Try saving the new label
                self._saveNewLabel(self._oldLabel,world,infoLabel) #Discarding if no valid
                self._oldLabel = None
            # Change the current color of the input box.
            self._colorOutline = COLOR_ACTIVE if self._active else self._defaultOutlineColor
        
        if event.type == pygame.KEYDOWN:
            if self._active:
                if event.key == pygame.K_RETURN:
                    self._saveNewLabel(self._oldLabel,world,infoLabel) #Discarding if no valid
                    self._active = False
                    self._colorOutline = self._defaultOutlineColor
                elif event.key == pygame.K_BACKSPACE:
                    self._label = self._label[:-1]
                elif event.key == pygame.K_DELETE:
                    #delete the node
                    if not self._specialNodeStatus:
                        helpText = "Deleted {}".format(self)
                        #print(helpText)
                        infoLabel.setValue(helpText)
                        world.remove_node(self.id)
                        return False
                    else:
                        helpText = "Special node delete Permission Denied! NOTE: Special nodes like Start and Goal can't be deleted"
                        #print(helpText)
                        infoLabel.setValue(helpText)
                else:
                    self._label += event.unicode
                # Re-render the text.
                self._txt_surface = self._font.render(self._label, True, self._colorOutline)
        return True
    def _saveNewLabel(self,oldLabel,world,infoLabel):
            """
            Function saves the label only if the new label is valid else switch back to old label
            """
            #Label is already saved check whether we want to discard it or not
            #Deal with empty label
            if len(self._label)==0:
                helpText = "Node must have a label to identify!"
                #print(helpText)
                infoLabel.setValue(helpText)
                self._label = oldLabel
                return False
            #Deal with duplicate labels
            if self._label in world.getNodes().values():
                #print(helpText)
                infoLabel.setValue(helpText)
                self._label = oldLabel
                return False
            helpText = "Label changed from {} to {}".format(oldLabel,self._label)
            #print(helpText)
            infoLabel.setValue(helpText)
    
    def add_neighbour(self,node):
        """
        Adds a node as neighbour if it doesn't exists already
        """
        if node not in self._neighbourNodes:
            self._neighbourNodes.append(node)
    def remove_neighbour(self,node):
        """
        Remove the node from the neighbour if it exists
        """
        if node in self._neighbourNodes:
            self._neighbourNodes.remove(node)
    def get_neighbours(self)->list:
        """
        Returns list of neighbours in sorted order of the label
        """
        return sorted(self._neighbourNodes)
    def to_dict(self)->dict:
        """
        Returns the node parameters in dictionary format
        """
        node = {
            "block_id":str(self.id), #To initalise the parent
            "label":self._label,
            "colorOutline":str(self._defaultOutlineColor),
            "colorNode":str(self._colorNode),
            "pos":str(self.pos),
            "outlineWidth":self._outlineWidth,
            "specialNodeStatus":self._specialNodeStatus,
            #Edge updates the neighbour for the node need not to be included
        }
        return node
    def __eq__(self, label:str)->bool:
        """
        Equality between label of the node
        """
        #If the label is being edited check with oldLabel, this will help whether we want to discard the label or not
        if self._oldLabel is not None:
            if label==self._oldLabel:
                return True
            else:
                return False
        if label==self._label:
            return True
        else:
            return False
    def __lt__(self,value:str)->bool:
        """
        Label comparator
        """
        if self._label < value:
            return True
        else:
            return False
    
    def __gt__(self, value:str)->bool:
        """
        Label comparator
        """
        if self._label > value:
            return True
        else:
            return False

    def __ge__(self, value:str)->bool:
        """
        Label comparator
        """
        if self._label >= value:
            return True
        else:
            return False

    def __le__(self, value:str)->bool:
        """
        Label comparator
        """
        if self._label <= value:
            return True
        else:
            return False
    def __str__(self):
        return "<Node label = "+ self._label+" id = "+str(self.id)+">"

