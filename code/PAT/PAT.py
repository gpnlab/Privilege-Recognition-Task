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
        self.player1 = Player((100,75))

        #Soooo I think this was two different ways of making coins? The first (and more effective way) was above, and this is an alternative approach?
        for i in range(len(self.coins)): #What does this do? I can tell, but the code was very spaced out. For blocks like this that take a few lines to do one thing, describe what that one this is.
            while True: #Ex: This code finds an optimal position for each coin.
                position = get_random_position(self.screen)
<<<<<<< Updated upstream
                if(position.distance_to(self.player1.position) > self.MIN_COIN_DISTANCE):
=======
                if (
                    position.distance_to(self.player1.position)
                    > self.MIN_COIN_DISTANCE
                ):
>>>>>>> Stashed changes
                    break
            #self.coins.append(Coin(position)) #This is causing an error, what is it?

    #This is the main game loop. #There are three main sections to every game. Getting input, doing stuff, and updating the screen.
    def main_loop(self):
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()

    #This initializes pygame commands and names the screen.
    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Privilege Awareness Task")
        #This does under the hood things to get pygame ready to run.

    def _handle_input(self):
        #This method will be pretty long. It takes the input on a frame and updates the game state according to our rules.
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
        return [*self.coins, self.player1] #What is *self.coins here?

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
        print("Collides:", self.coins[0].collides_with(self.player1))
        print("Collides:", self.coins[1].collides_with(self.player1))
