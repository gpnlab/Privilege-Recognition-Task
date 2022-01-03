import numpy
import pygame
from configReader import ConfigReader
from logWriter import LogWriter
from background import *
from objects import *
from datetime import date, datetime,time
import sys


seed = 0

class PAT:
    def __init__(self):
        pygame.init()
        
        numpy.random.seed(seed)

        
        self.presetName = "block1"

        #levels is a list of level names, which will be individual jsons in the respective preset directory
        while True:
            try:
                
                #RES is fullScreen
                self.mainConfig = ConfigReader.parseToDict("main",self.presetName)
                
            except Exception:
                self.presetName = input(f"Preset {self.presetName} does not exist. Try a different name: ")
                continue

            break

        

        self.levels = self.mainConfig["levels"]
        
        print(self.levels)
        self.displayInfo = pygame.display.Info()
        self.res = (self.displayInfo.current_w, self.displayInfo.current_h)
        self.clock = pygame.time.Clock()

        
    

        self.time = datetime.now().strftime("%H_%M_%S")
        
        #self.font = pygame.font.SysFont('arial',20)
        self.background = Background(self.res)

        self.start = StartScreen(self.background)

        while not self.start.finished:
            self.start.mainLoop()
        self.patientName = self.start.name

    def main_loop(self):

        for currLevel in range(len(self.levels)):
            level = Level(self,self.time,self.patientName,self.presetName,currLevel,self.levels)

            level.main_loop()

        final = FinalScreen(self.background)

        final.mainLoop()

            
            
            
            
    def finalScreen(self):
        self.background.screen.fill((200,200,200))

        finalTxt = "Game Complete! Press esc on your keyboard to exit."






class Level:
    def __init__(self,Pat,timestamp,patientName,presetName,level,levelList):
        self.Pat = Pat
        self.levelList = levelList
        self.levelNum = level
        self.levels = len(levelList)
        self.config = ConfigReader.parseToDict(f"{levelList[level]}",presetName)
        print(self.config)
        self.background = Pat.background
        self.res = Pat.res
        self.pauseFlag = True

        self.logWriter = LogWriter(presetName,patientName,timestamp,seed)

        self.logWriter.writeSeed()
        
        #not a questions block
        if "questions" not in self.config:
            self.aGroup = pygame.sprite.Group()
            self.eGroup = pygame.sprite.Group()
            self.cGroup = pygame.sprite.Group()

            self.initGroups()
            #keep track of total coins
            self.pCoins = 0
            self.e1Coins = 0
            self.e2Coins = 0
            self.e3Coins = 0
            #self.coinsLeft = config["numberOfCoins"]
            #self.inProgress = True
            
            
            self.rounds = int(self.config["rounds"])
            self.currRound = 0
            #self.time = 0
        

        
            self.info = [["tick","coins left","player input", "player coins", "e1 coins", "e2 coins", "e3 coins","player pos", "e1 pos", "e2 pos", "e3 pos"]]

    

    
    def initGroups(self):
        self.player = Player(self.background,self.aGroup,(self.res[0] // 4, self.res[1] // 4), self.config["playerVel"], "p1.png")
        
        #TODO: change the temporary spawn points of enemies, and change sprite
        # aaand make it so this is less disgusting code
        self.enemy1 = Enemy("player2",self.background,self.aGroup,self.cGroup,(3 * self.res[0] // 4,self.res[1] // 4),self.config["enemy1Vel"],"p2.png")

        self.enemy2 = Enemy("player3",self.background,self.aGroup,self.cGroup,(self.res[0] // 4,3 * self.res[1] // 4),self.config["enemy2Vel"],"p3.png")
        
        self.enemy3 = Enemy("player4",self.background,self.aGroup,self.cGroup,(3 * self.res[0] // 4,3 * self.res[1] // 4),self.config["enemy3Vel"],"p4.png")

        self.eGroup.add(self.enemy1)
        self.eGroup.add(self.enemy2)
        self.eGroup.add(self.enemy3)

    def main_loop(self):

        #blit questions here if a question block
        if "questions" in self.config:
            levelStartPause = PauseScreen(self.levelNum,self.levels,0,0,self.background,self.config)
            while levelStartPause.paused:
                levelStartPause.updateLoop()
            #record what answers were chosen
            self.logWriter.writeLevelQA(levelStartPause.returnQuestionText(),levelStartPause.returnAnswerText(),self.levelList[self.levelNum])

        else:
            for currRound in range(self.rounds):
              

                round = Round(self.Pat,self.levelNum,currRound,self.config)

            
                while round.inProgress:
                    round.main_loop()
            
                self.pCoins += round.player.coins
                self.e1Coins += round.enemy1.coins
                self.e2Coins += round.enemy2.coins
                self.e3Coins += round.enemy3.coins

            
                print(f"writing log for level {self.levelList[self.levelNum]}, round {self.currRound}")
                self.logWriter.writeLevelLog(round.info,self.levelList[self.levelNum],self.currRound)
                self.currRound += 1
            


            
                pauseScreen = PauseScreen(self.levelNum,self.levels,self.currRound,self.rounds,self.background,round.config,round.aGroup,1)

                while pauseScreen.paused:
                    #TODO: only have a "box" display, so it doesn't block the entire screen
                    pauseScreen.updateLoop() 

            round.reset()
        
        
            
        #keys = pygame.key.get_pressed()

        #self._handle_input(keys)
        #self._process_game_logic(keys)
        #self._draw()

    def _handle_input(self,keys):
        #player moves with WASD
        self.player.getInput(keys)

    def _process_game_logic(self,keys):
        self.time += 1
        events = pygame.event.get()

        #collisions
        collectFlag = pygame.sprite.groupcollide(self.aGroup,self.cGroup,False,True)

        #allows us to access and update selected agent coin count
        #everytime anyone collects a coin, update objective
        for (agent,_) in collectFlag.items():
            print(f"{agent.name} has collected a coin!")
            #when more players are added, this will be done via group.items (see level.py of Social Heroes)
            agent.coins += 1
            self.coinsLeft -= 1
        
        

        
        for e in self.eGroup:
            if self.coinsLeft > 0:
                e.randomWalk(self.time)


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
        self.info.append([str(self.time),str(self.coinsLeft),keysPressedStr,str(self.player.coins),str(self.enemy1.coins),str(self.enemy2.coins),str(self.enemy3.coins),str((self.player.x,self.player.y)),str(self.player.coins),str(self.enemy1.coins),str(self.enemy2.coins),str(self.enemy3.coins),str((self.enemy1.x,self.enemy1.y)),str((self.enemy2.x,self.enemy2.y)),str((self.enemy3.x,self.enemy3.y))])
        
    def reset(self):
        pygame.sprite.Group.empty(self.aGroup)
        pygame.sprite.Group.empty(self.eGroup)
        pygame.sprite.Group.empty(self.cGroup)

    

class Round:
    def __init__(self,Pat,levelNum,roundNum,config):
        print(f"starting level {levelNum}, round {roundNum}")
        self.coinsLeft = config["numberOfCoins"]
        self.inProgress = True
        self.background = Pat.background
        self.res = Pat.res
        self.time = 0

        self.config = config

    
        self.info = [["tick","coins left","player input", "player coins", "e1 coins", "e2 coins", "e3 coins","player pos", "e1 pos", "e2 pos", "e3 pos"]]

        #to make sure info is fast as possible, I will convert everything into strings at the very end


        #TODO: make sure coins don't spawn on top of players
        
        #kill all sprites at the end of each level
        #aGroup is the group of all agents
        #cGroup is the group of all coins
        self.aGroup = pygame.sprite.Group()
        self.eGroup = pygame.sprite.Group()
        self.cGroup = pygame.sprite.Group()

        

        #Pass background and player into HUD
        self.HUD = HUD(self.background, self.aGroup) 
        self.initGroups()

        #set mean acoording to biases:
        meanCoor = (self.res[0] / 2, self.res[1] / 2)
        
        

        if config["playerBias"] > 0:
            print("playerBias detected")

            dx = meanCoor[0] - self.player.x
            dy = meanCoor[1] - self.player.y 
            meanCoor = ((meanCoor[0] - config["playerBias"] * dx),(meanCoor[1] - config["playerBias"] * dy))

        

        if config["enemy1Bias"] > 0:
            print("e1 bias")
            dx = meanCoor[0] - self.enemy1.x
            dy = meanCoor[1] - self.enemy1.y 
            meanCoor = ((meanCoor[0] - config["enemy1Bias"] * dx),(meanCoor[1] - config["enemy1Bias"] * dy))

        if config["enemy2Bias"] > 0:
            print("e2 bias")
            dx = meanCoor[0] - self.enemy2.x
            dy = meanCoor[1] - self.enemy2.y 
            meanCoor = ((meanCoor[0] - config["enemy2Bias"] * dx),(meanCoor[1] - config["enemy2Bias"] * dy))
        if config["enemy3Bias"] > 0:
            print("e3 bias")
            dx = meanCoor[0] - self.enemy3.x
            dy =  meanCoor[1] - self.enemy3.y 
            meanCoor = ((meanCoor[0] - config["enemy3Bias"] * dx),(meanCoor[1] - config["enemy3Bias"] * dy))

        

        for i in range(int(config["numberOfCoins"])):
            spawnCoord = numpy.random.normal(meanCoor[0],self.res[0] / 5),numpy.random.normal(meanCoor[1],self.res[1] / 5)
            
            while spawnCoord[0] < 100 or spawnCoord[0] > self.res[0] - 100 or spawnCoord[1] < 100 or spawnCoord[1] > self.res[1] - 100:
                spawnCoord = numpy.random.normal(meanCoor[0],self.res[0] / 4),numpy.random.normal(meanCoor[1],self.res[1] / 6)
            
            coin = Coin(self.cGroup,self.background,spawnCoord)
        
        for e in self.eGroup:
            e.setObj()
        

    
    def initGroups(self):
        self.player = Player(self.background,self.aGroup,(self.res[0] // 4, self.res[1] // 4), self.config["playerVel"], "p1.png",seed)
        
        #TODO: change the temporary spawn points of enemies, and change sprite
        # aaand make it so this is less disgusting code
        self.enemy1 = Enemy("player 2",self.background,self.aGroup,self.cGroup,(3 * self.res[0] // 4,self.res[1] // 4),self.config["enemy1Vel"],"p2.png",seed)

        self.enemy2 = Enemy("player 3",self.background,self.aGroup,self.cGroup,(self.res[0] // 4,3 * self.res[1] // 4),self.config["enemy2Vel"],"p3.png",seed)
        
        self.enemy3 = Enemy("player 4",self.background,self.aGroup,self.cGroup,(3 * self.res[0] // 4,3 * self.res[1] // 4),self.config["enemy3Vel"],"p4.png",seed)

        self.eGroup.add(self.enemy1)
        self.eGroup.add(self.enemy2)
        self.eGroup.add(self.enemy3)

    #main loop will check what 
    def main_loop(self):
            
        keys = pygame.key.get_pressed()

        self._handle_input(keys)
        self._process_game_logic(keys)
        self._draw()

        

    def _handle_input(self,keys):
        #player moves with WASD
        self.player.getInput(keys)

    def _process_game_logic(self,keys):
        self.time += 1
        events = pygame.event.get()

        #collisions
        collectFlag = pygame.sprite.groupcollide(self.aGroup,self.cGroup,False,True)

        #allows us to access and update selected agent coin count
        for (agent,_) in collectFlag.items(): 
            print(f"{agent.name} has collected a coin!")

            for e in self.eGroup:
                e.setObj()

            #when more players are added, this will be done via group.items (see level.py of Social Heroes)
            agent.coins += 1
            self.coinsLeft -= 1
        
        

        
        for e in self.eGroup:
            if self.coinsLeft > 0:
                e.randomWalk(self.time)
        
        #TODO: flag whenever all coins are gone to end "level"

        if self.coinsLeft <= 0 or len(self.cGroup) == 0:
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
        self.info.append([str(self.time),str(self.coinsLeft),keysPressedStr,str(self.player.coins),str(self.enemy1.coins),str(self.enemy2.coins),str(self.enemy3.coins),str((self.player.x,self.player.y)),str(self.player.coins),str(self.enemy1.coins),str(self.enemy2.coins),str(self.enemy3.coins),str((self.enemy1.x,self.enemy1.y)),str((self.enemy2.x,self.enemy2.y)),str((self.enemy3.x,self.enemy3.y))])
        
    def reset(self):
        pygame.sprite.Group.empty(self.aGroup)
        pygame.sprite.Group.empty(self.eGroup)
        pygame.sprite.Group.empty(self.cGroup)
