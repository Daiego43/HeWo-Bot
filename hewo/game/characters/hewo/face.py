import pygame
import math
from hewo.game.characters.hewo.eye import Eye
from hewo.game.characters.hewo.mouth import Mouth
from settings.settings_loader import SettingsLoader

PHI = (1 + math.sqrt(5)) / 2
settings = SettingsLoader().load_settings("settings.hewo")


class Face:
    MAX_SIZE = (960, 640)
    COLOR = (
        settings['surface']['color']['r'],
        settings['surface']['color']['g'],
        settings['surface']['color']['b']
    )

    def __init__(self, position=None, color=COLOR, factor=350):
        if position is None:
            position = [0, 0]
        self.size = [PHI * factor, factor]
        self.position = position
        self.color = color
        self.face_surface = pygame.surface.Surface(self.size)

        self.face_surface = pygame.surface.Surface(self.size)
        self.eye_size = [self.size[0] / 5, self.size[1] / 5 * 4]
        self.mouth_size = [self.size[0] / 5 * 3, self.size[1] / 5]

        self.left_eye_pos = [0, 0]  # in the canvas
        self.right_eye_pos = [self.eye_size[0] * 4, 0]
        self.mouth_pos = [self.eye_size[0], self.eye_size[1]]

        self.left_eye = Eye(self.eye_size, self.left_eye_pos)
        self.right_eye = Eye(self.eye_size, self.right_eye_pos)
        self.mouth = Mouth(self.mouth_size, self.mouth_pos)
        self.set_face_elements()

    def set_face_elements(self):
        self.face_surface = pygame.surface.Surface(self.size)
        self.eye_size = [self.size[0] / 5, self.size[1] / 5 * 4]
        self.mouth_size = [self.size[0] / 5 * 3, self.size[1] / 5]

        self.left_eye_pos = [0, 0]  # in the canvas
        self.right_eye_pos = [self.eye_size[0] * 4, 0]
        self.mouth_pos = [self.eye_size[0], self.eye_size[1]]

        emotion = self.left_eye.get_emotion()
        self.left_eye = Eye(self.eye_size, self.left_eye_pos, init_emotion=emotion)
        emotion = self.right_eye.get_emotion()
        self.right_eye = Eye(self.eye_size, self.right_eye_pos, init_emotion=emotion)
        emotion = self.mouth.get_emotion()
        self.mouth = Mouth(self.mouth_size, self.mouth_pos, init_emotion=emotion)

    def set_size(self, size):
        self.size[0] = max(PHI, min(size[0], self.MAX_SIZE[0]))
        self.size[1] = max(1, min(size[1], self.MAX_SIZE[1]))

    def set_position(self, pos):
        self.position[0] = max(0, min(pos[0], self.MAX_SIZE[0] - self.size[0]))
        self.position[1] = max(0, min(pos[1], self.MAX_SIZE[1] - self.size[1]))

    def update(self):
        self.handle_input()
        self.left_eye.update()
        self.right_eye.update()
        self.mouth.update()

    def handle_event(self, event):
        self.left_eye.handle_event(event)
        self.right_eye.handle_event(event)
        self.mouth.handle_event(event)

    def draw(self, surface):
        self.face_surface.fill(self.color)
        self.left_eye.draw(self.face_surface)
        self.right_eye.draw(self.face_surface)
        self.mouth.draw(self.face_surface)
        surface.blit(self.face_surface, dest=self.position)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        size = self.size.copy()
        ref = size[1]
        step = 10
        pos = self.position.copy()

        if keys[pygame.K_m]:
            ref += step
            self.set_size([ref * PHI, ref])
            self.set_face_elements()

        if keys[pygame.K_n]:
            ref -= step
            self.set_size([ref * PHI, ref])
            self.set_face_elements()

        if keys[pygame.K_UP]:
            pos[1] -= step
        if keys[pygame.K_DOWN]:
            pos[1] += step
        if keys[pygame.K_LEFT]:
            pos[0] -= step
        if keys[pygame.K_RIGHT]:
            pos[0] += step
        self.set_position(pos)
