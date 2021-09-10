def startInteraction(self):

        for event in pygame.event.get():
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.menuInteraction(pygame.mouse.get_pos())


            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: #Quitting out of fullScreen
                pygame.quit()
                exit()
        #moved outside the event loop to support holding mouse button
        if pygame.mouse.get_pressed()[0] == True: 
            self.sliderInteraction(pygame.mouse.get_pos())
    
#defines all the menu interactions given mousepos
    def menuInteraction(self,mousePos):
        x,y = mousePos

        #starting game
        inX = x in range(self.startRect[0], self.startRect[0] + self.startRect[2])
        inY = y in range(self.startRect[1], self.startRect[1] + self.startRect[3])
        if (inX and inY):
            
            #check if all answered
            if self.allAnswered():
                self.paused = False
            



        #starting game
        inX = x in range(self.nextRoundRect[0], self.nextRoundRect[0] + self.nextRoundRect[2])
        inY = y in range(self.nextRoundRect[1], self.nextRoundRect[1] + self.nextRoundRect[3])
        if (inX and inY):
            if self.allAnswered():
                self.paused = False

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

                        print(newChoice)

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
                inX = aCenter[0] - aRadius * 2 < x and x < aCenter[0] + aRadius * 2
                inY = aCenter[1] - aRadius * 2 < y and y < aCenter[1] + aRadius * 2

                if inX and inY:

                    #set new center according to where mouse is in the circle
                    if x <= aLim[0]:
                        newPos = aLim[0]
                    elif x >= aLim[1]:
                        newPos = aLim[1]
                    else:
                        newPos = x
                    
                                        #TODO: better currPos logic, currently multiplying by 11 to round upward to 10
                    #slider min/max
                    sMin = aLim[0]
                    sMax = aLim[1]
                    currVal = int ((newPos - sMin) * 11 / sMax)
                    currValRender = self.font.render(f"{currVal}",True,(0,0,0))

                    self.aTextList[currInd1][0] = ((newPos,aCenter[1]),aRadius,aLim,currVal,currValRender,True)
            currInd1 += 1