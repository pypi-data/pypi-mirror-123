import pygame

from aerforge import *

class GameObject(pygame.Rect):
    def __init__(self, window, shape = Rect, width = 50, height = 50, x = 0, y = 0, color = WHITE, points = [], add_to_objects = True):
        self.window = window

        self.width = width
        self.height = height

        self.x = x
        self.y = y

        self.shape = shape
        self.color = color

        self.points = points

        self.destroyed = False

        self.add_to_objects = add_to_objects

        if self.add_to_objects:
            self.window.objects.append(self)

    def draw(self):
        if not self.destroyed:
            if self.shape == Rect:
                pygame.draw.rect(self.window.window, self.color, self)

            elif self.shape == Circle:
                pygame.draw.ellipse(self.window.window, self.color, self)

            elif self.shape == Polygon:
                pygame.draw.polygon(self.window.window, self.color, self.points)

            else:
                raise ForgeError("Invalid shape")

    def center(self):
        self.x = self.window.width / 2 - self.width / 2
        self.y = self.window.height / 2 - self.height / 2

    def center_x(self):
        self.x = self.window.width / 2 - self.width / 2

    def center_y(self):
        self.y = self.window.height / 2 - self.height / 2

    def hit(self, gameobject):
        if isinstance(gameobject, pygame.Rect):
            return self.colliderect(gameobject)

        elif isinstance(gameobject, tuple):
            return self.collidepoint(gameobject)

        else:
            raise ForgeError("Invalid type")

    def destroy(self):
        self.destroyed = True