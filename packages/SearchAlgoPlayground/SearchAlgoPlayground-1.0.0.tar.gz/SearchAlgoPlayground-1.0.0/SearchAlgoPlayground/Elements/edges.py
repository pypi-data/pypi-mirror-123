from .nodes import *
import pygame
from SearchAlgoPlayground.config import config
import math

COLOR_ACTIVE = config["ELEMENT_ACTIVE_COLOR"]
class Edge:
    """
    An edge class represents an edge between 2 nodes
    ...

    Attribute
    ---------
    pgObj
        A pygame rect object
    
    Methods
    -------
    handle_event(world:World,event,infoLabel)
        Internal method to handle the pygame events

    set_color(color:tuple)
        Sets color of the edge
        color:tuple - A rgb value of the form (r,g,b)
    
    collidePoint(clickPoint,offeset=5)
        Returns true if the given click point is inside the offset value on edge

    draw_edge(screen)
        Draws edge on the screen
        screen - A pygame window

    getNodes()->tuple
        Returns the pair of node which the edge is connecting

    get_weight()->int
        Returns the weight of the edge

    to_dict()->dict
        Returns the object details its attributes and value as dictionary

    """
    def __init__(self,nodeStart:Node,nodeEnd:Node,isWeighted:bool = False,weight = 0,edgeColor = config["NODE_BORDER_COLOR"],edgeWidth = 3):
        """
        Parameters
        ----------
        nodeStart:Node
            A Node class object which represents the starting node of the edge

        nodeEnd:Node
            A Node class object which represents the ending node of the edge

        isWeighted:bool
            Whether the edge drawn between the node has weight or not, default False

        weight:int
            Wieght of the edge, default 0

        edgeColor:tuple
            A rgb value of the form (r,g,b) which represents the color of the edge, default value `NODE_BORDER_COLOR`
        
        edgeWidth:int
            Width of the edge, default 3
        """
        self._edgeColor = edgeColor
        self._defaultEdgeColor = edgeColor
        self._edgeWidth = edgeWidth
        self._weight = weight
        self._weightLabel = str(weight)
        self._nodeStart = nodeStart #Start of the edge
        self._nodeEnd = nodeEnd #End of the edge
        self._isWeighted = isWeighted

        #Inform the nodes that edge is created
        self._nodeStart.add_neighbour(self._nodeEnd) #Add neighbours
        self._nodeEnd.add_neighbour(self._nodeStart) #Add neighbour

        self._font = pygame.font.Font(None, int(min(30,self._nodeStart.size*0.80)))
        self._txt_surface = self._font.render(self._weightLabel, True, self._edgeColor)

        self._active = False #An edge is active if selected
        self._oldWeight = None
        self.pgObj = None
    
    def handle_event(self, world,event,infoLabel):
        """
        Function handles the event happening in the world with the node
        Allows to set weight or delete an Edge
        Once an edge deleted function returns False
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the edge rect.
            if self.collidePoint(event.pos):
                helpText = ""
                if self._isWeighted:
                    helpText +="Use your keyboard to add/edit weight of the edge"
                    #print(helpText)
                helpText += "Press DELETE to remove the edge"
                infoLabel.setValue(helpText)
                #print(helpText)
                # Toggle the active variable.
                self._active = not self._active
                if self._active:
                    self._oldWeight = self._weightLabel
                else:
                    infoLabel.setValue("")
            else:
                self._active = False
            
            #Change the label to new value after checking validity
            if not self._active and (self._oldWeight is not None and self._oldWeight != self._weightLabel):
                #Try saving the new label
                self._saveNewLabel(self._oldWeight,infoLabel) #Discarding if not valid
                self._oldWeight = None
            # Change the current color of the input box.
            self._edgeColor = COLOR_ACTIVE if self._active else self._defaultEdgeColor
        
        if event.type == pygame.KEYDOWN:
            if self._active:
                if event.key == pygame.K_RETURN:
                    self._saveNewLabel(self._oldWeight,infoLabel) #Discarding if no valid
                    self._active = False
                    self._edgeColor = self._defaultEdgeColor
                elif event.key == pygame.K_BACKSPACE:
                    self._weightLabel = self._weightLabel[:-1]
                elif event.key == pygame.K_DELETE:
                    #delete the node
                    helpText = "Deleted {}".format(self)
                    infoLabel.setValue(helpText)
                    #print(helpText)
                    world.remove_edge(self)
                    return False
                else:
                    self._weightLabel += event.unicode
                # Re-render the text.
                self._txt_surface = self._font.render(self._weightLabel, True, self._edgeColor)
        return True
    def _saveNewLabel(self,oldLabel,infoLabel):
        """
        Discard the value if it's invalid else saves the value
        """
        #Deal with empty string
        if len(self._weightLabel)==0:
            helpText = "Edge must contain a weight"
            infoLabel.setValue(helpText)
            #print(helpText)
            self._weightLabel = oldLabel
            return False
        try:
            weight = int(self._weightLabel)
            self._weightLabel = str(weight)
            self._weight = weight
            helpText = "{} new weight - {}".format(self,self._weightLabel)
            infoLabel.setValue(helpText)
            #print(helpText)
            return True
        except ValueError:
            helpText = "Edge weight value must be an integer"
            infoLabel.setValue(helpText)
            #print(helpText)
            self._weightLabel = oldLabel
            return False
    def set_color(self,color:tuple):
        """
        Sets the color of the edge
        """
        self._edgeColor = color
    def collidePoint(self,clickPoint,offset=5):
        """
        Returns true if the click point is inside offset limit of the edge
        """
        if self.pgObj.collidepoint(clickPoint) and self._distance_point_line(clickPoint) < offset:
            return True
        else:
            return False
    def _distance_point_line(self,pt):
        """
        Returns normal distance at which the point pt is clicked from the line
        """
        l1 = self._nodeStart.pos
        l2 = self._nodeEnd.pos
        NV = pygame.math.Vector2(l1[1] - l2[1], l2[0] - l1[0])
        LP = pygame.math.Vector2(l1)
        P = pygame.math.Vector2(pt)
        return abs(NV.normalize().dot(P -LP))

    def draw_edge(self,screen):
        self.pgObj = pygame.draw.line(screen,self._edgeColor,self._nodeStart.pos,self._nodeEnd.pos,self._edgeWidth)
        if self._isWeighted:
            #A weighted edge will have a label representing it's weight
            self._set_label(self._weightLabel,screen)

    def getNodes(self)->tuple:
        """
        Returns the nodes the edge is connecting
        """
        return (self._nodeStart,self._nodeEnd)

    def get_weight(self)->int:
        """
        Returns the weight of the edge
        """
        return self._weight if self._isWeighted else 0

    def _set_label(self,label,screen,offset = 0.4):
        """
        Sets the label of weight to the edge
        height above the edge the label is placed is offset*nodeSize
        """
        h = self._nodeEnd.size*offset
        xc,yc = self.pgObj.center
        x1,y1 = min(self._nodeStart.pos,self._nodeEnd.pos)
        dist_sq = (xc-x1)**2 + (yc-y1)**2
        mid_dist = math.sqrt(dist_sq)
        phi = math.atan((h)/mid_dist)
        theta = math.pi/2 if xc-x1==0 else math.atan((yc-y1)/(xc-x1))
        hyp = math.sqrt((h)**2 + (mid_dist)**2)
        (x,y) = (x1+int(hyp*math.cos(theta+phi)),y1+int(hyp*math.sin(theta+phi)))
        text = self._font.render(label, True, self._edgeColor)
        text_rect = text.get_rect(center = (x,y))
        screen.blit(text, text_rect)

    def to_dict(self)->dict:
        """
        Returns edge parameter and it's value as dictionary
        """
        edge = {
            "nodeStart":str(self._nodeStart.id),
            "nodeEnd":str(self._nodeEnd.id),
            "edgeColor":str(self._edgeColor),
            "edgeWidth":self._edgeWidth,
            "weight":self._weight,
            "isWeighted":self._isWeighted
        }
        return edge
    def __str__(self):
        return "<Edge {} - {}>".format(self._nodeStart.get_label(),self._nodeEnd.get_label())
