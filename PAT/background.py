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
    def __init__(self,level,levels,round,rounds,background,config,agents = [],levelStart = 0):
        self.level,self.round = level,round
        self.levelStart = levelStart
        self.levels = levels
        self.rounds = rounds

        self.agents = agents
        self.background = background
        self.config = config
        self.size = int(min(self.background.res[0],self.background.res[1]) * 0.04)
        self.font = pygame.font.SysFont('arial',self.size)

        #keep all question and answer texts here
        self.qTextList = []

        #a list of tuples: (font render, rect)
        self.aTextList = []

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


        self.menuRect = (50,50,self.background.res[0] - 100,self.background.res[1] - 100)
        self.startRect = (320,680,self.font.size('Next Round')[0],self.font.size('Next Round')[1])
        #self.quitRect  = (470,680,100,50)
        #self.titleRect = (119,134,400,100)
        #self.image = self.imgLoad("highwayright.png")
        #self.titleImage = self.imgLoad("logo.png")

    def returnQuestionText(self):
        retList = []
        for q in self.config["questions"]:
            retList.append(q["question"])
        return retList

    def returnAnswerText(self):
        retList = []
        for aList in self.aTextList:
            currAnsList = []
            for (ansTxt,ansRender,ansRect,choice) in aList:
                if choice:
                    currAnsList.append(ansTxt)
            retList.append(currAnsList)
        
        return retList

    def renderQuestions(self):
        yOff = 0
        for q in self.config["questions"]:
            qRendered = self.font.render(f"{yOff + 1}. {q['question']}",True,(0,0,0))
            qRenderedRect = (0,yOff * qRendered.get_height() * 3,self.font.size(f"{yOff + 1}. {q['question']}")[0],self.font.size(f"{yOff + 1}. {q['question']}")[1])
            qType = q["type"]
            self.qTextList.append((qRendered,qRenderedRect,qType))
            answers = []
            xOff = 0


            #each question is a dictionary of question, question type, and answers
            #TODO: implement questionType, so we can choose multiple answers or single
            #FOR NOW

            #0: single answer
            #1: multiple answer
            #2: short response
            for a in q["answers"]:
                aRendered = self.font.render(a,True,(0,0,0))
                aRenderedRect = (xOff, yOff * qRendered.get_height() * 3 + qRendered.get_height() ,self.font.size(a)[0],self.font.size(a)[1])
                answers.append((a,aRendered,aRenderedRect,False))
                xOff += aRendered.get_width() * 2
            
            self.aTextList.append(answers)
            yOff += 1
    

    def blitQuestions(self):
        self.background.screen.fill((255,255,255))

        yOff = 0
        for (q,qRect,qType) in self.qTextList:
            self.background.screen.blit(q,qRect)

            #questions and answers share same index
            ansList = self.aTextList[yOff]

            

            for (_,ansRend,ansRect,_) in ansList:
                self.background.screen.blit(ansRend,ansRect)
            yOff += 1
        
        startText = self.font.render('Start',True,(0,0,0))
        self.background.screen.blit(startText,self.startRect)
    
    #this is for after round is over
    def blitSumStats(self):

        #draw only a rectangle to display stats, unlike other blit functions
        pygame.draw.rect(self.background.screen,(234,0,120),(200,200,1000,600),0)

        levelTxt = self.font.render(f"Level {self.level + 1} Round {self.round}/{self.rounds} finished!",True,(0,0,0))
        self.background.screen.blit(levelTxt,(200,200,self.background.res[0],self.background.res[1]))
        #yOff = 100
        #for agent in self.agents:
        #    coinTxt = self.font.render(f"{agent.name} coins: {agent.coins}",True,(0,0,0))
        #    self.background.screen.blit(coinTxt,(0,yOff,self.background.res[0],self.background.res[1]))
        #    yOff += 100
        
        startText = self.font.render('Next Round',True,(0,0,0))
        pygame.draw.rect(self.background.screen,(100,100,100),(self.startRect[0],self.startRect[1],self.font.size('Next Round')[0],self.font.size('Next Round')[1]))
        self.background.screen.blit(startText,self.startRect)

    
    def blitFinalStats(self,cList):
        self.background.screen.fill((255,255,255))
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

        #starting game
        inX = x in range(self.startRect[0], self.startRect[0] + self.startRect[2])
        inY = y in range(self.startRect[1], self.startRect[1] + self.startRect[3])
        if (inX and inY):
            self.paused = False

        #answering questions - aTextList is indexed by the question number, list list of answers
        currInd1 = 0
        for aList in self.aTextList:
            currInd2 = 0
            for (ansTxt,ansRender,ansRect,choice) in aList:
                inX = x in range(ansRect[0], ansRect[0] + ansRect[2])
                inY = y in range(ansRect[1],ansRect[1] + ansRect[3])

                if (inX and inY):

                    newChoice = not choice
                    
                    #before the answer is chosen, check the question type, and unchoose all other answers before hand if needed
                    if (self.qTextList[currInd1][2] == 0):
                        print("question type 0")
                        #unselect all items in that answer list
                        aListIndex = 0
                        for (aTxt,aRender,aRect,c) in aList:
                            newR = self.font.render(aTxt,True,(0,0,0))

                            self.aTextList[currInd1][aListIndex] = (aTxt,newR,aRect,False)
                            aListIndex += 1
                        

                    #choose the answer
                
                    if newChoice: 
                        newCol = (0,255,0) 
                    else: 
                        newCol = (0,0,0)

                    nAnsRender = self.font.render(ansTxt,True,newCol)

                    self.aTextList[currInd1][currInd2] = (ansTxt,nAnsRender,ansRect,newChoice)
                currInd2 += 1
            currInd1 += 1

