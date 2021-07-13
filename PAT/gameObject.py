#Justin Zhang's imported game object class
import pygame
from pathlib import Path

class GameObject(pygame.sprite.Sprite):
    def __init__(self,coord,imgName,velocity = 0,acceleration = 0):
        self.x,self.y = coord
        self.vel = velocity

        #should we have acceleration?
        self.acc = acceleration

        #add additional argument if resize is needed
        self.image = self.imgLoad(imgName)
        
        #store the dimension of the sprite
        self.xDim,self.yDim = self.image.get_rect().size

        #pygame uses Rect to detect collisions
        #everytime the object moves, we need to update the Rect coordinates (call setRect whenever object pos changes)
        self.setRect()

    #load all the images at once so it doesnt need to be done constantly
    #must be in the game image directory
    #default size will be 80x80
    @staticmethod
    def imgLoad(img,resizeDim = (80,80)):

        relPath = Path(f"images/objects/{img}")
        #pathLib fixes problems with differnet path conventions between linux and windows
        playerImg = pygame.image.load(relPath.name).convert_alpha()
        playerImg = pygame.transform.scale(playerImg,resizeDim)
        return playerImg

    

    def setRect(self):
        self.rect = pygame.Rect(self.x - self.xDim/2,self.y - self.yDim/2,
                                self.xDim,self.yDim)

    #direction is horizontal, then veritical
    def move(self,horizontal = False, vertical = False):
        self.x += horizontal * self.vel
        self.y += vertical * self.vel

        #TODO: check for out of bounds
        self.setRect()