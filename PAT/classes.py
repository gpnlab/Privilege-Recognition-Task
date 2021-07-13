import pygame
from pathlib import Path
import os

class PAT:
    def __init__(self):
        #fixed res for now (TODO)

        

        pygame.init()
        self.background = Background((800,800))
        self.clock = pygame.time.Clock()
        

    def main_loop(self):
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()

    def _handle_input(self):
        pass

    def _process_game_logic(self):
        events = pygame.event.get()

    def _draw(self):

        self.background.draw()
        
        pygame.display.flip()
        pygame.display.update()


class Background(pygame.sprite.Sprite):
    def __init__(self,res,image = "pacman.png",caption = "Privilege Recognition Task"):
        pygame.sprite.Sprite.__init__(self)
        self.res = res
        self.screen = pygame.display.set_mode(res)
        self.drawTo = pygame.Surface(res)
        self.image = self.imgLoad(image)

        pygame.display.set_caption(caption)

    def imgLoad(self,img):

        relPath = os.path.join(os.path.dirname(__file__),f"images/background/{img}")

        print(relPath)
        #pathLib fixes problems with differnet path conventions between linux and windows
        backImg = pygame.image.load(relPath).convert_alpha()
        backImg = pygame.transform.scale(backImg,self.res)
        return backImg
    
    def draw(self):
        #fills a black screen
        self.screen.fill((0,0,0))
        self.screen.blit(self.image,(0,0))

        




class GameObject(pygame.sprite.Sprite):
    def __init__(self,coord,imgName,velocity = 0,acceleration = 0):
        pygame.sprite.Sprite.__init__(self)

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


class Player(GameObject):
    

    #TODO: preload sprites for each eight direcitons
    def preload(self):
        return
    
    def __init__(self,coord):
        super.__init__(coord,"pacman.png")

    
    def update(self,horiz=1,vert=1):
        keys = pygame.key.get_pressed()
        xUpdate = 0
        yUpdate = 0
        
        #self.imgUpdate(keys)
        #when 8 directions added, this will update with corresponding sprite
        
    
        if keys[pygame.K_w]:
            yUpdate = vert*self.vel
        elif keys[pygame.K_s]:
            self.yVel = abs(self.yVel)
            yUpdate = vert*self.yVel
            
        if keys[pygame.K_a]:
            self.xVel = -abs(self.xVel)
            xUpdate = horiz*self.xVel  
        elif keys[pygame.K_d]:
            self.xVel = abs(self.xVel)
            xUpdate = horiz*self.xVel


        self.x += xUpdate
        self.y += yUpdate

class Coin:
    def __init__(self):
        pass