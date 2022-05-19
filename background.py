import pygame
import math
from os import path
from configReader import *

from pygame.constants import QUIT

class Background(pygame.sprite.Sprite):
    def __init__(self,res,image = "pacman.png"):
        """
        It creates a surface object with the resolution of the screen, and then sets the
        caption of the window to "Privilege Recognition Task"
        
        Args:
          res: the resolution of the screen
          image: The image to load. Defaults to pacman.png
        """
        pygame.sprite.Sprite.__init__(self)
        self.res = res
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.surface = pygame.Surface(res)
        #self.image = self.imgLoad(image)

        pygame.display.set_caption("Privilege Recognition Task")

    def imgLoad(self,img):
        """
        It takes a string, and returns a pygame image object
        
        Args:
          img: The name of the image to load.
        
        Returns:
          The image is being returned.
        """

        print(f"loading {img}")

        asset_url = EXE.resource_path(f"images/objects/{img}")
        
        backImg = pygame.image.load(asset_url).convert_alpha()
        backImg = pygame.transform.scale(backImg,self.res)

        return backImg
    
    def draw(self):
        """
        It fills the screen with white
        """
        #fills a black screen
        self.screen.fill((255,255,255))
    
        #not a fan of this dark background :P
        #self.screen.blit(self.image,(0,0))

class HUD:
    def __init__(self, background, agents):
        """
        The function is a constructor that initializes the class HUD. It sets the background,
        agents, font, font size, and timer
        
        Args:
          background: The background image
          agents: a list of agents
        """
        self.background = background
        self.agents = agents
        #just the font size
        self.size = int(min(self.background.res[0],self.background.res[1]) * 0.04)
        
        fontPath = path.join("fonts","arial.TTF")

        self.fontHUD = pygame.font.SysFont('arial', self.size)
        self.timer = 0
    
    def updateTimer(self,time_passed):
        """
        The function updateTimer() takes in a parameter called time_passed, and adds to 
        the current amount of time passed
        
        Args:
          time_passed: The amount of time that has passed since the last time the function was
        called.
        """
        self.timer += time_passed

    def resetTimer(self):
        """Sets the time passed to 0
        """
        self.timer = 0

    def drawHUD(self):
        """
        It draws the timer on the screen
        """
        #UNCOMMENT IF WANT TO DISPLAY SCORES
        #i = 0
        #for agent in self.agents:
        #    coinTxt = self.fontHUD.render(f"{agent.name} coins: {agent.coins}",True,(0,0,0))
        #    self.background.screen.blit(coinTxt,(0,self.size * i))
        #    i += 1

        #Timer
        timerTxt = self.fontHUD.render(f"Time: {(self.timer // 1000)}" ,True,(0,0,0))
        timerRect = timerTxt.get_rect()
        timerRect.topright = (self.background.res[0],0)
        self.background.screen.blit(timerTxt,timerRect)

class StartScreen:
    def __init__(self,background):
        """
        The function takes the name the user has entered and saves it to a file. This 
        function also initiallizes the screen to select the experiment structure.
        
        Args:
          background: the background of the game
        """
        
        self.name = ""
        self.finished = False
        self.background = background
        self.size = int(min(self.background.res[0],self.background.res[1]) * 0.05)
        self.font = pygame.font.SysFont('arial',self.size)
        
        self.enterText = self.font.render("Please enter your name and press enter",True,(0,0,0),(255,255,255))
        self.nameText = self.font.render(self.name,True,(0,0,0),(100,0,200))
        self.menuRect = (50,50,self.background.res[0] - 100,self.background.res[1] - 100)

        #TODO: for now, adding another rect for the rectangle so that it is slightly bigger than text
        self.nameRect1 = (40 + self.background.res[0] // 5,40 + self.background.res[1] // 5,self.background.res[0] // 2,self.font.size("1")[1] + 20)
        self.nameRect = (50 + self.background.res[0] // 5,50 + self.background.res[1] // 5,self.background.res[0] // 2,self.font.size("1")[1])

        #Start game off with selecting config, then actually start game
        self.configSelect = True
        self.structRectList = []
        self.configSelectText = self.font.render("Choose Config",True,(0,0,0),(255,255,255))
        self.configSelectRect = (40 + self.background.res[0] // 5,40 + self.background.res[1] // 5,self.background.res[0] // 2,self.font.size("1")[1] + 20)

        #just do two structs as a proof of concept, otherwise, would be in a list
        self.struct1Text = self.font.render("Struct 0",True,(0,0,0),(255,255,255))
        self.struct1Rect = () 

        self.struct2Text = self.font.render("Struct 1",True,(0,0,0),(255,255,255))
        self.struct2Rect = (40 + self.background.res[0] // 5,self.background.res[1] // 2,self.background.res[0] // 2,self.font.size("1")[1] + 20) 

        self.structRectList = []
        self.structNameList = []

        for i in range(9):
            self.structRectList.append((40 + self.background.res[0] // 5,self.background.res[1] // 3 + 50 * i,self.background.res[0] // 2,self.font.size("1")[1] + 20))
            self.structNameList.append(self.font.render(f"Struct {i}",True,(0,0,0),(255,255,255)))

        self.chosenStruct = ""    

    def updateName(self):
        """
        It takes the name of the player and renders it to the screen
        """
        self.nameText = self.font.render(self.name,True,(0,0,0),(255,255,255))
        
    def mainLoop(self):
        self.drawAll()
        self.startInteraction()
        pygame.display.flip()
        pygame.display.update()
        
    def drawAll(self):
        """
        It draws the menu screen.
        """
        self.background.screen.fill((255,255,255))

        if self.configSelect:
            self.hover(pygame.mouse.get_pos())
            self.background.screen.blit(self.configSelectText,self.configSelectRect)

            for i in range(len(self.structRectList)):
                self.background.screen.blit(self.structNameList[i],self.structRectList[i])
            
        else:
            self.background.screen.blit(self.enterText,self.menuRect)
            pygame.draw.rect(self.background.screen,(0,0,0),self.nameRect1,1)
            self.background.screen.blit(self.nameText,self.nameRect)

    def hover(self,mousePos):
        """
        It takes the mouse position and checks if it's in the range of the rectangles. If it
        is, it changes the color of the text to green
        
        Args:
          mousePos: The position of the mouse
        """
        x,y = mousePos
        i = 0
        for rect in self.structRectList:
            xRange = range(rect[0],rect[0] + rect[2])
            yRange = range(rect[1],rect[1] + rect[3])

            inX = x in xRange
            inY = y in yRange
            if (inX and inY):
                self.structNameList[i] = self.font.render(f"Struct {i}",True,(0,255,0),(255,255,255))
            else:
                self.structNameList[i] = self.font.render(f"Struct {i}",True,(0,0,0),(255,255,255)) 
            i += 1



    def configSelection(self,mousePos): 
        """
        The function takes in a mouse position and checks if the mouse is in the range of any
        of the rectangles in the list. If it is, it sets the chosenStruct variable to the name
        of the structure
        
        Args:
          mousePos: the position of the mouse
        """
        i = 0
        x,y = mousePos

        #starting game
        for rect in self.structRectList:
            xRange = range(rect[0],rect[0]+rect[2])
            yRange = range(rect[1],rect[1] + rect[3])

            inX = x in xRange
            inY = y in yRange
            if (inX and inY):
                self.chosenStruct = f"structure{i}"
                self.configSelect = False
            i += 1 

    def startInteraction(self):
        """
        It's a function handles the input logic for this game
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: #Quitting out of fullScreen
                pygame.quit()
                exit()

            elif self.configSelect and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.configSelection(pygame.mouse.get_pos()) 
            elif not self.configSelect and event.type == pygame.KEYDOWN:
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
        """
        It's a function that initializes the round start screen or the question screen
        
        Args:
          level: the current level
          levels: the number of levels in the game
          round: the current round
          rounds: the number of rounds in the game
          background: a pygame.Surface object
          config: a dictionary of the config file
          agents: a list of agents
          levelStart: the time at which the level started. Defaults to 0
        """
        
        self.level = level
        self.round = round
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
 
        self.nextRect = (600, self.background.res[1] - 50 - self.font.size('Next')[1]) + self.font.size('Next')


        self.menuRect = (50,50,self.background.res[0] - 100,self.background.res[1] - 100)
        self.startRect = (self.background.res[0] * 3 // 4,self.background.res[1] * 9 // 10,self.font.size('Start')[0] + 20,self.font.size('Start')[1] + 20)
        self.nextRoundRect = (460,550,self.font.size('Next Round')[0] + 10,self.font.size('Next Round')[1] + 10)

        self.startText = self.font.render('Start',True,(0,0,0))
        self.nextText = self.font.render('Next Round',True,(0,0,0))
        self.endLevelText = self.font.render('End Level',True,(0,0,0))
        
    def returnQuestionText(self):
        """
        It takes a list of dictionaries, and returns a list of the values of the "question"
        key in each dictionary
        
        Returns:
          returns all question strings specified in the given config
        """
        retList = []
        for q in self.config["questions"]:
            retList.append(q["question"])
        return retList

    def returnAnswerText(self):
        """
        Parses values in the aTextList and qTextList arrays
        
        Returns:
          returns all answer strings specified in the given config
        """
        
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

    def allAnswered(self):
        """
        check that all questions given have been answered
        """
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
        """
        It renders the questions and answers to the screen. The logic for slider and text 
        response answers are different
        """
        
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
                
                #add each slider to list of things to be rendered 
                #stored as the center coord,radius,(lowLim,highLim),currVal,currValRender,Chosen
                answers.append(((self.background.res[0] // 4 + 26,y + qRendered.get_height() * 1.5),qRendered.get_height() / 2,(self.background.res[0] // 4 + 15,self.background.res[0] // 4 + 511),currVal,currValRender,False))
                #generate a ball

            self.aTextList.append(answers)
            yOff += 1
    

    def blitQuestions(self):
        """
        It loops through a list of questions and answers and blits them to the screen.
        """
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
        """
        It takes a question tuple and a list of answers and decides how to blit them
        
        Args:
          qTup: (question, questionRect, questionType)
          ansList: a list of tuples, each tuple containing the answer text, the answer rect,
        and the answer type (0,1,2)
        """
        (q,qRect,qType) = qTup

        for aa in ansList:
            if qType < 2:
                self.blitButtonAnswer(aa)
            elif qType == 2:
                self.blitSliderAnswer(qTup,aa)


    def blitButtonAnswer(self,aa):
        """
        It draws a rectangle around the answer and then blits the answer onto the screen
        
        Args:
          aa: a tuple containing the following:
        """
        (_,ansRender,ansRect,_) = aa
        pygame.draw.rect(self.background.screen,(0,0,0),ansRect,1)
        self.background.screen.blit(ansRender,ansRect)


    def blitSliderAnswer(self,qTup,aa):
        """
        It draws a slider bar with a circle on it that can be moved by the user
        
        Args:
          qTup: (q,qRect,qType)
          aa: (center,radius,(lowLim,highLim),currVal,currValRender,Chosen)
        """
        
        (q,qRect,qType) = qTup
        (x,y,lenX,lenY) = qRect

        x = self.background.res[0] // 4

        (center,radius,(lowLim,highLim),currVal,currValRender,Chosen) = aa
        (cX,cY) = center

        #segment the bar into 11 spaces
        incr = (highLim - lowLim) / 10

        offset = 0

        for i in range(11): 
            
            #for some reason 10 is 5 pixels off probably due to rounding
            if i == 10:
                offset -= 5
            #render number beforehand
            nRendered = self.font.render(f"{i}",True,(0,0,0))
            
            #blit number and bar here
            pygame.draw.rect(self.background.screen,(0,0,0),(x + offset + 20 + self.font.size(f'{i}')[0]//2,y + q.get_height() * 2 - 10,1,10))
            #NOTE: uncomment if debug currVal
            #self.background.screen.blit(currValRender,(x + offset + 20,y + q.get_height() * 2 + 30,500,500))
            
            self.background.screen.blit(nRendered,(x + offset + 21,y + q.get_height() * 2,500,500))
            
            offset += incr
            
        #draw a progress bar + the circle to where the current position is
        pygame.draw.rect(self.background.screen,(0,0,0),(x + 10,y + q.get_height(),520,lenY),1)
        pygame.draw.rect(self.background.screen,(0,53,148),(x + 10,y + q.get_height(),cX - (x + 10),lenY))
        pygame.draw.circle(self.background.screen,(255,184,28),center,radius)
        #self.background.screen.blit(currValRender,(cX + radius,cY + radius,self.background.res[0],self.background.res[1]))
    
    
    #this is for after round is over
    def blitSumStats(self):
        """
        It draws a rectangle and then draws the summary statistics on top of it
        """

        #draw a smol rectangle to display stats
        #TODO: relativize the size
        pygame.draw.rect(self.background.screen,(200,200,200),(250,250,800,400),0)

        levelTxt = self.font.render(f"Level {self.level + 1} Round {self.round}/{self.rounds} finished!",True,(0,0,0))
        self.background.screen.blit(levelTxt,(250,250,self.background.res[0],self.background.res[1]))

        #pygame.draw.rect(self.background.screen,(150,150,150),(self.nextRoundRect[0],self.nextRoundRect[1],self.font.size('Next Round')[0],self.font.size('Next Round')[1]))
        self.background.screen.blit(self.nextText,self.nextRoundRect)

    
    def blitFinalStats(self,cList):
        """
        Displays the final stats of the game
        
        Args:
          cList: list of all the characters in the game
        """
        
        self.background.screen.fill((255,255,255))
        levelTxt = self.font.render(f"Level {self.level + 1} finished!",True,(0,0,0))
        self.background.screen.blit(levelTxt,(0,0,self.background.res[0],self.background.res[1]))

        
        self.background.screen.blit(self.endLevelText,self.startRect)

    def updateLoop(self,x=[]):
        self.drawAll(x)
        self.startInteraction()


        pygame.display.flip()
        pygame.display.update()


    #custom designed for start menu
    def startInteraction(self):
        """
        It checks for mouse events and keyboard events. If the mouse is clicked, it checks if
        the mouse is hovering over a menu item. If it is, it calls the menuInteraction
        function. If the mouse is clicked and held, it calls the sliderInteraction function.
        If the escape key is pressed, it quits the program
        """

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
        """
        Chooses different blit functions depending on levelStart variable
        
        Args:
          x: the number of questions answered correctly
        """
        if self.levelStart == 0:
            self.blitQuestions()
        elif self.levelStart == 1:
            #display some summary stats
            self.blitSumStats()
        else:
            self.blitFinalStats(x)

    def hoverMenuText(self,mousePos):
        """
        It's a function that changes the color of the text in the menu depending on whether
        the mouse is hovering over it or not
        
        Args:
          mousePos: (x,y)
        """
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
        """
        The function takes in a mouse position, and checks if the mouse is hovering over any
        of the buttons on the screen. If it is, it changes the color of the button to green.
        If it is not, it changes the color of the button to black
        
        Args:
          mousePos: the position of the mouse
        """
        x,y = mousePos

        #starting game
        inX = x in range(self.startRect[0], self.startRect[0] + self.startRect[2])
        inY = y in range(self.startRect[1], self.startRect[1] + self.startRect[3])
        if (inX and inY):
            #check if all answered
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
        """
        The function takes in the mouse position and checks if the mouse is within the
        slider's bounds. If it is, it calculates the new slider position and updates the
        slider's center position
        
        Args:
          mousePos: (x,y) tuple of mouse position
        """
        x,y = mousePos

        #answering questions - aTextList is indexed by the question number, list list of answers
        for currInd1, aList in enumerate(self.aTextList):     
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
                    sMin = aLim[0] + aRadius -1
                    sMax = aLim[1] + aRadius 
                    currVal = (newPos - sMin) * 10 / (sMax - sMin)
                    #rounding lol
                    if currVal - int(currVal) >= .5:
                        currVal = math.ceil(currVal)
                    elif currVal - int(currVal) < .5:
                        currVal = int(currVal)
                    currValRender = self.font.render(f"{currVal}",True,(0,0,0))

                    #use integer value as new center by recalculating with currVal
                    #calculated with the eqn used for currVal above
                    newCenter = ((currVal * (sMax- sMin) / 10) + sMin,aCenter[1])

                    self.aTextList[currInd1][0] = (newCenter,aRadius,aLim,currVal,currValRender,True)
            
        

class FinalScreen:
    def __init__(self, background):
        """
        Initializes the end screen for the game
        
        Args:
          background: The background object that the text will be drawn on.
        """
        self.background = background
        self.size = int(min(self.background.res[0],self.background.res[1]) * 0.04)
        
        fontPath = path.join("fonts","arial.TTF")

        self.font = pygame.font.SysFont('arial', self.size)

        drawTxt = "You have completed the game! Press esc on your keyboard to exit."
        self.txt = self.font.render(drawTxt,True,(0,0,0))


    def draw(self):
        """
        The function draws the background of the screen white, then draws the text in the
        middle of the screen
        """
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