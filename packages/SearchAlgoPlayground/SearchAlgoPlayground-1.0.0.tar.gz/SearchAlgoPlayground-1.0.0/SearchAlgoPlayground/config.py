###Colors###
DARK_PURPLE = (3, 3, 66)
PURPLE = (136, 137, 219)
GRAY = (232, 232, 232)
DARK_GRAY = (130, 130, 130)
LIGHT_BLUE = (217, 247, 255)
BROWN = (61, 51, 23)
WHITE = (255,255,255)
BLUE = (28,134,238)
BLACK = (0,0,0)
GREEN = (151, 240, 175)
RED = (255, 120, 120)
CYAN = (0, 255, 255)
YELLOW = (217, 210, 74)


config = {
    "TITLE":"Algo PlayGround",               #Title of the playground window
    "BLOCKS_DIMENSION":(21,23),              #ROWS,COLUMNS
    "BLOCK_SIZE":30,                         #Size of each block i.e. sides
    "BOTTOM_PANEL_HEIGHT":200,               #Size of bottom panel for control
    "MARGIN":15,                             #Margin between sides and the grid 
    "GRID_WIDTH":1,                          #Width of the boundary of the block
    "BACKGROUND_COLOR":WHITE,                #Color of the background of the world
    "GRID_COLOR":GRAY,                       #Block boundary color
    "HIGHLIGHT_COLOR":DARK_GRAY,             #Highlighting color
    "BUTTON_COLOR_PRIMARY":BROWN,            #Color for the button larger
    "BUTTON_COLOR_SECONDARY": PURPLE,        #color for the smaller button
    "INFO_LABEL_COLOR":DARK_GRAY,            #color for the info text
    "NODE_COLOR":GRAY,                       #color of the node
    "NODE_BORDER_COLOR":BLACK,               #color of the border of node
    "SPECIAL_NODE_BORDER_COLOR": DARK_PURPLE,#Special node border color
    "SPECIAL_NODE_COLOR":GREEN,              #special node color
    "SELECTED_NODE_COLOR" : RED,             #color of the node selected
    "ELEMENT_ACTIVE_COLOR":BLUE,             #Element selected by user is considered as active to the playground
    "MY_WORK_DIR": "MyGraph/"                #Directory in which the work is saved
}