import pygame
from background import *
from objects import *


#TODO: repurpose as "level" class so we can have multiple levels
class PAT:
    def __init__(self):
        #TODO: fixed coins for now
        self.coinsLeft = 30

        #TODO: fixed coins for now
        self.coinsLeft = 30

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

        self.player = Player(self.background,self.aGroup,(self.res[0] // 4, self.res[1] // 4), "p1.png")
        
        #TODO: change the temporary spawn points of enemies, and change sprite
        # aaand make it so this is less disgusting code
        self.enemy1 = Enemy("enemy1",self.background,self.aGroup,self.cGroup,(3 * self.res[0] // 4,self.res[1] // 4),"p2.png")

        self.enemy2 = Enemy("enemy2",self.background,self.aGroup,self.cGroup,(self.res[0] // 4,3 * self.res[1] // 4),"p3.png")
        
        self.enemy3 = Enemy("enemy3",self.background,self.aGroup,self.cGroup,(3 * self.res[0] // 4,3 * self.res[1] // 4),"p4.png")

        self.eGroup.add(self.enemy1)
        self.eGroup.add(self.enemy2)
        self.eGroup.add(self.enemy3)

        #Pass background and player into HUD
        self.HUD = HUD(self.background, self.aGroup) 

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
            if self.coinsLeft > 0: e.randomWalk(self.HUD.timer)
                

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

    





