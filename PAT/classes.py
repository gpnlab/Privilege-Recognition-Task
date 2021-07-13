import pygame
import random
from os import path

class PAT:
    def __init__(self):
        #fixed res for now (TODO)
        self.res = (800,800)

        pygame.init()
        self.background = Background(self.res)
        self.clock = pygame.time.Clock()

        self.pGroup = pygame.sprite.GroupSingle()
        self.cGroup = pygame.sprite.Group()

        self.player = Player(self.background.screen,self.pGroup,(0,0))

        #TODO: fixed number of coins currently 
        for i in range(5):
            spawnCoord = random.randint(50,self.res[0]),random.randint(50,self.res[1])
            coin = Coin(self.cGroup,self.background.screen,spawnCoord)
            

        

    def main_loop(self):
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()

    def _handle_input(self):
        pass

    def _process_game_logic(self):
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT: 
                pygame.quit()
                exit()
        self.player.update()


    def _draw(self):

        self.background.draw()

        #sprite groups are great because they allow you
        #to draw all sprites of the group at the same time
        self.pGroup.draw(self.background.screen)
        self.cGroup.draw(self.background.screen)
        
        pygame.display.flip()
        pygame.display.update()


class Background(pygame.sprite.Sprite):
    def __init__(self,res,image = "pacman.png",caption = "Privilege Recognition Task"):
        pygame.sprite.Sprite.__init__(self)
        self.res = res
        self.screen = pygame.display.set_mode(res)
        self.surface = pygame.Surface(res)
        self.image = self.imgLoad(image)

        pygame.display.set_caption(caption)

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

        




class GameObject(pygame.sprite.Sprite):
    def __init__(self,screen,group,coord,imgName,resize = (80,80), velocity = 1,acceleration = 0):
        pygame.sprite.Sprite.__init__(self)

        self.group = group 
        self.group.add(self)
        #screen tells us where to draw to
        self.screen = screen

        self.x,self.y = coord
        self.vel = velocity

        #should we have acceleration?
        self.acc = acceleration

        #add additional argument if resize is needed
        self.image = self.imgLoad(imgName,resize)


        
        #store the dimension of the sprite
        self.xDim,self.yDim = self.image.get_rect().size

        #pygame uses Rect to detect collisions
        #everytime the object moves, we need to update the Rect coordinates (call setRect whenever object pos changes)
        self.setRect()

    #load all the images at once so it doesnt need to be done constantly
    #must be in the game image directory
    #default size will be 80x80
    @staticmethod
    def imgLoad(img,resizeDim = (80,80)):

        relPath = path.join(path.dirname(__file__),f"images/objects/{img}")
        
        playerImg = pygame.image.load(relPath).convert_alpha()
        playerImg = pygame.transform.scale(playerImg,resizeDim)
        return playerImg

    

    def setRect(self):
        self.rect = pygame.Rect(self.x - self.xDim/2,self.y - self.yDim/2,
                                self.xDim,self.yDim)

    #direction is horizontal, then veritical
    def move(self,horizontal = 0, vertical = 0):
        self.x += horizontal * self.vel
        self.y += vertical * self.vel

        #TODO: check for out of bounds
        self.setRect()
    
    def draw(self):
        self.screen.blit(self.image,(self.x,self.y))

class Player(GameObject):

    #TODO: preload sprites for each eight direcitons
    def preload(self):
        return
    
    def __init__(self,screen,group,coord):
        super().__init__(screen,group,coord,"placeHolder.png")

    
    def update(self,horiz=1,vert=1):
        keys = pygame.key.get_pressed()
        xUpdate = 0
        yUpdate = 0
        
        #self.imgUpdate(keys)
        #when 8 directions added, this will update with corresponding sprite
        
    
        if keys[pygame.K_w]:
            self.move(0,-1)
        elif keys[pygame.K_s]:
            self.move(0,1)
            
        if keys[pygame.K_a]:
            self.move(-1,0)  
        elif keys[pygame.K_d]:
            self.move(1,0)


class Coin(GameObject):
    #have the coin give itself a random coordinate for now
    #TODO: implement "placement bias"
    def __init__(self,group,screen,coord):
        super().__init__(screen,group,coord,"coin.png",(40,40))
        
