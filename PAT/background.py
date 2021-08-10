import pygame 
from os import path

from pygame.constants import QUIT

class Background(pygame.sprite.Sprite):
    def __init__(self,res,image = "pacman.png"):
        pygame.sprite.Sprite.__init__(self)
        self.res = res
        self.screen = pygame.display.set_mode(res)
        self.surface = pygame.Surface(res)
        self.image = self.imgLoad(image)

        pygame.display.set_caption("Privilege Recognition Task")

    def imgLoad(self,img):

        relPath = path.join(path.dirname(__file__),"images","background",f"{img}")
        backImg = pygame.image.load(relPath).convert_alpha()
        backImg = pygame.transform.scale(backImg,self.res)
        return backImg
    
    def draw(self):
        #fills a black screen
        self.screen.fill((255,255,255))
    
        #not a fan of this dark background :P
        #self.screen.blit(self.image,(0,0))

class HUD:
    def __init__(self, background, agents):
        self.background = background
        self.agents = agents
        self.size = int(min(self.background.res[0],self.background.res[1]) * 0.04)
        
        fontPath = path.join("fonts","arial.TTF")

        self.fontHUD = pygame.font.SysFont('arial', self.size)
        self.timer = 0
    
    def updateTimer(self):
        self.timer = pygame.time.get_ticks()

    def resetTimer(self):
        self.timer = 0

    def drawHUD(self):
        i = 0
        for agent in self.agents:
            coinTxt = self.fontHUD.render(f"{agent.name} coins: {agent.coins}",True,(0,0,0))
            self.background.screen.blit(coinTxt,(0,self.size * i))
            i += 1

        #Timer
        timerTxt = self.fontHUD.render(f"Time: {self.timer // 1000}" ,True,(0,0,0))
        timerRect = timerTxt.get_rect()
        timerRect.topright = (self.background.res[0],0)
        self.background.screen.blit(timerTxt,timerRect)


class PauseScreen:
    def __init__(self,level,round,background,config,agents = [],levelStart = 0):
        self.level,self.round = level,round
        self.levelStart = levelStart
        self.agents = agents
        self.background = background
        self.config = config
        self.size = int(min(self.background.res[0],self.background.res[1]) * 0.04)
        self.font = pygame.font.SysFont('arial',self.size)

        #keep all question texts here
        self.qTextList = []

        self.renderQuestions()


        self.black = (0,0,0)
        self.red = (255,0,0)
        self.green = (0,255,0)
        self.blue = (0,0,255)

        self.paused = True
        

        self.next = self.font.render('Next',True,self.black,self.green)
 
        #self.back = self.font.render('Back',True,self.black,self.red) 
        #self.levelSelect = self.font.render('Level Select',True,self.black,pygame.SRCALPHA)

        self.nextRect = (600, self.background.res[1] - 50 - self.font.size('Next')[1]) + self.font.size('Next')
        #self.levelSelectRect = (self.xDim/2 - self.font.size("Level Select")[0]/2,100) + self.font.size('Level Select')
        #self.l1Rect = (100,150) + self.font.size('Level1: Chaos on Cat Street')
        #self.l2Rect = (100,250) + self.font.size('Level2: Rat Trap Crusaders')
        #self.backRect = (100,self.yDim - 50 - self.font.size('Back')[1]) + self.font.size('Back')

        #self.story = self.imgLoad("story.png")
        #self.l1Story = self.imgLoad('l1story.png')
        #self.l2Story = self.imgLoad('l2story.png')

        self.menuRect = (50,50,self.background.res[0] - 100,self.background.res[1] - 100)
        self.startRect = (320,680,100,50)
        #self.quitRect  = (470,680,100,50)
        #self.titleRect = (119,134,400,100)
        #self.image = self.imgLoad("highwayright.png")
        #self.titleImage = self.imgLoad("logo.png")

    def renderQuestions(self):
        for q in self.config["questions"]:
            self.qTextList.append(self.font.render(q["question"],True,(0,0,0)))

    def blitQuestions(self):
        yOff = 0
        for qText in self.qTextList:
            self.background.screen.blit(qText,(0,yOff,self.background.res[0],self.background.res[1]))
            
            yOff += 100
        
        startText = self.font.render('Start',True,(0,0,0))
        self.background.screen.blit(startText,self.startRect)
    
    def blitSumStats(self):
        levelTxt = self.font.render(f"Level {self.level + 1} Round {self.round}",True,(0,0,0))
        self.background.screen.blit(levelTxt,(0,0,self.background.res[0],self.background.res[1]))
        yOff = 100
        for agent in self.agents:
            coinTxt = self.font.render(f"{agent.name} coins: {agent.coins}",True,(0,0,0))
            self.background.screen.blit(coinTxt,(0,yOff,self.background.res[0],self.background.res[1]))
            yOff += 100
        
        startText = self.font.render('Next Round',True,(0,0,0))
        self.background.screen.blit(startText,self.startRect)

    
    def blitFinalStats(self,cList):
        levelTxt = self.font.render(f"Level {self.level + 1} finished!",True,(0,0,0))
        self.background.screen.blit(levelTxt,(0,0,self.background.res[0],self.background.res[1]))
        yOff = 100
        pTxt = self.font.render(f"Player total coins: {cList[0]}",True,(0,0,0))
        e1Txt = self.font.render(f"Enemy1 total coins: {cList[1]}",True,(0,0,0))
        e2Txt = self.font.render(f"Enemy2 total coins: {cList[2]}",True,(0,0,0))
        e3Txt = self.font.render(f"Enemy3 total coins: {cList[3]}",True,(0,0,0))

        self.background.screen.blit(pTxt,(0,100,self.background.res[0],self.background.res[1]))
        self.background.screen.blit(e1Txt,(0,200,self.background.res[0],self.background.res[1]))
        self.background.screen.blit(e2Txt,(0,300,self.background.res[0],self.background.res[1]))
        self.background.screen.blit(e3Txt,(0,400,self.background.res[0],self.background.res[1]))

        startText = self.font.render('End Level',True,(0,0,0))
        self.background.screen.blit(startText,self.startRect)
    def updateLoop(self,x=[]):
        #self.autoScrollTimeUpdate()
        #self.autoScroll()
        self.drawAll(x)
        self.startInteraction()


        pygame.display.flip()
        pygame.display.update()


    #custom designed for start menu
    def startInteraction(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.menuInteraction(pygame.mouse.get_pos())


            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: #Quitting out of fullScreen
                pygame.quit()
                exit()
    

    def drawAll(self,x):
        
        self.background.screen.fill((255,255,255))
        pygame.draw.rect(self.background.surface,(255,255,0),self.startRect)
        #pygame.draw.rect(self.background,(255,0,0),self.quitRect)
        
        #self.background.blit(self.titleImage,(300,180,400,400))
        

        if self.levelStart == 0:
            self.blitQuestions()
        elif self.levelStart == 1:
            #display some summary stats
            self.blitSumStats()

        else:
            self.blitFinalStats(x)



    #defines all the menu interactions given mousepos
    def menuInteraction(self,mousePos):
        x,y = mousePos

        inX = x in range(self.startRect[0], self.startRect[0] + self.startRect[2])
        inY = y in range(self.startRect[1], self.startRect[1] + self.startRect[3])
        if (inX and inY):

            self.paused = False

        #
