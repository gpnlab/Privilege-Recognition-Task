#This file contains the classes for the objects in our game like coins, ships, and more.

#IMPORTS
from pygame.math import Vector2
from pygame.transform import rotozoom
from utils import load_sprite, wrap_position

#The class GameObject will never actually be created during our program. Instead, it's a class we write that other objects
#like Player and Coin will inherit characteristics from. If you see "__super__" called in Player and Coin, that is referring
#to the GameObject class from which they descend.

class GameObject:
    def __init__(self, position, sprite, velocity):
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)

    def draw(self, surface):
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)

    def move(self, surface):
        self.position = wrap_position(self.position + self.velocity, surface)

    def collides_with(self, other_obj):
        distance = self.position.distance_to(other_obj.position)
        return distance < self.radius + other_obj.radius

class Player(GameObject):
    MANEUVERABILITY = 3
    ACCELERATION = 0.1
    face_up = Vector2(0,-1)

    def __init__(self, position, sprite_path):
        self.direction = Vector2(0,-1)
        self.score = 0
        super().__init__(position, load_sprite(sprite_path), Vector2(0))

    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        angle = self.MANEUVERABILITY * sign
        self.direction.rotate_ip(angle)

    def draw(self, surface):
        angle = self.direction.angle_to(Vector2(0,-1))
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
        super().__init__(position, load_sprite("coin.png"), (0,0))
