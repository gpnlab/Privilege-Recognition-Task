import pygame
import math
from gameObject import *

class Player(GameObject):
    

    #TODO: preload sprites for each eight direcitons
    def preload(self):
    
    def __init__(self,coord):
        super.__init__(coord,"pacman.png")