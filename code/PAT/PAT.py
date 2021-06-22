#This file details the game class. This class does all of the running of the game.

#IMPORTS - These statements make code from different Python libraries available for use to use.
import pygame
from models import Coin, Player
from utils import get_random_position, load_sprite
from time import time
from random import random

#The remainder of this file details an object, which is a collection of code that is consistently used in the same way.
#A class describes how an object works (methods) and what makes it up (attributes). We define methods in Python with the keyword "def",
#and we define attributes with the keyword "self.". After we create a specific instance of this object somewhere else in our code, we
#can access its methods and attributes with ".". For example, "PAT.coins" refers to the list of coins in the game.
#The object we're making here describes the game as a whole. There will only be one instance, because there is only one game.
class PAT:
    MIN_COIN_DISTANCE = 250
    #__init__ is a special method that is run the moment that an instance of an object is created. Thus, we see many attributes being
    #set with default values.
    def __init__(self):
        self.start = time()
        self._init_pygame()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        num_coins = 10
        self.coins = [Coin(get_random_position(self.screen)) for i in range(num_coins)]
        self.player1 = Player((400,100))
        self.opponents = [Player((100,300)), Player((700,300)), Player((400,500))]

    #This initializes pygame commands and names the screen.
    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Privilege Awareness Task")
        #This does under the hood things to get pygame ready to run.

    #Everything above this line happens the moment a game instance is created. Everything below happens as the game progresses.

    #This is the main game loop. #There are three main sections to every game. Getting input, doing stuff, and updating the screen.
    def main_loop(self):
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()

    #This is the "getting input".
    def _handle_input(self):
        for event in pygame.event.get(): #This command lists out all of the updates that happened this frame.
            if event.type == pygame.QUIT or ( event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE ):
                print("Your final score is:", self.score)
                quit()

        is_key_pressed = pygame.key.get_pressed()

        if is_key_pressed[pygame.K_RIGHT]:
            self.player1.rotate(clockwise=True)
        elif is_key_pressed[pygame.K_LEFT]:
            self.player1.rotate(clockwise=False)
        if is_key_pressed[pygame.K_UP]:
            self.player1.accelerate()
        if is_key_pressed[pygame.K_DOWN]:
            self.player1.decelerate()

    def _get_game_objects(self):
        return [*self.coins, *self.opponents, self.player1]

    #This is the "doing stuff".
    def _process_game_logic(self):
        for game_object in self._get_game_objects():
            game_object.move(self.screen)
        self.player1.move(self.screen)

        #CREATE OPPONENT MOVEMENT
        for opponent in self.opponents:
            accel = random() > 0.5
            rotate = random() > 0.5
            if(accel):
                opponent.accelerate()
            else:
                opponent.decelerate()
            if(rotate):
                opponent.rotate(clockwise=True)
            else:
                opponent.rotate(clockwise=False)


        #HANDLE COIN COLLISIONS
        if(self.player1):
            for coin in self.coins:
                if(self.player1.collides_with(coin)):
                    #print("COLLISION AT: ", time()-self.start)
                    self.coins.remove(coin)
                    self.player1.score+=1
                if(coin):
                    for opponent in self.opponents:
                        if(opponent.collides_with(coin)):
                            self.coins.remove(coin)
                            opponent.score+=1

        #IF NO COINS LEFT, END GAME
        if(len(self.coins)<=0):
            print("Your final score is:", self.player1.score)
            i=1
            for opponent in self.opponents:
                print(f"Opponent #{i}'s final score is: {opponent.score}")
                i+=1
            quit()

    #This is the "updating the screen".
    def _draw(self):
        self.screen.fill((0, 0, 255))
        self.player1.draw(self.screen)
        #self.coin.draw(self.screen)

        for game_object in self._get_game_objects():
            game_object.draw(self.screen)

        pygame.display.flip()
        self.clock.tick(60) #Neat fact: this ticks the clock so that the game runs at the same speed on any machine.
