import pygame
import math
from os import path
from configReader import *

from pygame.constants import QUIT

class Background(pygame.sprite.Sprite):
    def __init__(self,res,image = "pacman.png"):
        pygame.sprite.Sprite.__init__(self)
        self.res = res
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.surface = pygame.Surface(res)
       #self.image = self.imgLoad(image)

        pygame.display.set_caption("Privilege Recognition Task")

    def imgLoad(self,img):

        print(f"loading {img}")

        asset_url = EXE.resource_path(f"images/objects/{img}")
        
        backImg = pygame.image.load(asset_url).convert_alpha()
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

class StartScreen:
    def __init__(self,background):
        self.name = ""
        self.finished = False
        self.background = background
        self.size = int(min(self.background.res[0],self.background.res[1]) * 0.1)
        self.font = pygame.font.SysFont('arial',self.size)
        
        self.enterText = self.font.render("Please enter your name",True,(0,0,0),(255,255,255))
        self.nameText = self.font.render(self.name,True,(0,0,0),(100,0,200))
        self.menuRect = (50,50,self.background.res[0] - 100,self.background.res[1] - 100)
        self.nameRect = (50 + self.background.res[0] // 5,50 + self.background.res[1] // 5,self.font.size(self.name)[0],self.font.size(self.name)[1])
    

    def updateName(self):
        self.nameRect = (50 + self.background.res[0] // 5,50 + self.background.res[1] // 5,self.font.size(self.name)[0],self.font.size(self.name)[1])
        self.nameText = self.font.render(self.name,True,(0,0,0),(10,80,200))

    def mainLoop(self):
        self.drawAll()
        self.startInteraction()
        pygame.display.flip()
        pygame.display.update()
        
    def drawAll(self):
        self.background.screen.fill((255,255,255))

        self.background.screen.blit(self.enterText,self.menuRect)
        self.background.screen.blit(self.nameText,self.nameRect)

    def startInteraction(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: #Quitting out of fullScreen
                pygame.quit()
                exit()
            
            elif event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_RETURN]:
                    self.finished = True
                elif keys[pygame.K_BACKSPACE]:
                    self.name =  self.name[:-1]
                elif len(self.name) < 20:
                    self.name += event.unicode
        self.updateName()

class PauseScreen:
    def __init__(self,level,levels,round,rounds,background,config,agents = [],levelStart = 0):
        self.level,self.round = level,round
        self.levelStart = levelStart
        self.levels = levels
        self.rounds = rounds

        self.agents = agents
        self.background = background
        self.config = config
        self.size = int(min(self.background.res[0],self.background.res[1]) * 0.02)
        self.font = pygame.font.SysFont('arial',self.size)

        #keep all question and answer texts here
        self.qTextList = []

        #a list of tuples: (font render, rect)
        self.aTextList = []

        if "questions" in self.config:  
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
        self.startRect = (self.background.res[0] * 3 // 4,self.background.res[1] * 9 // 10,self.font.size('Start')[0] + 20,self.font.size('Start')[1] + 20)
        self.nextRoundRect = (460,550,self.font.size('Next Round')[0] + 10,self.font.size('Next Round')[1] + 10)

        self.startText = self.font.render('Start',True,(0,0,0))
        self.nextText = self.font.render('Next Round',True,(0,0,0))
        self.endLevelText = self.font.render('End Level',True,(0,0,0))
    #returns all question strings specified in the given config
    def returnQuestionText(self):
        retList = []
        for q in self.config["questions"]:
            retList.append(q["question"])
        return retList

    #returns all answer strings specified in the given config
    def returnAnswerText(self):
        retList = []
        currIndex = 0
        for aList in self.aTextList:

            qType = self.qTextList[currIndex][2]

            currAnsList = []
            for aa in aList:
                if qType < 2:
                    (ansTxt,ansRender,ansRect,choice) = aa
                    if choice:
                        currAnsList.append(ansTxt)
                else:
                    (center,radius,(lowLim,highLim),currVal,currValRender,choice) = aa
                    #if choice:
                    currAnsList.append(f"{currVal}")
            retList.append(currAnsList)

            currIndex += 1
        
        return retList

    #check that all questions given have been answered
    def allAnswered(self):
        currIndex = 0
        for aList in self.aTextList:

            qType = self.qTextList[currIndex][2]

            

            chosenForAny = False
            for aa in aList:

                #these are button type answers, just need at least one chosen
                if qType < 2:
                    (ansTxt,ansRender,ansRect,choice) = aa
                    if choice:
                        chosenForAny = True

                #slider type questions: as long as slider has been 'clicked', chosen == true
                elif qType == 2:
                    (center,radius,(lowLim,highLim),currVal,currValRender,choice) = aa
                    if not choice:
                        return False
                    chosenForAny = True

            if not chosenForAny:
                return False

            currIndex += 1
        
        return True


    def renderQuestions(self):
        yOff = 0
        for q in self.config["questions"]:
            qRendered = self.font.render(f"{yOff + 1}. {q['question']}",True,(0,0,0))
            
            xC = self.background.res[0] // 4
            yC = yOff * qRendered.get_height() * 6
            xH = self.font.size(f"{yOff + 1}. {q['question']}")[0]
            yH = self.font.size(f"{yOff + 1}. {q['question']}")[1]
            qRenderedRect = (xC,yC,xH,yH)
            qType = q["type"]
            self.qTextList.append((qRendered,qRenderedRect,qType))
            answers = []
            xOff = self.background.res[0] // 4


            #each question is a dictionary of question, question type, and answers
            #TODO: implement questionType, so we can choose multiple answers or single
            #FOR NOW

            #0: single answer
            #1: multiple answer
            #2: slider
            if qType < 2:
                for a in q["answers"]:
                    aRendered = self.font.render(a,True,(0,0,0))
                    aRenderedRect = (xOff, yC + qRendered.get_height() ,self.font.size(a)[0],self.font.size(a)[1])
                    answers.append((a,aRendered,aRenderedRect,False))
                    xOff += aRendered.get_width() + 20
            
                
            
            elif qType == 2:
                (x,y,lenX,lenY) = qRenderedRect
                #TODO: better currPos logic, currently multiplying by 11 to round upward to 10

                currVal = 0
                currValRender = self.font.render(f"0",True,(0,0,0))
                #ball should start at the start of the slider
                #stored as the center coord,radius,(lowLim,highLim),currVal,currValRender,Chosen
                answers.append(((self.background.res[0] // 4 + 20,y + qRendered.get_height() * 1.5),qRendered.get_height() / 2,(self.background.res[0] // 4 + 20,self.background.res[0] // 4 + 520),currVal,currValRender,False))
                #generate a ball

            
            self.aTextList.append(answers)
            yOff += 1
    

    def blitQuestions(self):
        self.background.screen.fill((255,255,255))

        yOff = 0

        #first, loop through question
        #inner loop loops through all the answers of the specific question
        for (q,qRect,qType) in self.qTextList:
            self.background.screen.blit(q,qRect)

            qTuple = (q,qRect,qType)
            #question and corresponding answers will share same index
            ansList = self.aTextList[yOff]

            self.blitAnswers(qTuple,ansList)
            

            yOff += 1

            
        
        

        #create a rectangle below the text
        #pygame.draw.rect(self.background.screen,(150,150,150),self.startRect)
        self.background.screen.blit(self.startText,self.startRect)

    def blitAnswers(self,qTup,ansList):
        (q,qRect,qType) = qTup
            

        for aa in ansList:
            if qType < 2:
                self.blitButtonAnswer(aa)
            elif qType == 2:
                self.blitSliderAnswer(qTup,aa)


    def blitButtonAnswer(self,aa):
        (_,ansRender,ansRect,_) = aa
        pygame.draw.rect(self.background.screen,(0,0,0),ansRect,1)
        self.background.screen.blit(ansRender,ansRect)


    def blitSliderAnswer(self,qTup,aa):
        (q,qRect,qType) = qTup
        (x,y,lenX,lenY) = qRect

        x = self.background.res[0] // 4

        (center,radius,(lowLim,highLim),currVal,currValRender,Chosen) = aa
        (cX,cY) = center

        #segment the bar into 11 spaces
        incr = (highLim - lowLim) / 10

        offset = 0

        for i in range(11): 

            #render number beforehand
            nRendered = self.font.render(f"{i}",True,(0,0,0))
            
            #blit number and bar here
            pygame.draw.rect(self.background.screen,(0,0,0),(x + offset + 10 + self.font.size(f'{i}')[0],y + q.get_height() * 2 - 10,1,10))
            #NOTE: uncomment if debug currVal
            #self.background.screen.blit(currValRender,(x + offset + 20,y + q.get_height() * 2 + 30,500,500))
            self.background.screen.blit(nRendered,(x + offset + 20,y + q.get_height() * 2,500,500))

            offset += incr
            

        #draw a progress bar + the circle to where the current position is
        #TODO: relative the rects
        pygame.draw.rect(self.background.screen,(0,0,0),(x + 10,y + q.get_height(),520,lenY),1)
        pygame.draw.rect(self.background.screen,(0,53,148),(x + 10,y + q.get_height(),cX - (x + 10),lenY))
        pygame.draw.circle(self.background.screen,(255,184,28),center,radius)
        #self.background.screen.blit(currValRender,(cX + radius,cY + radius,self.background.res[0],self.background.res[1]))
    
    
    #this is for after round is over
    def blitSumStats(self):

        #draw a smol rectangle to display stats
        #TODO: relativize the size
        pygame.draw.rect(self.background.screen,(200,200,200),(250,250,800,400),0)

        levelTxt = self.font.render(f"Level {self.level + 1} Round {self.round}/{self.rounds} finished!",True,(0,0,0))
        self.background.screen.blit(levelTxt,(250,250,self.background.res[0],self.background.res[1]))

        
        #pygame.draw.rect(self.background.screen,(150,150,150),(self.nextRoundRect[0],self.nextRoundRect[1],self.font.size('Next Round')[0],self.font.size('Next Round')[1]))
        self.background.screen.blit(self.nextText,self.nextRoundRect)

    
    def blitFinalStats(self,cList):
        self.background.screen.fill((255,255,255))
        levelTxt = self.font.render(f"Level {self.level + 1} finished!",True,(0,0,0))
        self.background.screen.blit(levelTxt,(0,0,self.background.res[0],self.background.res[1]))
        #yOff = 100

        #TODO: change the way the level class is maintained so we can do what is in the comment
        # rather than passing in the coin list
        #for agent in self.agents:
        #    currText = self.font.render(f"{agent.name} total coins: {agent.coins}",True,(0,0,0))
        #    self.background.screen.blit(currText,(0,yOff,self.background.res[0],self.background.res[1]))
        #    yOff += 100



        #NOTE: currently choosing to not display how many coins each player had obtained
        #pTxt = self.font.render(f"Player total coins: {cList[0]}",True,(0,0,0))
        #e1Txt = self.font.render(f"Enemy1 total coins: {cList[1]}",True,(0,0,0))
        #e2Txt = self.font.render(f"Enemy2 total coins: {cList[2]}",True,(0,0,0))
        #e3Txt = self.font.render(f"Enemy3 total coins: {cList[3]}",True,(0,0,0))

        #self.background.screen.blit(pTxt,(0,100,self.background.res[0],self.background.res[1]))
        #self.background.screen.blit(e1Txt,(0,200,self.background.res[0],self.background.res[1]))
        #self.background.screen.blit(e2Txt,(0,300,self.background.res[0],self.background.res[1]))
        #self.background.screen.blit(e3Txt,(0,400,self.background.res[0],self.background.res[1]))

        self.background.screen.blit(self.endLevelText,self.startRect)

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
            self.hoverMenuText(pygame.mouse.get_pos())
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.menuInteraction(pygame.mouse.get_pos())
                


            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: #Quitting out of fullScreen
                pygame.quit()
                exit()
        #moved outside the event loop to support holding mouse button
        if pygame.mouse.get_pressed()[0] == True: 
            self.sliderInteraction(pygame.mouse.get_pos())
    

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

    def hoverMenuText(self,mousePos):
        x,y = mousePos

        #starting game
        inX = x in range(self.startRect[0], self.startRect[0] + self.startRect[2])
        inY = y in range(self.startRect[1], self.startRect[1] + self.startRect[3])
        if (inX and inY):
            self.startText = self.font.render('Start',True,(0,255,0))
            self.endLevelText = self.font.render('End Level',True,(0,255,0))
        else: 
            self.startText = self.font.render('Start',True,(0,0,0))
            self.endLevelText = self.font.render('End Level',True,(0,0,0))

        #next round
        inX = x in range(self.nextRoundRect[0], self.nextRoundRect[0] + self.nextRoundRect[2])
        inY = y in range(self.nextRoundRect[1], self.nextRoundRect[1] + self.nextRoundRect[3])
        if (inX and inY):
            self.nextText = self.font.render('Next Round',True,(0,255,0))
        else:
            self.nextText = self.font.render('Next Round',True,(0,0,0))

    #defines all the menu interactions given mousepos
    def menuInteraction(self,mousePos):
        x,y = mousePos

        #starting game
        inX = x in range(self.startRect[0], self.startRect[0] + self.startRect[2])
        inY = y in range(self.startRect[1], self.startRect[1] + self.startRect[3])
        if (inX and inY):
            #check if all answered
            #if self.allAnswered():
            #    self.paused = False
            self.paused = False
            self.startText = self.font.render('Start',True,(0,255,0))
            self.endLevelText = self.font.render('End Level',True,(0,255,0))
        else: 
            self.startText = self.font.render('Start',True,(0,0,0))
            self.endLevelText = self.font.render('End Level',True,(0,0,0))

        #next round
        inX = x in range(self.nextRoundRect[0], self.nextRoundRect[0] + self.nextRoundRect[2])
        inY = y in range(self.nextRoundRect[1], self.nextRoundRect[1] + self.nextRoundRect[3])
        if (inX and inY):
            self.paused = False
            self.nextText = self.font.render('Next Round',True,(0,255,0))
        else:
            self.nextText = self.font.render('Next Round',True,(0,0,0))

        #answering questions - aTextList is indexed by the question number, list list of answers
        currInd1 = 0
        for aList in self.aTextList:
            

            (q,qRect,qType) = self.qTextList[currInd1]

            if qType < 2:
                currInd2 = 0

                for (ansTxt,ansRender,ansRect,choice) in aList:
                    inX = x in range(ansRect[0], ansRect[0] + ansRect[2])
                    inY = y in range(ansRect[1],ansRect[1] + ansRect[3])

                    if (inX and inY):

                        newChoice = not choice
                    
                        #before the answer is chosen, check the question type, and unchoose all other answers before hand if needed
                        if (qType == 0):
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

    def sliderInteraction(self,mousePos):
        x,y = mousePos

        #answering questions - aTextList is indexed by the question number, list list of answers
        currInd1 = 0
        for aList in self.aTextList:     

            (q,qRect,qType) = self.qTextList[currInd1]


            #Slider: move depending on mouse distance from center
            if qType == 2:
                (aCenter,aRadius,aLim,val,valRender,choice) = aList[0]

                #allow the mouse to be a little further out
                inX = aCenter[0] - aRadius * 4 < x and x < aCenter[0] + aRadius * 4
                inY = aCenter[1] - aRadius * 4 < y and y < aCenter[1] + aRadius * 4

                if inX and inY:

                    #set new center according to where mouse is in the circle
                    #make sure it does not go out of bounds
                    if x <= aLim[0] + aRadius:
                        newPos = aLim[0] + aRadius
                    elif x >= aLim[1]:
                        newPos = aLim[1]
                    else:
                        newPos = x
                    
                    #TODO: better currPos logic, currently multiplying by 11 to round upward to 10
                    #slider min/max
                    sMin = aLim[0] + aRadius
                    sMax = aLim[1]
                    currVal = (newPos - sMin) * 10 / (sMax - sMin)
                    #rounding lol
                    if currVal - int(currVal) > .7:
                        currVal = math.ceil(currVal)
                    elif currVal - int(currVal) < .3:
                        currVal = int(currVal)
                    currValRender = self.font.render(f"{currVal}",True,(0,0,0))

                    #use integer value as new center by recalculating with currVal
                    #calculated with the eqn used for currVal above
                    newCenter = ((currVal * (sMax- sMin) / 10) + sMin,aCenter[1])

                    self.aTextList[currInd1][0] = (newCenter,aRadius,aLim,currVal,currValRender,True)
            currInd1 += 1
        

class FinalScreen:
    def __init__(self, background):
        self.background = background
        self.size = int(min(self.background.res[0],self.background.res[1]) * 0.04)
        
        fontPath = path.join("fonts","arial.TTF")

        self.font = pygame.font.SysFont('arial', self.size)

        drawTxt = "You have completed the game! Press esc on your keyboard to exit."
        self.txt = self.font.render(drawTxt,True,(0,0,0))


    def draw(self):
        self.background.screen.fill((255,255,255))

        self.background.screen.blit(self.txt,(self.size // 2, self.size // 2))
    
    def mainLoop(self):
        
        while True:
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT: 
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: #Quitting out of fullScreen
                    pygame.quit()
                    exit()

            self.draw()

            pygame.display.flip()
            pygame.display.update()