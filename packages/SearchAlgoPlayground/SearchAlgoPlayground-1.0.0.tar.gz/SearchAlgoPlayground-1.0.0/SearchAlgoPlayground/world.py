import pygame
from .Elements import Block,Node,Edge


class World:
    """
    A World class represents the world for the playground which is responsible for Maintaining Node,Edge and Block of the playground

    Methods
    -------
    fromdict(datadict:dict)
        A classmethod to create World class object from a dictionary
        NOTE:The dictionary must be of the same form returned by to_dict() method of the class

    create_grids()
        Generates grids if not generated in the world, if the gird is already availbale then it redraws them

    add_node(node:Node)
        Adds nodes to the world
        NOTE: To make the node visible on playground window it must be include in the world

    remove_node(node:Node)
        Removes nodes from the world
        NOTE: If nodes are not available in the world it will no longer visible on playground window

    update_node_loc(node:Node,newBlock:Block)
        Updates the location of the node to newBlock location and removes it from previous block
        node:Node - A Node class object which needs to be updated
        newBlock:Block - A Block class object to which the node is require to move to

    getEdges()->dict
        Returns all the available edges in the world as dictionary with key as the node pairs ids
        e.g ((1,1),(1,5)) is the key for an edge between the node with id (1,1) and (1,5)
        NOTE: The id represents position in the 2D matrix of the block

    add_edge(e:Edge)
        Adds edge to the world, edge added to the world will be visible on Playground window
        NOTE: Edges are added with the key of the end node ids e.g. ((1,1),(1,5)) is the key for an edge between the node with id (1,1) and (1,5)

    remove_edge(e:Edge)
        Removes the edge from the world. The edge removed from the world will no longer be visible on the Playground window

    getEdge(startNodeID:tuple,endNodeID:tuple)->Edge
        Returns edge between startNodeID and endNodeID if there exists an edge else returns None
        startNodeID:tuple - id of the node which has edge with the other node we're looking for
        endNodeID:tuple - id of the node which has edge with the other node we're looking for
    
    getNodes()->dict
        Returns the dictionary of all the nodes available in the world
        Key of is the id of the node
    
    getNode(key:tuple)->Node
        Returns node with given key, returns None if the node doesn't exists
        key:tuple - id of the node we are looking for,  location in the grid or 2D array.

    getBlock(id)->Block
        Returns block at the given id.
        id:tuple - Index Location in 2D matrix
    
    get_dimension()->tuple
        Returns dimension of the world as tuple of (rows,col)

    to_dict()->dict
        returns the object details with all attribute and values as dictionary


    """
    def __init__(self,blocks_dimension:tuple,block_size:int,bottom_panel_size:int,grid_width:int = 1,background_color:tuple=(255,255,255),gird_color:tuple = ((232, 232, 232)),margin=10):
        """
        Parameters
        ----------
        blocks_dimension : tuple
            blocks_dimension represents number of blocks that will be generated in the world
            e.g (23,21) represents 23 rows and 21 columns

        block_size : int
            size of each block i.e. one side of the squared block
        
        bottom_panel_size:int
            height of the bottom panel on which buttons and other UI element will be drawn
            min allowed 180

        grid_width:int
            Width of the grids

        background_color:tuple
            A rgb value type of the form (r,g,b) to set color for the background of the world default (255,255,255)
            
        gird_color:tuple
            A rgb value type of the form (r,g,b) to set color for the blocks border of the world default (232, 232, 232)

        margin:int
            Margin from the edges of the playground window, minimum value allowed is 10, default 10
        
        """
        self._rows,self._cols = blocks_dimension
        self._background = background_color
        self._available_blocks = None
        self._margin = max(margin,10)
        self._bottom_panel_size = bottom_panel_size
        self._screen_size = self._calc_screen_size(blocks_dimension,block_size,self._bottom_panel_size)
        self._width,self._height = self._screen_size[0],self._screen_size[1]
        self.win = pygame.display.set_mode((self._width,self._height))
        self._grid_width = grid_width
        self._block_size = block_size
        self._grid_color = gird_color
        self._blocksGenerated = False
        self._available_nodes = {} #Type dictionary where block id is a key
        self._available_edges = {}
        self.create_grids() #Initialise grid always as soon as world is created
    @classmethod
    def fromdict(cls,datadict:dict):
        """
        Returns a world object with initialised with values given in dictionary
        """
        world = cls(tuple(eval(datadict['blocks_dimension'])),int(datadict['block_size']),int(datadict['bottom_panel_size']),int(datadict['grid_width']),tuple(eval(datadict['background_color'])),eval(datadict['grid_color']),int(datadict['margin']))
        world.create_grids() #Initialise the blocks
        #Create nodes
        available_nodes = datadict['available_nodes']
        for nodeKey in available_nodes:
            node_dict = available_nodes[nodeKey]
            #Get block
            block = world.getBlock(eval(nodeKey))
            node = Node(block,node_dict['label'],tuple(eval(node_dict['colorOutline'])),tuple(eval(node_dict['colorNode'])),node_dict['outlineWidth'],node_dict['specialNodeStatus'])
            world.add_node(node)
        available_edges = datadict['available_edges']
        for edgeKey in available_edges:
            edge_dict = available_edges[edgeKey]
            nodeStart = world.getNode(tuple(eval(edge_dict['nodeStart'])))
            nodeEnd = world.getNode(tuple(eval(edge_dict['nodeEnd'])))
            edge = Edge(nodeStart,nodeEnd,edge_dict['isWeighted'],edge_dict['weight'],tuple(eval(edge_dict['edgeColor'])),int(edge_dict['edgeWidth']))
            world.add_edge(edge)
        return world
    

    def _calc_screen_size(self,blocks_dimension,block_size,bottom_panel_size):
        """
        Returns size of the screen
        """
        screen_width = block_size*self._cols + 2*self._margin
        screen_height = block_size*self._rows + self._margin + max(bottom_panel_size,180)
        return (screen_width,screen_height)
    def create_grids(self):
        self.win.fill(self._background)
        """
        Create grid of blocks
        """
        if self._blocksGenerated:
            self._redraw_world()
            return #if blocks are generated no regenerating required just redraw
        
        total_cols = self._cols
        total_rows = self._rows
        start_x = self._margin
        start_y = self._margin
        for col in range(0,total_cols):
            cols = []
            for row in range(0,total_rows):
                x = start_x+self._block_size*col
                y = start_y+self._block_size*row
                id = (col,row)
                block = Block(x,y,self._block_size,id,self._grid_color,self._grid_width)
                block.draw_block(self.win)
                cols.append(block)
            if not self._blocksGenerated:
                self._add_blocks(cols)
        self._blocksGenerated = True
    def _redraw_world(self):
        """
        Redraws frames of the world
        all the element on the world must be redrawn
        """
        if self._available_blocks is None:
            raise ValueError("Block are not available")
        else:
            for row in self._available_blocks:
                for block in row:
                    block.draw_block(self.win)
        #Draw edges
        if self._available_edges is not None:
            for edge in self._available_edges.values():
                edge.draw_edge(self.win)
        #Draw nodes
        if self._available_nodes is not None:
            for node in self._available_nodes.values():
                node.draw_block(self.win)
    def add_node(self,node:Node):
        """
        Add nodes to the world
        """
        #Dictionary is updated each time the node is moved in the grid
        if self._available_nodes is None:
            self._available_nodes = {}
        if not node.id in self._available_nodes:
            self._available_nodes[node.id] = node
        else:
            #print("{} already exists at thAT block location".format(node))
            pass

        #Now the block contains a node over it
        block = self.getBlock(node.id)
        block.setHasNode(True)
    
    def remove_node(self,id:tuple,forUpdate=False):
        """
        Deletes node with id as key from world
        """
        try:
            if not forUpdate:
                self._removeEdges(self._available_nodes[id])
            del self._available_nodes[id]
        except KeyError:
            print("World: Deleting a node which doesn't exists")

        #Now the block doesn't contains a node over it
        block = self.getBlock(id)
        block.setHasNode(False)
    def update_node_loc(self,node:Node,newBlock:Block):
        """
        Updates the location of a node to new block
        """
        #Deletes from last location and add to new location
        oldLoc = node.id #oldLoc id to update the edge dict
        self.remove_node(node.id,True)#remove from current block for update purpose
        node.setLocation(newBlock) #Update the location of the node
        self._updateEdges(node,oldLoc) #Update location in dictionary

        self.add_node(node) #Add updated location block
    def getEdges(self):
        """
        Returns list of edges
        """
        return self._available_edges
    def add_edge(self,e:Edge):
        """
        Add edge to the world
        """
        #FIX-ME Make it work for directed graph as well
        (node1_id,node2_id) = (e.getNodes()[0].id,e.getNodes()[1].id)
        key = tuple(sorted((node1_id,node2_id)))#The key of the edge is nodes in sorted ascending order
        if self._available_edges is None:
            self._available_edges = {}
        if not key in self._available_edges:
            self._available_edges[key] = e
        else:
            print("World: Edge between the nodes {} - {} already exists".format(e.getNodes()[0],e.getNodes()[1]))
            pass
    def remove_edge(self,edge:Edge):
        """
        Removes the edge
        """
        try:
            (sNode,eNode) = edge.getNodes()
            key = tuple(sorted((sNode.id,eNode.id)))#The key of the edge is nodes in sorted ascending order
            sNode.remove_neighbour(eNode)
            eNode.remove_neighbour(sNode)
            del self._available_edges[key] 
        except KeyError:
            print("World: Edge to be deleted Doesn't exists {}".format(key))
    def _removeEdges(self,node:Node):
        """
        Function removes all the edges from the given node
        """
        for endNode in node.get_neighbours():
            self.remove_edge(self.getEdge(node.id,endNode.id))
    def _updateEdges(self,node:Node,oldLoc:tuple):
        """
        Updates the edge for avaialable_edges
        """
        for endNode in node.get_neighbours():
            edge = self.getEdge(oldLoc,endNode.id)
            key = tuple(sorted((oldLoc,endNode.id)))#The key of the edge is nodes in sorted ascending order
            try:
                del self._available_edges[key]
                self.add_edge(edge)
            except KeyError:
                print("World: Error in updating the edge to world")
    
    def getEdge(self,startNodeID:tuple,endNodeID:tuple)->Edge:
        """
        Returns edge between startNodeID and endNodeID if there exists an edge else returns None
        """
        key = tuple(sorted((startNodeID,endNodeID)))
        if key in self._available_edges:
            return self._available_edges[key]
        else:
            return None
    def getNodes(self):
        """
        Returns available nodes in the world
        Dictionary of nodes id as key
        """
        return self._available_nodes
    def getNode(self,key:tuple):
        """
        key is tuple of location in the grid or 2D array
        Returns the node
        """
        if key in self._available_nodes:
            return self._available_nodes[key]
        else:
            return None
    def getBlock(self,id:tuple):
        """
        Returns block associated with the id in the grid
        id - location in 2D matrix
        """
        x,y = id
        try:
            return self._available_blocks[x][y]
        except IndexError:
            raise IndexError("Provided id '{}' doesn't contain any block".format(id))
    def getBlocks(self)->dict:
        """
        Returns all the available blocks in the world as dict
        """
        return self._available_blocks
    def _add_blocks(self,col):
        """
        Method decides whether to add the row or not based on whether we have already added the node or not
        """
        if self._available_blocks is None:
            self._available_blocks = []
        self._available_blocks.append(col)
    
    def get_dimension(self)->tuple:
        """
        Returns dimension of the world as tuple of form (rows,cols)
        """
        return (self._rows,self._cols)

    def to_dict(self)->dict:
        """
        Returns world information as dictionary
        """
        world = {
            "blocks_dimension":str((self._rows,self._cols)),
            "background_color":str(self._background),
            "bottom_panel_size":self._bottom_panel_size,
            "available_blocks":{},
            "margin":self._margin,
            "screen_size":str(self._screen_size),
            "block_size":self._block_size,
            "grid_color":str(self._grid_color),
            "grid_width":self._grid_width,
            "available_nodes":{},
            "available_edges":{},
        }
        for edgeKey in self._available_edges:
            world["available_edges"][str(edgeKey)] = self._available_edges[edgeKey].to_dict()
        for nodeKey in self._available_nodes:
            world["available_nodes"][str(nodeKey)] = self._available_nodes[nodeKey].to_dict()
        return world
    def __str__(self):
        details =   "World Details\nScreen Size - "+str(self._width)+"x"+str(self._height)+"\n"+"Total Blocks - "+str(self._rows)+"x"+str(self._cols)+"\n"
        return details

