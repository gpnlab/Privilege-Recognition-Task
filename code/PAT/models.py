#This file contains the classes for the objects in our game like coins, ships, and more.

from pygame.math import Vector2
from utils import load_sprite

class GameObject:
    def __init__(self, position, sprite, velocity): #Creating a game object might look like: obj = GameObject((20,20), load_sprite('coin'), (5,1))
        self.position = Vector2(position) #For position and velocity, we need to store these as 2D vectors. Simply feed your value and let the constructor handle it.
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)

    def draw(self, surface):
        blit_position = self.position - Vector2(self.radius) #(0,0) is the top left edge of the screen. Thus, we have to adapt our position to this.
        surface.blit(self.sprite, blit_position)

    def move(self):
        self.position = self.position + self.velocity

    def collides_with(self, other_obj):
        distance = self.position.distance_to(other_obj.position)
        return distance < self.radius + other_obj.radius

class Player(GameObject):
    def __init__(self, position):
        super().__init__(position, load_sprite("player"), Vector2(0))
