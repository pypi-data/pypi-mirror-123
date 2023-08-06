"""
Search Algorithm Playground
===========================

Developer - Sritabh Priyadarshi(sobydanny@gmail.com)

About
Search Algorithm Playground is a python package to work with graph related algorithm, mainly dealing with different Artificial Intelligence Search alorithms.
The tool provides an user interface to work with the graphs and visualise the effect of algorithm on the graph while giving the freedom to programmer to make adjustments in the way they wants.
It also provides a way to save the graph in json format hence enabling the programmers to share the files and use different algorithm on same graph with ease.

Currently supports only undirected graphs
"""


import os
import pygame 
import json
from .world import World
from .Elements import Block,Node,Edge
from .config import *
from .UI import *


class PlayGround:
    """
    PlayGround class represents the ground which which consists of the world of blocks on which the graph is displayed or modified. 
    PlayGround class provide controls on the elements in the world like Edge and Nodes.
    
    ...

    Attribute
    ---------
    world: World
        World class object on which playground is available

    Methods
    -------
    fromfilename(filename:str)
        a classmethod which returns PlayGround class object initialised from values given in filename and returns the object
        filename: a json file name to which previously a playround is saved into

    addUIElement(element)
        Adds UI element to the playground
        NOTE: any UI element must contain draw() method which takes pygame screen as a parameter, the method will be called each time frame is drawn

    removeUIElement(element)
        Removes UI element from the playground

    onStart(func)
        Sets function to be executed when the start button is clicked
        func: function which will be executed when start is pressed
    
    delay(millisecond:int)
        Delays the program for given milliseconds
        Uses pygame.time.delay method
        Once the controls are taken away no other control would work on playground except exit
        NOTE: Using this delay function would allow to reflect changes on playground in delay mode better than instantaneous

    MoveGen(node:Node)
        Returns all the neighbours(in sorted order according to the label) of a node i.e. all the nodes which has edge between the given node
        node: A Node class object

    get_edge(nodeStart:Node,nodeEnd:Node)->Edge
        Returns an Edge class object between the node nodeStart and nodeEnd, if no edge exists returns None
        nodeStart: A Node class object
        nodeEnd: A Node class object

    getGoalNode()->Node
        Returns Node class object which is currenty set as a goal node for the playground

    getSartNode()->Node
        Returns Node class object which is currenty set as a start node for the playground

    setGoalNode(node:Node)
        Sets the given node as goal node for the PlayGround
        node: A Node class object

    setStartNode(node:Node)
        Sets the given node as goal node for the PlayGround
        node: A Node class object

    getAllNodes()->list
        Returns all nodes available in the world as a list

    getAllEdges()->list
        Returns list of all edges available in world

    getScreen()
        Returns a pygame window object which is the surface on which the elements are being drawn
        Useful in case more extra elements are needed to be drawn on the playground
    
    add_node(node: Node)
        Adds node to the world
        NOTE: node available in the world will be displayed on the playground screen

    add_edge(edge: Edge)
        Adds edge to the world
        NOTE: edge available in the world will be displayed on the playground screen
    
    remove_edge(edge:Edge)
        Removes edge from the world
    
    remove_node(node:Node)
        Removed node from the world
        
    saveWork(filename:str=None)
        Saves the playground with the given filename
        if no filename is provided, then playground will be saved with arbitrary filename

    showInfoText(text:str)
        To display informational texts on the playground right above the start button
        text: text to be displayed on the playground infoText area

    to_dict()->dict
        Returns Playrgound attributes as dictionary

    setTitle(title:str)
        Sets the title of the playground window
    
    run()
        runs the playground as an active window on which the frames are drawn
    


    """
    def __init__(self,world:World=None,saveToFile:str=None,weighted = False,startNode:Node=None,goalNode:Node=None,blocks_dimension = config["BLOCKS_DIMENSION"],block_size = config["BLOCK_SIZE"]):
        """
        Parameter
        ---------
        world : World
            a World class object on which the nodes/edges are drawn
            The screen size of the world determines the screensize of the playground window (default None).

        saveToFile : str
            name of the file with which the world(or graph) will be saved(file will be saved in json format) when the 'Save Work' button is pressed (default None).

        weighted : bool
            whether the edges that will be drawn on playround is weighted or not (default False).

        startNode : Node
            a node object of Node class which will be set as start node for the graph.
            NOTE: startNode is a special node which cannot be deleted from the playground(default None)
            if no value is provided then top left block contains the start node 'S'

        goalNode : Node
            a node object of Node class which will be set as start node for the graph.
            NOTE: goalNode is a special node which cannot be deleted from the playground(default None)
            if no value is provided then bottom right block contains the goal node 'G'

        blocks_dimension : tuple
            blocks_dimension represents number of blocks that will be generated in the world if world object is given as None(default (23,21))
            e.g (23,21) represents 23 rows and 21 columns

        block_size : int
            size of each block i.e. one side of the squared block (default 30)
        """
        pygame.init() #Initialise the pygame
        pygame.display.set_caption(config["TITLE"]) #set the title
        self.world = World(blocks_dimension,block_size,config["BOTTOM_PANEL_HEIGHT"],config["GRID_WIDTH"],config["BACKGROUND_COLOR"],config["GRID_COLOR"],config["MARGIN"]) if world is None else world
        self._isClicked = False
        self._running = False
        self._selectedNode = None #This is the node which is selected, will help in moving the nodes around
        #A Playground consist of a start node and a goal node always
        self._startNode = Node(self.world.getBlock((0,0)),'S',config["SPECIAL_NODE_BORDER_COLOR"],config["SPECIAL_NODE_COLOR"],3,True) if startNode is None else startNode
        self._goalNode = Node(self.world.getBlock((len(self.world.getBlocks())-1,len(self.world.getBlocks()[0])-1)),'G',config["SPECIAL_NODE_BORDER_COLOR"],config["SPECIAL_NODE_COLOR"],3,True) if goalNode is None else goalNode
        #Start and goal nodes are special nodes
        self._startNode._specialNodeStatus = True
        self._goalNode._specialNodeStatus = True
        #Add the nodes in the world
        self.world.add_node(self._startNode)
        self.world.add_node(self._goalNode)
        self._isDragging = False #True when clicked and mouse is dragging
        self._selectedEdge = None
        self._selectedBlock = None
        self.startButton = None
        self._saveWorkButton = None
        self._infoLabel = None #A label showing helpful texts
        self._onStartMethod = None #Method to be executed when start button is clicked
        self._isWeighted = weighted #Tells whether the playground will have weighted edge or not
        self._saveToFile = saveToFile
        self._createControlUI()
        self._UIElements = []
    
    @classmethod
    def fromfilename(cls,filename:str):
        """
        Parameter
        ---------
        filename : str
            a json file name to which previously a playround is saved into

        Returns a playground object initialised from the values given in filename
        """
        file = config["MY_WORK_DIR"]+filename
        pygame.init()
        try:
            with open(file,'r') as f:
                playGroundData = json.load(f)
                #Create world
                world = World.fromdict(dict(playGroundData['world']))
                startNodeID = tuple(eval(playGroundData['startNode']))
                goalNodeID = tuple(eval(playGroundData['goalNode']))
                isWeighted = playGroundData['isWeighted']
                #Create special nodes
        except FileNotFoundError:
            msg = "Unable to locate the file '{}' at '{}'\nMake sure the given filename is present at the given location".format(filename,file)
            raise FileNotFoundError(msg)
        return cls(world,filename,isWeighted,world.getNode(startNodeID),world.getNode(goalNodeID))
    def _createControlUI(self):
        """
        Generates UI elements for the controlls and info
        """
        height = int(config["BOTTOM_PANEL_HEIGHT"]/3)
        width = int(height*2)
        pos_x = int((self.world.win.get_size()[0]-width)/2)
        pos_y = (self.world.win.get_size()[1]-int((config["BOTTOM_PANEL_HEIGHT"])/2))
        self.startButton = Button((pos_x,pos_y),(width,height),config["BUTTON_COLOR_PRIMARY"],GRAY,"Start")
        label_size = 15
        pos_x += int(width/2)
        self._infoLabel = Label(config["INFO_LABEL_COLOR"],label_size,(pos_x,int(pos_y-label_size*1.5)))
        ##Secondary buttons
        height = int(config["BOTTOM_PANEL_HEIGHT"]/5.5)
        width = int(height*3)
        pos_x = int((width)/2)
        self._saveWorkButton = Button((pos_x,pos_y),(width,height),config["BUTTON_COLOR_SECONDARY"],GRAY,"Save work",0.7,0)


    def addUIElement(self,element):
        """
        Method adds UI element on the playground
        NOTE: any UI element must contain draw() method which takes pygame screen as a parameter
        """
        self._UIElements.append(element)
    def removeUIElement(self,element):
        """
        Removes UI element from the playground
        """
        if element in self._UIElements:
            self._UIElements.remove(element)

    def _drawUIElements(self):
        """
        Draws the frame for UI elements
        """
        self.startButton.draw(self.world.win)
        self._saveWorkButton.draw(self.world.win)
        self._infoLabel.draw(self.world.win)
        #Draw remaining UI elements
        for elements in self._UIElements:
            elements.draw(self.world.win)

    def _genLabel(self):
        """
        Function generates a label for a node which is not already there in the grid
        """
        def _nextLabel(label = ""):
            """
            A utility function to genLabel
            Counting with alphabet system
            Generates next label 
            """
            revL = [char for char in label[::-1]]
            n = len(revL)
            if n==0:
                return 'A'
            found = False
            for i in range(0,n):
                nextChar = chr(ord(revL[i])+1)
                if(nextChar <= 'Z'):
                    found = True
                    revL[i] = nextChar
                    break
                else:
                    revL[i] = 'A'
            if not found:
                revL.append('A')
            return ''.join(revL[::-1])
        label = "A"
        while label in self.world.getNodes().values():
            label = _nextLabel(label)
        return label

    def _getClickedEdge(self,pos)->Edge:
        """
        Returns an edge if the click position pos collides with any edge in the world
        """
        edges = self.world.getEdges()
        if edges:
            for edge in edges.values():
                if edge.collidePoint(pos):
                    return edge
        
        return None
    def _getClickedBlock(self,pos)->Block:
        """
        Returns a Block class object if the click position pos collides with any block in the world
        """

        blocks = self.world.getBlocks()
        if not blocks:
            raise ValueError("Blocks are not initialised")
        else:
            for row in blocks:
                for block in row:
                    if block.pgObj.collidepoint(pos):
                        return block
    def _dragNode(self,newBlock:Block):
        """
        Drags node to newBlock location

        Parameter
        ---------
        newBlock:Block
            A block in the world to which the selected node will be shifted
            NOTE: Selected node is the one which is selected after click on is made on it
        """
        if self._isClicked and self._selectedNode is not None and not newBlock.hasNode():
            #Update node location
            self.world.update_node_loc(self._selectedNode,newBlock)
            #print("Dragging to {}".format(newBlock))
    def _handleClicks(self,event):
        """
        Handles any click made on the screen
        """
        if self.startButton.isClicked(event.pos) and self._isClicked:
            #No more event monitoring till startMethod is finished
            self._isClicked = False
            self._start()
            return
        if self._saveWorkButton.isClicked(event.pos) and self._isClicked:
            self.saveWork(self._saveToFile)
            return
        

        block = self._getClickedBlock(event.pos)
        if block is not None and not block.hasNode() and not self._isDragging:
            #No selected node
            if self._selectedNode is not None:
                self._selectedNode.selected(False)
                self._selectedNode = None

            edge = self._getClickedEdge(event.pos)
            if edge is not None:
                if self._selectedEdge != edge:
                    #Show only different edge selected
                    self._infoLabel.setValue(str(edge))
                self._selectedEdge = edge
                if self._selectedBlock is not None:
                    self._selectedBlock.highlight(False)
                    self._selectedBlock = None
                return
        if block is not None:
            #Click is made on some block area

            self._dragNode(block)
            if not self._isDragging:
                if block.hasNode():
                    if self._selectedNode is None:
                        #Display infoText
                        #print(self.world.getNode(block.id))
                        self._infoLabel.setValue(str(self.world.getNode(block.id)))

                    if self._selectedBlock is not None:
                        self._selectedBlock.highlight(False)
                        self._selectedBlock = None

                    if self._selectedNode is not None and self._selectedNode != self.world.getNode(block.id):
                        self._selectedNode.selected(False) #Remove any selected node, probably help in creating no further edges without knowing
                        #If the nodes are not same then create an edge
                        if self.world.getNode(block.id) not in self._selectedNode.get_neighbours():
                            edge = Edge(self._selectedNode,self.world.getNode(block.id),edgeColor=config["NODE_BORDER_COLOR"],isWeighted=self._isWeighted)
                            ##Add new edge to the world
                            self.world.add_edge(edge)
                        self._selectedNode = None

                    elif self._selectedNode is not None:
                        pass
                    else:
                        self._selectedNode = self.world.getNode(block.id)
                        self._selectedNode.selected(True)

                else:
                    self._infoLabel.setValue(str(block))
                    #print(block)
                    if self._selectedBlock is not None:
                        self._selectedBlock.highlight(False) #Remove previous highlighted block
                        if block == self._selectedBlock:
                            self._selectedNode = Node(block,self._genLabel(),config["NODE_BORDER_COLOR"],config["NODE_COLOR"])
                            self.world.add_node(self._selectedNode) #Add the new node to world
                            self._selectedNode.selected(False)
                            self._selectedBlock = None
                        else:
                            self._selectedBlock = block
                            self._selectedBlock.highlight(True)
                    else:
                        self._selectedBlock = block
                        self._selectedBlock.highlight(True)
                    self._selectedNode = None
        else:
            #If the click is made somewhere outside a grid
            if self._selectedBlock is not None:
                self._selectedBlock.highlight(False)
                self._selectedBlock = None
            if self._selectedNode is not None and not self._isDragging:
                self._selectedNode.selected(False)
                self._selectedNode = None
            self._infoLabel.setValue("") #Blank info text


    def _eventHandler(self,event):
        """
        Handles all the events
        """
        if self._selectedNode is not None:
            if not self._selectedNode.handle_event(self.world,event,self._infoLabel):
                self._selectedNode.selected(False)
                self._selectedNode = None
        elif self._selectedEdge is not None:
            if not self._selectedEdge.handle_event(self.world,event,self._infoLabel):
                self._selectedEdge = None
        if event.type == pygame.MOUSEBUTTONDOWN:
            self._isClicked = True
            self._handleClicks(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            self._isClicked = False
            self._isDragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self._isClicked:
                self._isDragging = True
                self._handleClicks(event)
            else:
                self._isDragging = False
    
    def onStart(self,func):
        """
        Sets function to be executed when the start button is clicked

        Parameter
        ---------
        func: function which will be executed when start is pressed
        """
        self._onStartMethod = func
    def _start(self):
        """
        Function executes the method which is set as onStart
        """
        if self._onStartMethod is not None:
            self.saveWork("cached.json")
            #self._infoLabel.setValue("Running Algorithm...") # info text
            self._onStartMethod()
            #self._infoLabel.setValue("Finished Running") # info text
        else:
            self._infoLabel.setValue("No start function is set")
    def delay(self,millisecond:int):
        """
        Delays the program for given milliseconds
        Uses pygame.time.delay method
        Once the controls are taken away no other control would work on playground except exit
        NOTE: Using this delay function would allow to reflect changes on playground in delay mode better than instantaneous
        """
        pygame.time.delay(millisecond)
        self._drawScenary() #Draw scenary even if the program is being paused
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:
                pygame.quit()
                print("Killed")
                exit()
    def _drawScenary(self):
        """
        Draw the elements of the world and world along with it
        NOTE: If the control is taken away for a while, make sure to drawScenary to reflect the changes in the world
        """
        self.world.create_grids()
        self._drawUIElements()
        pygame.display.update()
        

    def MoveGen(self,node:Node)->list:
        """
        Returns a list of neighbouring nodes in sorted order of their label

        Parameter
        ---------
        node:Node
            A Node class object
        """
        return node.get_neighbours()
    def get_edge(self,nodeStart:Node,nodeEnd:Node)->Edge:
        """
        Returns an edge between the two nodes if it exists

        Parameter
        ---------
        nodeStart:Node
            A Node class object

        nodeEnd:Node
            A Node class object
        """
        return self.world.getEdge(nodeStart.id,nodeEnd.id)
    def getAllNodes(self)->list:
        """
        Returns all node available in the world in sorted order of their labels
        """
        return sorted(list(self.world.getNodes().values()))

    def getAllEdges(self)->list:
        """
        Returns list of all edges available in world
        """
        return list(self.world.getEdges().values())

    def remove_edge(self, edge:Edge):
        """
        Remove edge from the world

        Parameter
        ---------
        edge:Edge
            An Edge class object to be removed from world
        """
        self.world.remove_edge(edge)

    def remove_node(self, node:Node):
        """
        Remove node from the world

        Parameter
        ---------
        node:Node
            A node class object to be removed from the world
        """
        self.world.remove_node(node.id)
    def getGoalNode(self)->Node:
        """
        Returns Node class object which is currenty set as a goal node for the playground
        """
        return self._goalNode
    
    def getStartNode(self)->Node:
        """
        Returns Node class object which is currenty set as a start node for the playground
        """
        return self._startNode
    def setGoalNode(self,node:Node):
        """
        Sets the given node as goal node for the PlayGround
        NOTE: At any moment playground supports only on goal node

        Parameter
        ---------
        node:Node
            A Node class object
        """
        self._goalNode._specialNodeStatus = False
        self._goalNode = node
        self._goalNode._specialNodeStatus = True
    def setStartNode(self,node:Node):
        """
        Sets the given node as goal node for the PlayGround
        NOTE: At any time only one start node can be present

        node:Node
            A Node class object
        """
        self._startNode._specialNodeStatus = False #Remove the previous node from special category
        self._startNode = node
        self._startNode._specialNodeStatus = True #Set the new node as special


    def getScreen(self):
        """
        Returns a pygame window object which is the surface on which the elements are being drawn
        Useful in case more extra elements are needed to be drawn on the playground
        """
        return self.world.win
    def add_node(self,node:Node):
        """
        Adds node to the world
        NOTE: node available in the world will be displayed on the playground screen
        """
        self.world.add_node(node)
    def add_edge(self,e:Edge):
        """
        Adds edge to the world
        NOTE: edge available in the world will be displayed on the playground screen
        """
        self.world.add_edge(e)
    def saveWork(self,filename:str=None):
        """
        Saves the current graph to a file with given filename
        If no filename is provided files are saved with some meaningful name
        """
        from datetime import datetime as dt
        # Getting current date and time
        now = dt.now()
        if filename is None and self._saveToFile is None:
            filename = "Graph "+now.strftime("%d-%m-%Y %H:%M:%S")+".json" #Save data with current date and time
        elif filename is None:
            filename = self._saveToFile
        location = os.path.join(os.getcwd(),config["MY_WORK_DIR"])
        file = os.path.join(location, filename)
        try:
            with open(file,'w') as f:
                val = str(self.to_dict())
                f.write(json.dumps(self.to_dict(), indent=4))
                infoText = "Work saved at: {}".format(file)
                self._infoLabel.setValue(infoText)
                #print(infoText)
        except FileNotFoundError:
            #Directory not found
            os.mkdir(location) #Create the directory
            self.saveWork(filename)

    def showInfoText(self,text:str):
        """
        To display informational texts on the playground right above the start button
        
        Parameter
        ---------
        text : str
            text to be displayed on the playground infoText area
        """
        self._infoLabel.setValue(text)
    def to_dict(self)->dict:
        """
        Returns attributes and values as dictionary
        """
        playground = {
            'world':self.world.to_dict(),
            'startNode':str(self._startNode.id),
            'goalNode':str(self._goalNode.id),
            'isWeighted':self._isWeighted
        }
        return playground
    def setTitle(self,title:str):
        """
        Sets title of the playground window
        """
        pygame.display.set_caption(title)
    def run(self):
        """
        Start the playground to play with
        """
        clock = pygame.time.Clock()
        cwd = os.path.dirname(os.path.realpath(__file__))
        icon_path = os.path.join(cwd,'img/icon.png')
        icon = pygame.image.load(icon_path)
        pygame.display.set_icon(icon)
        self.__running = True
        print("Search Algorithm PlayGround Tool created by Sritabh Priyadarshi using pygame.\nVisit https://github.com/SobyDamn/SearchAlgorithmPlayground for more info.")
        while self.__running:
            self._drawScenary()
            for event in pygame.event.get():  
                if event.type == pygame.QUIT:  
                    self.__running = False
                else:
                    self._eventHandler(event)
            clock.tick(60)
        pygame.quit()