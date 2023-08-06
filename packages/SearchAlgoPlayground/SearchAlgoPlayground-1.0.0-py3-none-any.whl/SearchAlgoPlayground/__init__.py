import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from .UI import *
from .Elements import Block,Node,Edge
from .playground import PlayGround
from .world import World
from .config import config