#This file details the game class. This class does all of the running of the game.

import pygame
from models import Coin, Player
from utils import get_random_position, load_sprite

class PAT:
    MIN_COIN_DISTANCE = 250
    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        num_coins = 2 #If there's a property that has to be changed by editing more than 2-3 lines, make a variable for it! Plus, naming the variable makes it so much clearer to read.
        self.coins = [Coin(get_random_position(self.screen)) for i in range(num_coins)] #This is amazing! Make sure to check out how this code works if you haven't already. It's called list comprehension and it's extremely useful.
        self.player1 = Player((400,300))

        for i in range(len(self.coins)): #What does this do? I can tell, but the code was very spaced out. For blocks like this that take a few lines to do one thing, describe what that one this is.
            while True: #Ex: This code finds an optimal position for each coin.
                position = get_random_position(self.screen)
                if(position.distance_to(self.player1.position) > self.MIN_COIN_DISTANCE):
                    break
            self.coins.append(Coin(position))

    def main_loop(self):
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()
        #There are three main sections to every game. Getting input, doing stuff, and updating the screen.

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Privilege Awareness Task")
        #This does under the hood things to get pygame ready to run.

    def _handle_input(self):
        for event in pygame.event.get(): #This command lists out all of the updates that happened this frame.
            if event.type == pygame.QUIT or ( event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE ):
                quit()

        is_key_pressed = pygame.key.get_pressed()

        if is_key_pressed[pygame.K_RIGHT]:
            self.player1.rotate(clockwise=True)
        elif is_key_pressed[pygame.K_LEFT]:
            self.player1.rotate(clockwise=False)
        if is_key_pressed[pygame.K_UP]:
            self.player1.accelerate()

    def _get_game_objects(self):
        return[*self.coins, self.player1]

    def _process_game_logic(self):
        #self.coin.move()
        for game_object in self._get_game_objects():
            game_object.move(self.screen) #You had game_object.move() here, why would that cause an error?
        self.player1.move(self.screen)

    def _draw(self):
        self.screen.fill((0, 0, 255)) #The argument here is an RGB channel.
        self.player1.draw(self.screen)
        #self.coin.draw(self.screen)

        for game_object in self._get_game_objects():
            game_object.draw(self.screen)

        pygame.display.flip()
        self.clock.tick(60) #This ticks the clock so that the game runs at the same speed on any machine.
        #print("Collides:", self.coin.collides_with(self.player))
