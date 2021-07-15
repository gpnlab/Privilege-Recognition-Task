import math
import pygame
import random
from os import path, stat

class PAT:
    def __init__(self):
        pygame.init()

        #RES is fullScreen
        self.displayInfo = pygame.display.Info()
        self.res = (self.displayInfo.current_w, self.displayInfo.current_h)

        
        self.font = pygame.font.SysFont('arial',20)
        self.background = Background(self.res)
        self.clock = pygame.time.Clock()

        #aGroup is the group of all agents
        #cGroup is the group of all coins
        self.aGroup = pygame.sprite.Group()
        self.eGroup = pygame.sprite.Group()
        self.cGroup = pygame.sprite.Group()

        self.player = Player(self.background,self.aGroup,(self.res[0] // 4, self.res[1] // 4))
        
        #TODO: change the temporary spawn points of enemies, and change sprite
        # aaand make it so this is less disgusting code
        self.enemy1 = Enemy("enemy1",self.background,self.aGroup,self.cGroup,(3 * self.res[0] // 4,self.res[1] // 4))

        self.enemy2 = Enemy("enemy2",self.background,self.aGroup,self.cGroup,(self.res[0] // 4,3 * self.res[1] // 4))
        
        self.enemy3 = Enemy("enemy3",self.background,self.aGroup,self.cGroup,(3 * self.res[0] // 4,3 * self.res[1] // 4))

        self.eGroup.add(self.enemy1)
        self.eGroup.add(self.enemy2)
        self.eGroup.add(self.enemy3)

        #Pass background and player into HUD
        self.HUD = HUD(self.background, self.player) 

        #TODO: fixed number of coins currently 
        for i in range(30):
            spawnCoord = random.randint(50,self.res[0]),random.randint(50,self.res[1])
            coin = Coin(self.cGroup,self.background,spawnCoord)
            

        
    #TODO: handle logistics of rounds changing
    def main_loop(self):
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()

    def _handle_input(self):
        self.player.getInput()

    def _process_game_logic(self):
        events = pygame.event.get()
        
        #TODO: flag whenever all coins are gone to end "level"
        for e in self.eGroup:
            if self.coinsLeft > 0: e.optMove()

        for event in events:
            if event.type == pygame.QUIT: 
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: #Quitting out of fullScreen
                pygame.quit()
                exit()


        #collisions
        collectFlag = pygame.sprite.groupcollide(self.aGroup,self.cGroup,False,True)

        #allows us to access and update selected agent coin count
        for (agent,_) in collectFlag.items(): 
            print(f"{agent.name} has collected a coin!")
            #when more players are added, this will be done via group.items (see level.py of Social Heroes)
            agent.coins += 1
            self.coinsLeft -= 1

        #Clock updates
        self.HUD.updateTimer()

        


    def _draw(self):

        self.background.draw()

        #sprite groups are great because they allow you
        #to draw all sprites of the group at the same time
        self.aGroup.draw(self.background.screen)
        self.cGroup.draw(self.background.screen)
        self.HUD.drawHUD()
        
        pygame.display.flip()
        pygame.display.update()

    
class Background(pygame.sprite.Sprite):
    def __init__(self,res,image = "pacman.png"):
        pygame.sprite.Sprite.__init__(self)
        self.res = res
        self.screen = pygame.display.set_mode(res)
        self.surface = pygame.Surface(res)
        self.image = self.imgLoad(image)

        pygame.display.set_caption("Privilege Recognition Task")

    def imgLoad(self,img):

        relPath = path.join(path.dirname(__file__),f"images/background/{img}")
        backImg = pygame.image.load(relPath).convert_alpha()
        backImg = pygame.transform.scale(backImg,self.res)
        return backImg
    
    def draw(self):
        #fills a black screen
        self.screen.fill((255,255,255))
    
        #not a fan of this dark background :P
        #self.screen.blit(self.image,(0,0))

class HUD:
    def __init__(self, background, player):
        self.background = background
        self.player = player
        self.fontHUD = pygame.font.SysFont('arial', int(min(self.background.res[0],self.background.res[1]) * 0.1))
        self.timer = 0
    
    def updateTimer(self):
        self.timer = pygame.time.get_ticks()

    def resetTimer(self):
        self.timer = 0

    def drawHUD(self):
        #Coins
        coinTxt = self.fontHUD.render(f"Coins: {self.player.coins}",True,(0,0,0))
        self.background.screen.blit(coinTxt,(0,0))

        #Timer
        timerTxt = self.fontHUD.render(f"Time: {self.timer // 1000}" ,True,(0,0,0))
        timerRect = timerTxt.get_rect()
        timerRect.topright = (self.background.res[0],0)
        self.background.screen.blit(timerTxt,timerRect)



class GameObject(pygame.sprite.Sprite):
    def __init__(self,background,group,coord,imgName,resize = (40,40), velocity = .5,acceleration = 0):
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
    
    def __init__(self,name,background,group,coord,imgName = "placeholder.png"):
        super().__init__(background,group,coord,imgName)
        self.name = name
        self.coins = 0

    
class Player(Agent):
    def __init__(self,background,group,coord,imgName = "placeholder.png"):
        super().__init__("player",background,group,coord,imgName)

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
    def __init__(self,name,background,group,cGroup,coord,imgName = "placeholder.png"):
        super().__init__(name,background,group,coord,imgName)
        self.coinGroup = cGroup

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



class Coin(GameObject):
    #have the coin give itself a random coordinate for now
    #TODO: implement "placement bias"
    def __init__(self,group,background,coord):
        super().__init__(background,group,coord,"coin.png",(20,20))
        
