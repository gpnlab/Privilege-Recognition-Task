import numpy
import pygame
from configReader import ConfigReader
from background import *
from objects import *

class PAT:
    def __init__(self,levels = 1):
        pygame.init()

        #RES is fullScreen
        self.levels = levels
        self.displayInfo = pygame.display.Info()
        self.res = (self.displayInfo.current_w, self.displayInfo.current_h)

        
        #self.font = pygame.font.SysFont('arial',20)
        self.background = Background(self.res)
        

    def main_loop(self):
        for i in range(self.levels):
            currLevel = Level(self,i)

            while currLevel.inProgress:
                currLevel.main_loop()
            
            print("finished level!")
            print(currLevel.info)
            currLevel.reset()


class Level:
    def __init__(self,Pat,level = 0):
        config = ConfigReader.parseToDict(f"config{level}.txt")
        print(config)
        self.background = Pat.background
        self.res = Pat.res
        self.coinsLeft = config["numberOfCoins"]
        self.inProgress = True
        self.clock = pygame.time.Clock()

        #TODO: decide if lists would be the best way of storing and updating information
        # We have to update info with each game tick so efficiency is definitely in question
        # internet says list appending is constant time so I'll trust that 0.0

        self.info = [["tick","coins left","player input", "player coins", "e1 coins", "e2 coins", "e3 coins","player pos", "e1 pos", "e2 pos", "e3 pos"]]

        #to make sure info is fast as possible, I will convert everything into strings at the very end
        

        
        #kill all sprites at the end of each level
        #aGroup is the group of all agents
        #cGroup is the group of all coins
        self.aGroup = pygame.sprite.Group()
        self.eGroup = pygame.sprite.Group()
        self.cGroup = pygame.sprite.Group()

        self.player = Player(self.background,self.aGroup,(self.res[0] // 4, self.res[1] // 4), config["playerVel"], "p1.png")
        
        #TODO: change the temporary spawn points of enemies, and change sprite
        # aaand make it so this is less disgusting code
        self.enemy1 = Enemy("enemy1",self.background,self.aGroup,self.cGroup,(3 * self.res[0] // 4,self.res[1] // 4),config["enemy1Vel"],"p2.png")

        self.enemy2 = Enemy("enemy2",self.background,self.aGroup,self.cGroup,(self.res[0] // 4,3 * self.res[1] // 4),config["enemy2Vel"],"p3.png")
        
        self.enemy3 = Enemy("enemy3",self.background,self.aGroup,self.cGroup,(3 * self.res[0] // 4,3 * self.res[1] // 4),config["enemy3Vel"],"p4.png")

        self.eGroup.add(self.enemy1)
        self.eGroup.add(self.enemy2)
        self.eGroup.add(self.enemy3)

        #Pass background and player into HUD
        self.HUD = HUD(self.background, self.aGroup) 

        #set mean acoording to biases:
        meanCoor = (self.res[0] / 2, self.res[1] / 2)
        
        #TODO: get a stronger notion of 'bias', right now its just an arbitrary adjustment to mean

        if config["playerBias"]:
            print("playerBias detected")
            meanCoor = self.player.x,self.player.y
        
        if config["enemy1Bias"]:
            meanCoor = self.enemy1.x,self.enemy1.y
        if config["enemy2Bias"]:
            meanCoor = self.enemy2.x,self.enemy2.y
        if config["enemy3Bias"]:
            meanCoor = self.enemy3.x,self.enemy3.y

        for i in range(int(config["numberOfCoins"])):
            spawnCoord = numpy.random.normal(meanCoor[0],self.res[0] / 4),numpy.random.normal(meanCoor[1],self.res[1] / 4)
            
            while spawnCoord[0] < 50 or spawnCoord[0] > self.res[0] or spawnCoord[1] < 50 or spawnCoord[1] > self.res[1]:
                spawnCoord = numpy.random.normal(meanCoor[0],self.res[0] / 4),numpy.random.normal(meanCoor[1],self.res[1] / 4)
            
            coin = Coin(self.cGroup,self.background,spawnCoord)
            

        
    #TODO: handle logistics of rounds changing
    def main_loop(self):
        while self.inProgress:
            
            keys = pygame.key.get_pressed()

            self._handle_input(keys)
            self._process_game_logic(keys)
            self._draw()

    def _handle_input(self,keys):
        #player moves with WASD
        self.player.getInput(keys)

    def _process_game_logic(self,keys):
        events = pygame.event.get()

        #collisions
        collectFlag = pygame.sprite.groupcollide(self.aGroup,self.cGroup,False,True)

        #allows us to access and update selected agent coin count
        for (agent,_) in collectFlag.items(): 
            print(f"{agent.name} has collected a coin!")
            #when more players are added, this will be done via group.items (see level.py of Social Heroes)
            agent.coins += 1
            self.coinsLeft -= 1
        
        

        
        for e in self.eGroup:
            if self.coinsLeft > 0:
                e.randomWalk(self.HUD.timer)
        
        #TODO: flag whenever all coins are gone to end "level"

        if self.coinsLeft <= 0:
            print("finished level")
            self.inProgress = False

        for event in events:
            if event.type == pygame.QUIT: 
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: #Quitting out of fullScreen
                pygame.quit()
                exit()


        

        #Clock updates
        self.HUD.updateTimer()

        self.updateInfo(keys)

        


    def _draw(self):

        self.background.draw()

        #sprite groups are great because they allow you
        #to draw all sprites of the group at the same time
        self.aGroup.draw(self.background.screen)
        self.cGroup.draw(self.background.screen)
        self.HUD.drawHUD()
        
        pygame.display.flip()
        pygame.display.update()

    def updateInfo(self,keys):

        keysPressedStr = "" 

        if keys[pygame.K_w]:
            keysPressedStr += "w"
        elif keys[pygame.K_s]:
            keysPressedStr += "s"
            
        if keys[pygame.K_a]:
            keysPressedStr += "a"
        elif keys[pygame.K_d]:
            keysPressedStr += "d"

        #TODO: This hurts
        self.info.append([pygame.time.get_ticks(),self.coinsLeft,keysPressedStr,str(self.player.coins),str(self.enemy1.coins),str(self.enemy2.coins),str(self.enemy3.coins),str((self.player.x,self.player.y)),str(self.player.coins),str(self.enemy1.coins),str(self.enemy2.coins),str(self.enemy3.coins),str((self.enemy1.x,self.enemy1.y)),str((self.enemy2.x,self.enemy2.y)),str((self.enemy3.x,self.enemy3.y))])
        
    def reset(self):
        pygame.sprite.Group.empty(self.aGroup)
        pygame.sprite.Group.empty(self.eGroup)
        pygame.sprite.Group.empty(self.cGroup)

    





