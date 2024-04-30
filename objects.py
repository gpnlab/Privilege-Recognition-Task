import pygame
import math
import random
from os import path, stat
from exe import EXE


class GameObject(pygame.sprite.Sprite):
    def __init__(
        self,
        background,
        group,
        coord,
        imgName,
        velocity=0.5,
        acceleration=0,
        resize=(40, 40),
        seed=0,
    ):
        """
        This function creates a sprite object that can be drawn to the screen. The sprite
        object has a position, velocity, acceleration, image, and group.

        The sprite object can be removed from the screen and the group of sprites and deleted
        and the memory freed.

        Args:
          background: the background object that the sprite is on
          group: the sprite group that the object belongs to
          coord: the starting coordinates of the sprite
          imgName: the name of the image file
          velocity: how fast the object moves
          acceleration: how much the velocity changes per second. Defaults to 0
          resize: a tuple of the new dimensions of the image
          seed: random seed for the random number generator. Defaults to 0
        """

        pygame.sprite.Sprite.__init__(self)

        random.seed(seed)
        self.prev_time = pygame.time.get_ticks()

        self.group = group
        self.group.add(self)
        # screen tells us where to draw to
        self.bg = background
        self.screen = background.screen

        self.x, self.y = coord
        self.vel = velocity  # not sure what the units are

        # should we have acceleration?
        self.acc = acceleration

        # add additional argument if resize is needed
        self.image = self.imgLoad(imgName, resize)

        # store the dimension of the sprite
        self.xDim, self.yDim = self.image.get_rect().size

        # pygame uses Rect to detect collisions
        # everytime the object moves, we need to update the Rect coordinates (call setRect whenever object pos changes)
        self.setRect()

    # load all the images at once so it doesnt need to be done constantly
    # must be in the game image directory
    # default size will be 80x80
    @staticmethod
    def imgLoad(img, resizeDim=(80, 80)):
        """
        It takes an image file name, and returns a pygame image object

        Args:
          img: the name of the image file
          resizeDim: The dimensions of the image.

        Returns:
          The image is being returned.
        """

        asset_url = EXE.resource_path(f"images/objects/{img}")

        playerImg = pygame.image.load(asset_url).convert_alpha()

        # for exe wrapping
        asset_url = EXE.resource_path(f"images/objects/{img}")

        playerImg = pygame.image.load(asset_url).convert_alpha()
        playerImg = pygame.transform.scale(playerImg, resizeDim)
        return playerImg

    def setRect(self):
        """
        The function takes the x and y coordinates of the center of the rectangle and the x
        and y dimensions of the rectangle and returns a pygame.Rect object with the x and y
        coordinates of the top left corner of the rectangle and the x and y dimensions of the
        rectangle
        """
        self.rect = pygame.Rect(
            self.x - self.xDim / 2, self.y - self.yDim / 2, self.xDim, self.yDim
        )

    def update_velocity(self):
        """
        The function updates the velocity of the object by multiplying the velocity by the
        time passed since the last frame, and dividing it by 3
        """

        self.time_passed = pygame.time.get_ticks() - self.prev_time
        self.prev_time = pygame.time.get_ticks()

        # to correct for different framerates
        self.correct_vel = self.vel * self.time_passed / 5  # this is a good speed

    # direction is horizontal, then veritical
    def move(self, horizontal=0, vertical=0):
        """
        It moves the player in the direction of the input, and checks if the player is out of
        bounds. If the player is out of bounds, it moves the player back to the previous
        position

        Args:
          horizontal: -1, 0, or 1. Defaults to 0
          vertical: -1, 0, 1. Defaults to 0
        """

        self.update_velocity()
        # print(self.correct_vel)
        self.x += horizontal * self.correct_vel
        self.y += vertical * self.correct_vel

        # check oob
        if self.x < 0 + self.xDim // 2 or self.x > self.bg.res[0] - self.xDim // 2:
            self.x -= horizontal * self.correct_vel
        if self.y < 0 + self.yDim // 2 or self.y > self.bg.res[1] - self.yDim // 2:
            self.y -= vertical * self.correct_vel

        self.setRect()

    def draw(self):
        """
        The function draw() takes the image of the player and draws it on the screen at the x
        and y coordinates of the player
        """
        self.screen.blit(self.image, (self.x, self.y))


# Agent as in player/enemies
class Agent(GameObject):

    def __init__(
        self,
        name,
        background,
        group,
        coord,
        velocity,
        imgName="placeholder.png",
        seed=0,
    ):
        """
        This function is the constructor for the Player class. It takes in a name, background,
        group, coord, velocity, imgName, and seed. It then calls the super constructor for the
        Player class, and sets the name, and coins to the values passed in

        Args:
          name: The name of the player
          background: The background image
          group: The group that the sprite will be added to.
          coord: (x,y)
          velocity: a tuple of the form (x,y)
          imgName: The name of the image file. Defaults to placeholder.png
          seed: the seed for the random number generator. Defaults to 0
        """
        super().__init__(background, group, coord, imgName, velocity, seed)
        self.name = name
        self.coins = 0


class Player(Agent):
    def __init__(
        self, background, group, coord, velocity, imgName="placeholder.png", seed=0
    ):
        """
        This function is the constructor for the Player class. It takes in a background,
        group, coordinate, velocity, image name, and seed. It then calls the constructor
        for the Agent class above

        Args:
          background: The background image
          group: The group that the sprite will be added to.
          coord: (x,y)
          velocity: a tuple of the form (x,y)
          imgName: The name of the image file to be used for the sprite. Defaults to
        placeholder.png
          seed: The seed for the random number generator. Defaults to 0
        """
        super().__init__("Player 1", background, group, coord, velocity, imgName, seed)

    def getInput(self, keys, time_passed):
        """
        If the player is pressing a key, the player moves in that direction

        Args:
          keys: the list of keys that are currently being pressed
          time_passed: the time passed since the last frame
        """

        # self.imgUpdate(keys)
        # when 8 directions added, this will update with corresponding sprite
        xInd, yInd = 0, 0

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            yInd -= 1

        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            yInd += 1

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            xInd -= 1

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            xInd += 1

        if yInd != 0 and xInd != 0:
            self.move(math.sqrt(2) * xInd / 2, math.sqrt(2) * yInd / 2)
        else:
            self.move(xInd, yInd)


# TODO: improve AI
#   1. Don't allow "half" movements
#   2. If keeping markov chain approach, change states to be more "human"
class Enemy(Agent):
    # need to pass in coin group for AI to find nearest coin
    def __init__(
        self,
        name,
        background,
        group,
        cGroup,
        coord,
        velocity,
        imgName="placeholder.png",
        seed=0,
    ):
        """
        The constructor for the class, which sets the state of the object to 0, and sets the
        probability matrix for the state transitions

        Args:
          name: name of the object
          background: the background image
          group: the group of all the sprites
          cGroup: the coin group
          coord: the current position of the player
          velocity: the speed of the enemy
          imgName: the name of the image file for the sprite. Defaults to placeholder.png
          seed: random seed for the random number generator. Defaults to 0
        """

        super().__init__(name, background, group, coord, velocity, imgName, seed)

        # 3 states:
        # 0 - optimal path towards closest coin
        # 1 - random direction
        # 2 - stay still
        # transfer probabilities will be listed in the readme
        self.state = 0

        # probability matrix for transfering
        self.pMatrix = [[8, 1, 1], [7, 1, 2], [7, 1, 2]]

        # keep current objective (coin coord)
        self.coinObj = (0, 0)

    def _dist(self, c1, c2):
        """
        It calculates the distance between two points.

        Args:
          c1: The first coordinate
          c2: (x,y) coordinates of the center of the circle

        Returns:
          The distance between two points.
        """
        # we should make this numpy
        (x1, y1), (x2, y2) = c1, c2
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def getRandCoinCoord(self, cGroup):
        """
        It returns the coordinates of a random coin in the coinGroup

        Returns:
          The x and y coordinates of the random coin.
        """
        # loop through everything in coin group
        if len(cGroup) == 0:
            return (0, 0)

        randCoin = cGroup.sprites()[random.randint(0, len(cGroup) - 1)]

        return (randCoin.x, randCoin.y)

    def getNearestCoinCoord(self, cGroup):
        """
        It returns the coordinates of the nearest coin to the ai

        Returns:
          The x and y coordinates of the nearest coin.
        """
        if len(cGroup) == 0:
            return (0, 0)

        # default "max" distance
        bestDist = self.bg.res[0]

        for coin in cGroup:
            currDist = self._dist((self.x, self.y), (coin.x, coin.y))

            if currDist < bestDist:
                bestCoin = coin
                bestDist = currDist

        return (bestCoin.x, bestCoin.y)

    # should be ran whenever coin is obtained
    # for now, have it be 50/50 whether ai chooses opt or random coin
    # What is this function for? - Linghai
    def setCoinObjective(self, cGroup):
        """
        If the coin is still in the group, don't change the objective
        """
        self.coinObj = self.getNearestCoinCoord(cGroup)

    # optimal movement toward nearest coin
    def optimalMove(self):
        """
        The function takes the coordinates of the nearest coin and moves the ai towards it
        """
        # try:
        #    (cX,cY) = self.getNearestCoinCoord()
        # except:
        #    (cX,cY) = (0,0)
        (cX, cY) = self.coinObj
        d = self._dist((cX, cY), (self.x, self.y))

        # normalize - this is a relic of ai surpemacy
        xMov = self.vel * (cX - self.x) / d
        yMov = self.vel * (self.y - cY) / d

        # indicators for which direction
        xInd, yInd = 0, 0
        # prevent half movements
        if xMov < 0:
            xInd = -1
        elif xMov > 0:
            xInd = 1

        if yMov > 0:
            yInd = -1
        elif yMov < 0:
            yInd = 1

        if yInd != 0 and xInd != 0:
            self.move(math.sqrt(2) * xInd / 2, math.sqrt(2) * yInd / 2)
        else:
            self.move(xInd, yInd)

    def getRandMove(self):
        """
        It generates a random point on the unit circle as a direction for the ai
        """
        self.randX = random.uniform(-1, 1)
        self.randY = math.sqrt(1 - self.randX**2) * random.choice([-1, 1])

    def randMove(self):
        """
        It returns a randomized and normalized movement
        """
        # return a randomized and normalized movement
        self.move(self.randX, self.randY)

    def getNewState(self):
        """
        It returns a random number from the set {0,1,2} with probabilities given by the row of
        the transition matrix corresponding to the current state

        Returns:
          a random number from the list [0,1,2] with the probabilities given by the row of the
        pMatrix corresponding to the current state.
        """
        return random.choices([0, 1, 2], self.pMatrix[self.state])[0]


class Coin(GameObject):
    # have the coin give itself a random coordinate for now
    # TODO: implement "placement bias"
    def __init__(self, group, background, coord):
        super().__init__(background, group, coord, "coin.png", (20, 20))
