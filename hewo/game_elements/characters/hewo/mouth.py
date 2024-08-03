import pygame
import math
from hewo.game_elements.scenes.sandbox import SandBox


class HeWoMouth:
    INIT_POSITION = (0, 0)
    BBOX = ((960 // 20 * 2, 960 - 960 // 20 * 2),
            (0, 640))
    MOUTH_SIZE = (175, 50)
    MOUTH_COLOR = (231, 210, 146)
    MOVE_STEP = 20
    MOUTHS = [
        'smiling',
        'talking',
        None
    ]

    def __init__(self, name="mouth", position=INIT_POSITION, bbox=BBOX, size=MOUTH_SIZE):
        self.name = name
        self.position = position
        self.size = size
        self.move_step = self.MOVE_STEP
        self.bbox = bbox
        self.set_position(position)
        self.talk_frame = self.MOUTH_SIZE[1]
        self.talk_increment = 15
        self.mouth_state = self.MOUTHS[1]
        self.mouth_i = 0

    def update(self):
        self.handle_input()

    def handle_input(self, step=MOVE_STEP):
        keys = pygame.key.get_pressed()
        position = list(self.get_position())
        if keys[pygame.K_UP]:
            position[1] -= step
        if keys[pygame.K_DOWN]:
            position[1] += step
        if keys[pygame.K_LEFT]:
            position[0] -= step
        if keys[pygame.K_RIGHT]:
            position[0] += step
        self.set_position(position)

    def set_position(self, position):
        size = self.size
        if position[0] < self.bbox[0][0]:
            position = (self.bbox[0][0], position[1])
        if position[1] < self.bbox[1][0]:
            position = (position[0], self.bbox[1][0])
        if position[0] + size[0] > self.bbox[0][1]:
            position = (self.bbox[0][1] - size[0], position[1])
        if position[1] + size[1] > self.bbox[1][1]:
            position = (position[0], self.bbox[1][1] - size[1])
        self.position = position

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.toggle_mouth_state()
            if event.key == pygame.K_q:
                self.mouth_state = self.MOUTHS[0]
            if event.key == pygame.K_w:
                self.mouth_state = self.MOUTHS[1]
            if event.key == pygame.K_e:
                self.mouth_state = self.MOUTHS[2]


    def toggle_mouth_state(self):
        self.mouth_state = self.MOUTHS[self.mouth_i]
        self.mouth_i += 1
        if self.mouth_i >= len(self.MOUTHS):
            self.mouth_i = 0

    def get_position(self):
        return self.position

    def set_size(self, size):
        self.size = size

    def draw(self, screen):
        match self.mouth_state:
            case 'talking':
                self.move_lips()  # This is the only difference between the cases
                self.talking_mouth_smiling(screen)
            case 'smiling':
                self.smiling_mouth(screen)
            case _:
                self.plane_mouth(screen)

    def move_lips(self):
        self.talk_frame += self.talk_increment  # Incrementa el paso para abrir/cerrar la boca
        if self.talk_frame > self.size[1]:
            self.talk_frame = self.size[1]
            self.talk_increment *= -1
        if self.talk_frame < 0:
            self.talk_frame = 0
            self.talk_increment *= -1

    def talking_mouth_smiling(self, screen):
        # Línea horizontal en medio
        # Semicírculo inferior
        # Debe encongerse y expandirse para simular el habla

        new_size = self.size[1] - self.talk_frame
        curv = pygame.Rect(self.position[0], self.position[1],
                           self.size[0], new_size)
        start = self.position[0], self.position[1] + new_size // 2
        end = self.position[0] + self.size[0], self.position[1] + new_size // 2

        pygame.draw.line(screen, self.MOUTH_COLOR, start_pos=start, end_pos=end, width=5)
        pygame.draw.arc(screen, self.MOUTH_COLOR, curv, 3.14, 0, 5)

    def smiling_mouth(self, screen):
        start = self.position[0], self.position[1]
        end = self.size[0], self.size[1]
        rect = [start[0], start[1], end[0], end[1]]
        pygame.draw.arc(screen, self.MOUTH_COLOR, rect, 3.14, 0, 5)

    def plane_mouth(self, screen):
        start = self.position[0], self.position[1] + self.size[1] // 2
        end = self.position[0] + self.size[0], self.position[1] + self.size[1] // 2
        pygame.draw.line(screen, self.MOUTH_COLOR, start_pos=start, end_pos=end, width=5)
