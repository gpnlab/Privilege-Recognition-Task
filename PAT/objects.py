import pygame
import math
import random
from os import path, stat

class GameObject(pygame.sprite.Sprite):
    def __init__(self,background,group,coord,imgName,velocity = .5,acceleration = 0,resize = (40,40)):
        pygame.sprite.Sprite.__init__(self)

        self.group = group 
        self.group.add(self)
        #screen tells us where to draw to
        self.bg = background
        self.screen = background.screen


        self.x,self.y = coord
        self.vel = velocity

        #should we have acceleration?
        self.acc = acceleration

        #add additional argument if resize is needed
        self.image = self.imgLoad(imgName,resize)


        
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

        relPath = path.join(path.dirname(__file__),f"images/objects/{img}")
        
        playerImg = pygame.image.load(relPath).convert_alpha()
        playerImg = pygame.transform.scale(playerImg,resizeDim)
        return playerImg

    

    def setRect(self):
        self.rect = pygame.Rect(self.x - self.xDim/2,self.y - self.yDim/2,
                                self.xDim,self.yDim)

    #direction is horizontal, then veritical
    def move(self,horizontal = 0, vertical = 0):
        
        
        self.x += horizontal * self.vel
        self.y += vertical * self.vel

        #check oob
        if (self.x < 0 + self.xDim // 2 or self.x > self.bg.res[0] - self.xDim // 2):
            self.x -= horizontal * self.vel
        if (self.y < 0 + self.yDim // 2 or self.y > self.bg.res[1] - self.yDim // 2):
            self.y -= vertical * self.vel


        self.setRect()
    
    def draw(self):
        self.screen.blit(self.image,(self.x,self.y))


#Agent as in player/enemies
class Agent(GameObject):

    #TODO: preload sprites for each eight direcitons
    def preload(self):
        return
    
    def __init__(self,name,background,group,coord,velocity,imgName = "placeholder.png"):
        super().__init__(background,group,coord,imgName,velocity)
        self.name = name
        self.coins = 0

    
class Player(Agent):
    def __init__(self,background,group,coord,velocity,imgName = "placeholder.png"):
        super().__init__("player",background,group,coord,velocity,imgName)

    def getInput(self,horiz=1,vert=1):
        keys = pygame.key.get_pressed()
        
        #self.imgUpdate(keys)
        #when 8 directions added, this will update with corresponding sprite
        
        if keys[pygame.K_w]:
            self.move(0,-1)
        elif keys[pygame.K_s]:
            self.move(0,1)
            
        if keys[pygame.K_a]:
            self.move(-1,0)  
        elif keys[pygame.K_d]:
            self.move(1,0)


#is calling them enemies a form of bias within itself hmmmmmm
#"OtherPlayers" doesn't really roll off the tongue
class Enemy(Agent):
    #need to pass in coin group for AI to find nearest coin
    def __init__(self,name,background,group,cGroup,coord,velocity,imgName = "placeholder.png"):
        super().__init__(name,background,group,coord,velocity,imgName)
        self.coinGroup = cGroup
        
        #3 states:
        #0 - optimal path towards closest coin
        #1 - random direction
        #2 - stay still
        #transfer probabilities will be listed in the readme
        self.state = 0

        #probability matrix for transfering
        self.pMatrix = [[8,1,1],[7,1,2],[7,1,2]]

    def dist(self,c1,c2):
        (x1,y1),(x2,y2) = c1,c2
        return math.sqrt ((x1 - x2) ** 2 + (y1 - y2) ** 2)


    #loop through everything in coin group
    def getNearestCoinCoord(self):
        #default "max" distance
        bestDist = self.bg.res[0]
        for coin in self.coinGroup:
            currDist = self.dist((self.x,self.y),(coin.x,coin.y))

            if currDist < bestDist:
                bestCoin = coin
                bestDist = currDist

        return (bestCoin.x,bestCoin.y)


    #optimal movement toward nearest coin
    #will have to normalize vector to the velocity of the enemy (yay linear algebra)
    def optMove(self):
        (cX,cY) = self.getNearestCoinCoord()
        d = self.dist((cX,cY),(self.x,self.y))

        #normalize
        xMov = self.vel * (cX - self.x) / d
        yMov = self.vel * (self.y - cY) / d

        self.move(xMov,-yMov)
    
    def getRandMove(self):
        self.randX = random.uniform(-1,1)
        self.randY = math.sqrt(1 - self.randX ** 2) * random.choice([-1,1])
    
    def randMove(self):
        #return a randomized and normalized movement
        self.move(self.randX,self.randY)

    def getNewState(self):
        return random.choices([0,1,2],self.pMatrix[self.state])[0]

    def randomWalk(self,time):
        #0 - optimal path towards closest coin
        #1 - random direction
        #2 - stay still
        #Currently, wait 60 - 120 ticks before considering state chang
        if time % random.randint(60,120) == 0: 
            self.state = self.getNewState()
            if self.state == 1: self.getRandMove() #get new random movement

        if self.state == 0:
            self.optMove()
        elif self.state == 1:
            
            self.randMove()
        #state 2 do nothing




class Coin(GameObject):
    #have the coin give itself a random coordinate for now
    #TODO: implement "placement bias"
    def __init__(self,group,background,coord):
        super().__init__(background,group,coord,"coin.png",(20,20))
        