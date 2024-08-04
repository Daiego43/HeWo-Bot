"""
I have taken notes on how I want Hewo's face to look like.
I will be using this as a reference to create the face.
This also will require to create an extense yaml config
file to store game properties.
"""
import pygame
import math
from hewo.settings.settings_loader import SettingsLoader
from hewo.game.characters.hewo.eye import Eye

LOADER = SettingsLoader()


class HewoFace:
    face = LOADER.load_settings('hewo.settings.hewo.face')

    HEART = phi = (1 + math.sqrt(5)) / 2
    MAX_SIZE = [face['width'],
                face['height']]
    FACE_SIZE = [face['width'] / HEART,
                 face['height'] / HEART]
    INIT_POSITION = [face['position']['x'],
                     face['position']['y']]
    FACE_COLOR = [face['color']['r'],
                  face['color']['g'],
                  face['color']['b']]
    SPEED = face['speed']
    SPEED_STEP = face['speed_step']
    SIZE_STEP = face['size_step']
    SIZE_FACTOR = face['size_factor']

    def __init__(self):
        self.face_surface = pygame.Surface(self.FACE_SIZE)
        self.size = self.FACE_SIZE
        self.size_factor = self.SIZE_FACTOR
        self.size_step = self.SIZE_STEP
        self.speed = self.SPEED
        self.speed_step = self.SPEED_STEP
        self.position = self.INIT_POSITION
        self.face_elems = [
            Eye()
        ]
        self.set_size()

    def handle_event(self, event):
        pass

    def draw(self, display):
        self.face_surface = pygame.Surface(self.size)
        self.face_surface.fill(self.FACE_COLOR)
        for elem in self.face_elems:
            elem.draw(self.face_surface)
        display.blit(self.face_surface, self.position)

    def update(self):
        self.handle_inputs()
        for elem in self.face_elems:
            elem.update()

    def handle_inputs(self):
        keys = pygame.key.get_pressed()
        self.factors(keys)
        self.teleop(keys)

    def factors(self, keys):
        if keys[pygame.K_w]:
            self.set_size(self.size_factor - self.size_step)
        if keys[pygame.K_s]:
            self.set_size(self.size_factor + self.size_step)
        if keys[pygame.K_d]:
            self.set_speed(self.speed + self.speed_step)
        if keys[pygame.K_a]:
            self.set_speed(self.speed - self.speed_step)

    def set_speed(self, speed):
        self.speed = speed
        if self.speed < 0:
            self.speed = 0
        print('speed', self.speed)

    def set_size(self, size_factor=1):
        self.size_factor = size_factor
        if self.size_factor < 0.1:
            self.size_factor = 0.1
        heart = self.HEART * self.size_factor
        self.size = [
            self.face['width'] / heart,
            self.face['height'] / heart
        ]
        if self.size[0] > self.MAX_SIZE[0]:
            self.size = self.MAX_SIZE
        if self.size[1] > self.MAX_SIZE[1]:
            self.size = self.MAX_SIZE

        # Set up the elements positions and sizes
        self.face_setup()

    def face_setup(self):
        a, b = self.size[0], self.size[1]
        bit = a / 5
        bop = b / 5
        sizes = [
            (bit, bop * 4)
        ]
        poses = [
            (0, 0)
        ]
        for i, elem in enumerate(self.face_elems):
            elem.set_size(sizes[i])
            elem.set_position(poses[i])

    def teleop(self, keys):
        position = self.position
        if keys[pygame.K_LEFT]:
            position[0] -= self.speed
        if keys[pygame.K_RIGHT]:
            position[0] += self.speed
        if keys[pygame.K_UP]:
            position[1] -= self.speed
        if keys[pygame.K_DOWN]:
            position[1] += self.speed
        self.set_position(position)

    def set_position(self, position):
        self.position = position
        if self.position[0] < 0:
            self.position[0] = 0
        if self.position[0] + self.size[0] > self.MAX_SIZE[0]:
            self.position[0] = self.MAX_SIZE[0] - self.size[0]
        if self.position[1] < 0:
            self.position[1] = 0
        if self.position[1] + self.size[1] > self.MAX_SIZE[1]:
            self.position[1] = self.MAX_SIZE[1] - self.size[1]
