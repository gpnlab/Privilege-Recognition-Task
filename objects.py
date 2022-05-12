import pygame
import math
import random
from os import path, stat
from exe import EXE

class GameObject(pygame.sprite.Sprite):
    def __init__(self,background,group,coord,imgName,velocity = .5,acceleration = 0,resize = (40,40),seed = 0):
        pygame.sprite.Sprite.__init__(self)

        random.seed(seed)

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

        asset_url = EXE.resource_path(f"images/objects/{img}")
        

        playerImg = pygame.image.load(asset_url).convert_alpha()

        
        #for exe wrapping
        asset_url = EXE.resource_path(f"images/objects/{img}")
        
        playerImg = pygame.image.load(asset_url).convert_alpha()
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
    
    def __init__(self,name,background,group,coord,velocity,imgName = "placeholder.png",seed = 0):
        super().__init__(background,group,coord,imgName,velocity,seed)
        self.name = name
        self.coins = 0

    
class Player(Agent):
    def __init__(self,background,group,coord,velocity,imgName = "placeholder.png", seed = 0):
        super().__init__("Player 1",background,group,coord,velocity,imgName,seed)

    def getInput(self,keys,time_passed):
        
        #self.imgUpdate(keys)
        #when 8 directions added, this will update with corresponding sprite
        xInd,yInd = 0,0
        
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            yInd = -1
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            yInd = 1
            
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            xInd = -1 
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            xInd = 1

        if yInd != 0 and xInd != 0:
            self.move(math.sqrt(2) * xInd / 2, math.sqrt(2) * yInd / 2)
        else:
            self.move(xInd,yInd)


#TODO: improve AI
#   1. Don't allow "half" movements
#   2. If keeping markov chain approach, change states to be more "human"
#   3. Try to use less """"Quotations""""
class Enemy(Agent):
    #need to pass in coin group for AI to find nearest coin
    def __init__(self,name,background,group,cGroup,coord,velocity,imgName = "placeholder.png",seed=0):
        super().__init__(name,background,group,coord,velocity,imgName,seed)
        self.coinGroup = cGroup
        
        #3 states:
        #0 - optimal path towards closest coin
        #1 - random direction
        #2 - stay still
        #transfer probabilities will be listed in the readme
        self.state = 0

        #probability matrix for transfering
        self.pMatrix = [[8,1,1],[7,1,2],[7,1,2]]

        #keep current objective (coin coord)
        self.coinObj = (0,0)
        self.setObj()

    def dist(self,c1,c2):
        (x1,y1),(x2,y2) = c1,c2
        return math.sqrt ((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def getRandCoinCoord(self):
        if len(self.coinGroup) == 0: return (0,0)

        randCoin = self.coinGroup.sprites()[random.randint(0,len(self.coinGroup) - 1)]

        return (randCoin.x,randCoin.y)
    #loop through everything in coin group
    def getNearestCoinCoord(self):
        if len(self.coinGroup) == 0: return (0,0)

        #default "max" distance
        bestDist = self.bg.res[0]

        for coin in self.coinGroup:
            currDist = self.dist((self.x,self.y),(coin.x,coin.y))

            if currDist < bestDist:
                bestCoin = coin
                bestDist = currDist

        return (bestCoin.x,bestCoin.y)

    #should be ran whenever coin is obtained
    #for now, have it be 50/50 whether ai chooses opt or random coin
    def setObj(self):
        #check if coin is still in group, if yes, maybe don't change obj
        inFlag = False
        try:
            x,y = self.coinObj
        except:
            x,y = (0,0)
        #for coin in self.coinGroup:
        #    if (x == coin.x and y == coin.y):
        #        inFlag = True
                
        
        if (random.randint(0,1) == 0):
            self.coinObj = self.getNearestCoinCoord()
        elif (random.randint(0,1) == 0):
            self.coinObj = self.getRandCoinCoord()
            print(f"set objective to {self.coinObj}")

        #.25 percent chance we stay with current
        
        


    #optimal movement toward nearest coin
    #will have to normalize vector to the velocity of the enemy (yay linear algebra)
    def optMove(self):
        #try:
        #    (cX,cY) = self.getNearestCoinCoord()
        #except:
        #    (cX,cY) = (0,0)
        (cX,cY) = self.coinObj
        d = self.dist((cX,cY),(self.x,self.y))

        #normalize - this is a relic of ai surpemacy
        xMov = self.vel * (cX - self.x) / d
        yMov = self.vel * (self.y - cY) / d

        #indicators for which direction
        xInd,yInd = 0,0
        #prevent half movements
        if xMov < 0:
            xInd = -1
        elif xMov > 0:
            xInd = 1

        if yMov > 0:
            yInd = -1
        elif yMov < 0:
            yInd = 1
        
        if yInd != 0 and xInd != 0:
            self.move(math.sqrt(2) * xInd / 2, math.sqrt(2) * yInd / 2)
        else:
            self.move(xInd,yInd)
            
    def getRandMove(self):
        self.randX = random.uniform(-1,1)
        self.randY = math.sqrt(1 - self.randX ** 2) * random.choice([-1,1])
    
    def randMove(self):
        #return a randomized and normalized movement
        self.move(self.randX,self.randY)

    def getNewState(self):
        return random.choices([0,1,2],self.pMatrix[self.state])[0]

    def randomWalk(self):
        #0 - optimal path towards closest coin
        #1 - random direction
        #2 - stay still
        #Currently, wait 10 - 60 ticks before considering state chang
        #if time % random.randint(10,60) == 0: 
        #    self.state = self.getNewState()
        #    if self.state == 1: self.getRandMove() #get new random movement

        #if self.state == 0:
        self.optMove()
        #elif self.state == 1:
            
        #    self.randMove()
        #state 2 do nothing




class Coin(GameObject):
    #have the coin give itself a random coordinate for now
    #TODO: implement "placement bias"
    def __init__(self,group,background,coord):
        super().__init__(background,group,coord,"coin.png",(20,20))
        