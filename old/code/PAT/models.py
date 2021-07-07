#This file contains the classes for the objects in our game like coins, ships, and more.

from pygame.math import Vector2
from pygame.transform import rotozoom

from utils import load_sprite, wrap_position

UP = Vector2(0, -1)

class GameObject:
    def __init__(self, position, sprite, velocity): #Creating a game object might look like: obj = GameObject((20,20), load_sprite('coin'), (5,1))
        self.position = Vector2(position) #For position and velocity, we need to store these as 2D vectors. Simply feed your value and let the constructor handle it.
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)

    def draw(self, surface):
        blit_position = self.position - Vector2(self.radius) #(0,0) is the top left edge of the screen. Thus, we have to adapt our position to this.
        surface.blit(self.sprite, blit_position)

    def move(self, surface):
        self.position = wrap_position(self.position + self.velocity, surface)

    def collides_with(self, other_obj):
        distance = self.position.distance_to(other_obj.position)
        return distance < self.radius + other_obj.radius

class Player(GameObject):
    MANEUVERABILITY = 3
    ACCELERATION = 0.1

    def __init__(self, position):
        self.direction = Vector2(UP)
        super().__init__(position, load_sprite("player"), Vector2(0))

    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        angle = self.MANEUVERABILITY * sign
        self.direction.rotate_ip(angle)

    def draw(self, surface):
        angle = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)

    def accelerate(self):
        self.velocity += self.direction * self.ACCELERATION

    def decelerate(self):
        self.velocity -= self.direction * self.ACCELERATION

class Coin(GameObject):
    def __init__(self, position):
        super().__init__(position, load_sprite("coin"), (0,0))
