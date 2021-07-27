import pygame 
from os import path

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
    def __init__(self, background, agents):
        self.background = background
        self.agents = agents
        self.size = int(min(self.background.res[0],self.background.res[1]) * 0.04)
        self.fontHUD = pygame.font.SysFont('arial', self.size)
        self.timer = 0
        self.baseTime = 0
    
    def updateTimer(self):
        self.timer = pygame.time.get_ticks() - self.baseTime

    def resetTimer(self):
        self.baseTime = pygame.time.get_ticks()

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
