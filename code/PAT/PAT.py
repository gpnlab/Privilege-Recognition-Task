#This file details the game class. This class does all of the running of the game.

import pygame
from models import GameObject, Player
from utils import load_sprite

class PAT:
    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.player1 = Player((400,300))

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

    def _process_game_logic(self):
        self.coin.move()
        self.player.move()

    def _draw(self):
        self.screen.fill((0, 0, 255)) #The argument here is an RGB channel.
        self.player.draw(self.screen)
        self.coin.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(60) #This ticks the clock so that the game runs at the same speed on any machine.
        print("Collides:", self.coin.collides_with(self.player))
