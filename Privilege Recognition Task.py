#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install pygame')

import pygame, sys, os, random

import random

from pygame.locals import *

N0_WX = 0
USER_NAME = "Participant"

#Joystick settings
JS_DEVNUM=0 
JS_XAXIS=0 
JS_YAXIS=1 
JS_STARTBUTTON=0

pygame.mixer.pre_init(22050,16,2,512)
JS_STARTBUTTON=0 
pygame.mixer.init()

clock = pygame.time.Clock()
pygame.init()

window = pygame.display.set_mode((1, 1))
pygame.display.set_caption("Coin Gatherer")

screen = pygame.display.get_surface()

class game ():
    def default_high_score_list(self):
        return [(100, "Participant 2"), (75, "Participant 3"), (50, "Participant 4")]
    def getplayername(self):
            """Ask the player their name, to go on the high-score list."""
            if NO_WX: return USER_NAME
            try:
              import wx
            except:
              print("Error: No module wx. Can not ask the user their name!")
              return USER_NAME
            app=wx.App(None)
            dlog=wx.TextEntryDialog(None,"You made the high-score list! Name:")
            dlog.ShowModal()
            name=dlog.GetValue()
            dlog.Destroy()
            app.Destroy()
            return name
              
    def updatehiscores(self,newscore):
            """Add newscore to the high score list, if appropriate."""
            hs=self.gethiscores()
            for line in hs:
              if newscore>=line[0]:
                hs.insert(hs.index(line),(newscore,self.getplayername()))
                hs.pop(-1)
                break
            self.writehiscores(hs)
    def __init__ (self):
        self.levelNum = 0
        self.score = 0
        self.lives = 3
        self.mode = 0
        self.modeTimer = 0
        
        self.SetMode( 3 )
        
        # camera variables
        self.screenPixelPos = (0, 0) 
        self.screenNearestTilePos = (0, 0) 
        self.screenPixelOffset = (0, 0) 
        
        self.screenTileSize = (23, 21)
        self.screenSize = (self.screenTileSize[1] * 16, self.screenTileSize[0] * 16)
    
    def Move (self):
        self.x += self.velX
        self.y += self.velY
        
        self.nearestRow = int(((self.y + 8) / 16))
        self.nearestCol = int(((self.x + 8) / 16))

        if (self.x % 16) == 0 and (self.y % 16) == 0:
            if (self.currentPath):
                self.currentPath = self.currentPath[1:]
                self.FollowNextPathWay()
        
            else:
                self.x = self.nearestCol * 16
                self.y = self.nearestRow * 16
                
class coin ():
    def __init__ (self):
        self.slowTimer = 0
        self.x = -16
        self.y = -16
        self.velX = 0
        self.velY = 0
        self.speed = 1
        self.active = False
        
        self.bouncei = 0
        self.bounceY = 0
        
        self.nearestRow = (-1, -1)
        self.nearestCol = (-1, -1)
        
        self.imCoin = {}
        for i in range(0, 5, 1):
            self.imCoin[i] = pygame.image.load(os.path.join(pygame.draw.circle(screen, 255, 255, 0, random.randint(1,1000), 2),"res","sprite","fruit " + str(i) + ".gif")).convert()
        
        self.currentPath = ""
        self.coinType = 1
        
    def Draw (self):
        
        if thisGame.mode == 3 or self.active == False:
            return False
        
        screen.blit (self.imCoin[ self.coinType ], (self.x - thisGame.screenPixelPos[0], self.y - thisGame.screenPixelPos[1] - self.bounceY))

            
    def Move (self):
        
        if self.active == False:
            return False
        
        self.bouncei += 1
        if self.bouncei == 1:
            self.bounceY = 2
        elif self.bouncei == 2:
            self.bounceY = 4
        elif self.bouncei == 3:
            self.bounceY = 5
        elif self.bouncei == 4:
            self.bounceY = 5
        elif self.bouncei == 5:
            self.bounceY = 6
        elif self.bouncei == 6:
            self.bounceY = 6
        elif self.bouncei == 9:
            self.bounceY = 6
        elif self.bouncei == 10:
            self.bounceY = 5
        elif self.bouncei == 11:
            self.bounceY = 5
        elif self.bouncei == 12:
            self.bounceY = 4
        elif self.bouncei == 13:
            self.bounceY = 3
        elif self.bouncei == 14:
            self.bounceY = 2
        elif self.bouncei == 15:
            self.bounceY = 1
        elif self.bouncei == 16:
            self.bounceY = 0
            self.bouncei = 0
            snd_coinbounce.play()
        
        self.slowTimer += 1
        if self.slowTimer == 2:
            self.slowTimer = 0
            
            self.x += self.velX
            self.y += self.velY
            
            self.nearestRow = int(((self.y + 8) / 16))
            self.nearestCol = int(((self.x + 8) / 16))

            if (self.x % 16) == 0 and (self.y % 16) == 0:
                
                if len(self.currentPath) > 0:
                    self.currentPath = self.currentPath[1:]
                    self.FollowNextPathWay()
            
                else:
                    self.x = self.nearestCol * 16
                    self.y = self.nearestRow * 16
                    
                    self.active = False
                    thisGame.coinTimer = 0
                    
class player ():
    
    def __init__ (self):
        self.x = 0
        self.y = 0
        self.velX = 0
        self.velY = 0
        self.speed = 2
        
        self.nearestRow = 0
        self.nearestCol = 0
        
        self.homeX = 0
        self.homeY = 0
        
        self.pelletSndNum = 0
        
    def Move (self):
        
        self.nearestRow = int(((self.y + 8) / 16))
        self.nearestCol = int(((self.x + 8) / 16))

        if not thisLevel.CheckIfHitWall(self.x + self.velX, self.y + self.velY, self.nearestRow, self.nearestCol):
            self.x += self.velX
            self.y += self.velY

            thisLevel.CheckIfHitSomething(self.x, self.y, self.nearestRow, self.nearestCol)
            
           
           
            if thisCoin.active == True:
                if thisLevel.CheckIfHit( self.x, self.y, thisFruit.x, thisFruit.y, 8):
                    thisGame.AddToScore(2500)
                    thisCoin.active = False
                    thisGame.coinTimer = 0
                    thisGame.coinScoreTimer = 120
                    snd_coin.play()
        
        else:
            self.velX = 0
            self.velY = 0
            
        thisGame.coinTimer += 1
        if thisGame.coinTimer == 500:
            pathwayPair = thisLevel.GetPathwayPairPos()
            
            if not pathwayPair == False:
            
                pathwayEntrance = pathwayPair[0]
                pathwayExit = pathwayPair[1]
                
                thisCoin.active = True
                
                thisCoin.nearestRow = pathwayEntrance[0]
                thisCoin.nearestCol = pathwayEntrance[1]
                
                thisCoin.x = thisCoin.nearestCol * 16
                thisCoin.y = thisCoin.nearestRow * 16
                
                thisCoin.currentPath = path.FindPath( (thisCoin.nearestRow, thisCoin.nearestCol), pathwayExit )
                thisCoin.FollowNextPathWay()
            
        if thisGame.coinScoreTimer > 0:
            thisGame.coinScoreTimer -= 1
            
        
    def Draw (self):
        
        if thisGame.mode == 3:
            return False
            
        screen.blit (self.draw.surf.get_rect(), (self.x - thisGame.screenPixelPos[0], self.y - thisGame.screenPixelPos[1]))
        
class level ():
    
    def __init__ (self):
        self.lvlWidth = 0
        self.lvlHeight = 0
        self.edgeLightColor = (255, 255, 0, 255)
        self.edgeShadowColor = (255, 150, 0, 255)
        self.fillColor = (0, 255, 255, 255)
        self.pelletColor = (255, 255, 255, 255)
        
        self.map = {}
        
        self.pellets = 0
        self.powerPelletBlinkTimer = 0
        
    def SetMapTile (self, row, col, newValue):
        self.map[ (row * self.lvlWidth) + col ] = newValue
        
    def GetMapTile (self, row, col):
        if row >= 0 and row < self.lvlHeight and col >= 0 and col < self.lvlWidth:
            return self.map[ (row * self.lvlWidth) + col ]
        else:
            return 0
    
    def IsWall (self, row, col):
    
        if row > thisLevel.lvlHeight - 1 or row < 0:
            return True
        
        if col > thisLevel.lvlWidth - 1 or col < 0:
            return True
    
        # check the offending tile ID
        result = thisLevel.GetMapTile(row, col)

        # if the tile was a wall
        if result >= 100 and result <= 199:
            return True
        else:
            return False
    
                    
    def CheckIfHitWall (self, possiblePlayerX, possiblePlayerY, row, col):
    
        numCollisions = 0
        
        # check each of the 9 surrounding tiles for a collision
        for iRow in range(row - 1, row + 2, 1):
            for iCol in range(col - 1, col + 2, 1):
            
                if  (possiblePlayerX - (iCol * 16) < 16) and (possiblePlayerX - (iCol * 16) > -16) and (possiblePlayerY - (iRow * 16) < 16) and (possiblePlayerY - (iRow * 16) > -16):
                    
                    if self.IsWall(iRow, iCol):
                        numCollisions += 1
                        
        if numCollisions > 0:
            return True
        else:
            return False
        
        
    def CheckIfHit (self, playerX, playerY, x, y, cushion):
    
        if (playerX - x < cushion) and (playerX - x > -cushion) and (playerY - y < cushion) and (playerY - y > -cushion):
            return True
        else:
            return False


    def CheckIfHitSomething (self, playerX, playerY, row, col):
    
        for iRow in range(row - 1, row + 2, 1):
            for iCol in range(col - 1, col + 2, 1):
            
                if  (playerX - (iCol * 16) < 16) and (playerX - (iCol * 16) > -16) and (playerY - (iRow * 16) < 16) and (playerY - (iRow * 16) > -16):
                    # check the offending tile ID
                    result = thisLevel.GetMapTile(iRow, iCol)
        
                    if result == tileID[ 'pellet' ]:
                        # got a pellet
                        thisLevel.SetMapTile(iRow, iCol, 0)
                        snd_pellet[player.pelletSndNum].play()
                        player.pelletSndNum = 1 - player.pelletSndNum
                        
                        thisLevel.pellets -= 1
                        
                        thisGame.AddToScore(10)
                        
                        if thisLevel.pellets == 0:
                            # no more pellets left!
                            # WON THE LEVEL
                            thisGame.SetMode( 6 )
                            
                        
                    elif result == tileID[ 'pellet-power' ]:
                        # got a power pellet
                        thisLevel.SetMapTile(iRow, iCol, 0)
                        snd_powerpellet.play()
                        
                        thisGame.AddToScore(100)
                        thisGame.ghostValue = 200
                        
                        thisGame.ghostTimer = 360
                        for i in range(0, 4, 1):
                            if ghosts[i].state == 1:
                                ghosts[i].state = 2
                        
                    elif result == tileID[ 'door-h' ]:
                        # ran into a horizontal door
                        for i in range(0, thisLevel.lvlWidth, 1):
                            if not i == iCol:
                                if thisLevel.GetMapTile(iRow, i) == tileID[ 'door-h' ]:
                                    player.x = i * 16
                                    
                                    if player.velX > 0:
                                        player.x += 16
                                    else:
                                        player.x -= 16
                                        
                    elif result == tileID[ 'door-v' ]:
                        # ran into a vertical door
                        for i in range(0, thisLevel.lvlHeight, 1):
                            if not i == iRow:
                                if thisLevel.GetMapTile(i, iCol) == tileID[ 'door-v' ]:
                                    player.y = i * 16
                                    
                                    if player.velY > 0:
                                        player.y += 16
                                    else:
                                        player.y -= 16
                                        
   
        
    def PrintMap (self):
        
        for row in range(0, self.lvlHeight, 1):
            outputLine = ""
            for col in range(0, self.lvlWidth, 1):
            
                outputLine += str( self.GetMapTile(row, col) ) + ", "
                
            # print outputLine
            
   
    def LoadLevel (self, levelNum):
        
        self.map = {}
        
        self.pellets = 0
        
        f = open(os.path.join(SCRIPT_PATH,"res","levels",str(levelNum) + ".txt"), 'r')
        lineNum=-1
        rowNum = 0
        useLine = False
        isReadingLevelData = False
          
        for line in f:

          lineNum += 1
        
            # print " ------- Level Line " + str(lineNum) + " -------- "
          while len(line)>0 and (line[-1]=="\n" or line[-1]=="\r"): line=line[:-1]
          while len(line)>0 and (line[0]=="\n" or line[0]=="\r"): line=line[1:]
          str_splitBySpace = line.split(' ')
            
            
          j = str_splitBySpace[0]
                
          if (j == "'" or j == ""):
                # comment / whitespace line
                # print " ignoring comment line.. "
                useLine = False
          elif j == "#":
                # special divider / attribute line
                useLine = False
                
                firstWord = str_splitBySpace[1]
                
                if firstWord == "lvlwidth":
                    self.lvlWidth = int( str_splitBySpace[2] )
                    # print "Width is " + str( self.lvlWidth )
                    
                elif firstWord == "lvlheight":
                    self.lvlHeight = int( str_splitBySpace[2] )
                    # print "Height is " + str( self.lvlHeight )
                    
                elif firstWord == "edgecolor":
                    # edge color keyword for backwards compatibility (single edge color) mazes
                    red = int( str_splitBySpace[2] )
                    green = int( str_splitBySpace[3] )
                    blue = int( str_splitBySpace[4] )
                    self.edgeLightColor = (red, green, blue, 255)
                    self.edgeShadowColor = (red, green, blue, 255)
                    
                elif firstWord == "edgelightcolor":
                    red = int( str_splitBySpace[2] )
                    green = int( str_splitBySpace[3] )
                    blue = int( str_splitBySpace[4] )
                    self.edgeLightColor = (red, green, blue, 255)
                    
                elif firstWord == "edgeshadowcolor":
                    red = int( str_splitBySpace[2] )
                    green = int( str_splitBySpace[3] )
                    blue = int( str_splitBySpace[4] )
                    self.edgeShadowColor = (red, green, blue, 255)
                
                elif firstWord == "fillcolor":
                    red = int( str_splitBySpace[2] )
                    green = int( str_splitBySpace[3] )
                    blue = int( str_splitBySpace[4] )
                    self.fillColor = (red, green, blue, 255)
                    
                elif firstWord == "pelletcolor":
                    red = int( str_splitBySpace[2] )
                    green = int( str_splitBySpace[3] )
                    blue = int( str_splitBySpace[4] )
                    self.pelletColor = (red, green, blue, 255)
                    
                elif firstWord == "fruittype":
                    thisFruit.fruitType = int( str_splitBySpace[2] )
                    
                elif firstWord == "startleveldata":
                    isReadingLevelData = True
                        # print "Level data has begun"
                    rowNum = 0
                    
                elif firstWord == "endleveldata":
                    isReadingLevelData = False
                    # print "Level data has ended"
                    
          else:
                useLine = True
                
                
            # this is a map data line   
          if useLine == True:
                
                if isReadingLevelData == True:
                        
                    # print str( len(str_splitBySpace) ) + " tiles in this column"
                    
                    for k in range(0, self.lvlWidth, 1):
                        self.SetMapTile(rowNum, k, int(str_splitBySpace[k]) )
                        
                        thisID = int(str_splitBySpace[k])
                        if thisID == 4: 
                            # starting position for pac-man
                            
                            player.homeX = k * 16
                            player.homeY = rowNum * 16
                            self.SetMapTile(rowNum, k, 0 )
                            
                        elif thisID >= 10 and thisID <= 13:
                            # one of the ghosts
                            
                            ghosts[thisID - 10].homeX = k * 16
                            ghosts[thisID - 10].homeY = rowNum * 16
                            self.SetMapTile(rowNum, k, 0 )
                        
                        elif thisID == 2:
                            # pellet
                            
                            self.pellets += 1
                            
                    rowNum += 1
                    
                
        # reload all tiles and set appropriate colors
        GetCrossRef()

        # load map into the pathfinder object
        path.ResizeMap( self.lvlHeight, self.lvlWidth )
        
        for row in range(0, path.size[0], 1):
            for col in range(0, path.size[1], 1):
                if self.IsWall( row, col ):
                    path.SetType( row, col, 1 )
                else:
                    path.SetType( row, col, 0 )
        
        # do all the level-starting stuff
        self.Restart()
        
def Restart (self):
            
        thisCoin.active = False
            
        thisGame.coinTimer = 0

        player.x = player.homeX
        player.y = player.homeY
        player.velX = 0
        player.velY = 0
        


def CheckIfCloseButton(events):
    for event in events: 
        if event.type == pygame.QUIT: 
            sys.exit(0)


def CheckInputs(): 
    
    if thisGame.mode == 1:
        if pygame.key.get_pressed()[ pygame.K_RIGHT ] or (js!=None and js.get_axis(JS_XAXIS)>0):
            if not thisLevel.CheckIfHitWall(player.x + player.speed, player.y, player.nearestRow, player.nearestCol): 
                player.velX = player.speed
                player.velY = 0
                
        elif pygame.key.get_pressed()[ pygame.K_LEFT ] or (js!=None and js.get_axis(JS_XAXIS)<0):
            if not thisLevel.CheckIfHitWall(player.x - player.speed, player.y, player.nearestRow, player.nearestCol): 
                player.velX = -player.speed
                player.velY = 0
            
        elif pygame.key.get_pressed()[ pygame.K_DOWN ] or (js!=None and js.get_axis(JS_YAXIS)>0):
            if not thisLevel.CheckIfHitWall(player.x, player.y + player.speed, player.nearestRow, player.nearestCol): 
                player.velX = 0
                player.velY = player.speed
            
        elif pygame.key.get_pressed()[ pygame.K_UP ] or (js!=None and js.get_axis(JS_YAXIS)<0):
            if not thisLevel.CheckIfHitWall(player.x, player.y - player.speed, player.nearestRow, player.nearestCol):
                player.velX = 0
                player.velY = -player.speed
                
    if pygame.key.get_pressed()[ pygame.K_ESCAPE ]:
        sys.exit(0)
            
    elif thisGame.mode == 3:
        if pygame.key.get_pressed()[ pygame.K_RETURN ] or (js!=None and js.get_button(JS_STARTBUTTON)):
            thisGame.StartNewGame()
        

player = player()

thisCoin = coin()

tileIDName = {} # gives tile name (when the ID# is known)
tileID = {} # gives tile ID (when the name is known)
tileIDImage = {} # gives tile image (when the ID# is known)

# create game and level objects and load first level
thisGame = game()
thisLevel = level()
thisLevel.LoadLevel( thisGame.GetLevelNum() )

window = pygame.display.set_mode( thisGame.screenSize, pygame.DOUBLEBUF | pygame.HWSURFACE )

# initialise the joystick
if pygame.joystick.get_count()>0:
  if JS_DEVNUM<pygame.joystick.get_count(): js=pygame.joystick.Joystick(JS_DEVNUM)
  else: js=pygame.joystick.Joystick(0)
  js.init()
else: js=None

while True: 

    CheckIfCloseButton( pygame.event.get() )
    
    if thisGame.mode == 1:
        # normal gameplay mode
        CheckInputs()
        
        thisGame.modeTimer += 1
        player.Move()
        for i in range(0, 4, 1):
            thisCoin.Move()
            
    elif thisGame.mode == 2:
        # waiting after getting hit by a ghost
        thisGame.modeTimer += 1
        
        if thisGame.modeTimer == 90:
            thisLevel.Restart()
            
            thisGame.lives -= 1
            if thisGame.lives == -1:
                thisGame.updatehighscores(thisGame.score)
                thisGame.SetMode( 3 )
                thisGame.drawmidgamehiscores()
            else:
                thisGame.SetMode( 4 )
                
    elif thisGame.mode == 3:
        # game over
        CheckInputs()
            
    elif thisGame.mode == 4:
        # waiting to start
        thisGame.modeTimer += 1
        
        if thisGame.modeTimer == 90:
            thisGame.SetMode( 1 )
            player.velX = player.speed
            
    elif thisGame.mode == 5:
        # brief pause after munching a vulnerable ghost
        thisGame.modeTimer += 1
        
        if thisGame.modeTimer == 30:
            thisGame.SetMode( 1 )
            
    elif thisGame.mode == 6:
        # pause after eating all the pellets
        thisGame.modeTimer += 1
        
        if thisGame.modeTimer == 60:
            thisGame.SetMode( 7 )
            oldEdgeLightColor = thisLevel.edgeLightColor
            oldEdgeShadowColor = thisLevel.edgeShadowColor
            oldFillColor = thisLevel.fillColor
            
    elif thisGame.mode == 7:
        # flashing maze after finishing level
        thisGame.modeTimer += 1
        
        whiteSet = [10, 30, 50, 70]
        normalSet = [20, 40, 60, 80]
        
        if not whiteSet.count(thisGame.modeTimer) == 0:
            # member of white set
            thisLevel.edgeLightColor = (255, 255, 255, 255)
            thisLevel.edgeShadowColor = (255, 255, 255, 255)
            thisLevel.fillColor = (0, 0, 0, 255)
            GetCrossRef()
        elif not normalSet.count(thisGame.modeTimer) == 0:
            # member of normal set
            thisLevel.edgeLightColor = oldEdgeLightColor
            thisLevel.edgeShadowColor = oldEdgeShadowColor
            thisLevel.fillColor = oldFillColor
            GetCrossRef()
        elif thisGame.modeTimer == 150:
            thisGame.SetMode ( 8 )
            
    elif thisGame.mode == 8:
        # blank screen before changing levels
        thisGame.modeTimer += 1
        if thisGame.modeTimer == 10:
            thisGame.SetNextLevel()

    thisGame.SmartMoveScreen()
    
    screen.blit(img_Background, (0, 0))
    
    if not thisGame.mode == 8:
        thisLevel.DrawMap()
        
        if thisGame.coinScoreTimer > 0:
            if thisGame.modeTimer % 2 == 0:
                thisGame.DrawNumber (2500, thisCoin.x - thisGame.screenPixelPos[0] - 16, thisCoin.y - thisGame.screenPixelPos[1] + 4)

        for i in range(0, 4, 1):
            thisCoin.Draw()
        player.Draw()
        
        if thisGame.mode == 3:
                screen.blit(thisGame.imHiscores,(32,256))
        
    if thisGame.mode == 5:
        thisGame.DrawNumber (player.x - thisGame.screenPixelPos[0] - 4, player.y - thisGame.screenPixelPos[1] + 6)
    
    
    
    thisGame.DrawScore()
    
    pygame.display.flip()
    
    clock.tick (60)


# In[2]:


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((128,128,128))
        self.rect = self.surf.get_rect()
        

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((20, 10))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(800 + 20, 800 + 100),
                random.randint(0, 800),
            )
        )
        self.speed = random.randint(5, 20)
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

run = True


while run:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
            
        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
            
    screen.fill((255,255,255))
    pygame.draw.circle(screen, (0,0,255), (400,400), 400)
    
    pressed_keys = pygame.key.get_pressed()
   
    player.update(pressed_keys)
    
    enemies.update()
    
    screen.blit(player.surf, player.rect)

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
        
    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        running = False
    
    pygame.display.flip()
    
pygame.quit()


# In[ ]:





# In[ ]:




