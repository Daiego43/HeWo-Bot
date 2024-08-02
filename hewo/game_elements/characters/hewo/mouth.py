import pygame
from hewo.game_elements.scenes.sandbox import SandBox


class HeWoMouth:
    INIT_POSITION = (0, 0)
    BBOX = ((960 // 20 * 2, 960 - 960 // 20 * 2),
            (640 // 6, 640))
    MOUTH_SIZE = (175, 50)
    MOUTH_COLOR = (231, 210, 146)
    MOVE_STEP = 20
    ANIMATION_STEP = 10

    def __init__(self, name="mouth", position=INIT_POSITION, bbox=BBOX, size=MOUTH_SIZE):
        self.name = name
        self.position = position
        self.size = size
        self.move_step = self.MOVE_STEP
        self.bbox = bbox
        self.set_position(position)
        self.mouth_opening = 0
        self.increment = 1
        self.mouth_state = 'smiling'

    def update(self):
        self.handle_input()

    def move_lips(self):
        if self.increment > 0:
            self.mouth_opening += self.increment
            if self.mouth_opening >= self.MOUTH_SIZE[0] // 2:
                self.increment *= -1
        if self.increment < 0:
            self.mouth_opening += self.increment
            if self.mouth_opening <= 0:
                self.increment *= -1

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
        pass

    def get_position(self):
        return self.position

    def set_size(self, size):
        self.size = size

    def draw(self, screen):
        self.move_lips()
        start = self.position[0], self.position[1]
        end = self.size[0], self.size[1]
        match self.mouth_state:
            case 'talking':
                rect = [start[0], start[1], end[0], end[1]]
                pygame.draw.arc(screen, self.MOUTH_COLOR, rect, 3.14, 0, 5)
                start = self.position[0], self.position[1] + self.size[1] // 2
                end = self.position[0] + self.size[0], self.position[1] + self.size[1] // 2
                pygame.draw.line(screen, self.MOUTH_COLOR, start_pos=start, end_pos=end, width=5)
            case 'smiling':
                rect = [start[0], start[1], end[0], end[1]]
                pygame.draw.arc(screen, self.MOUTH_COLOR, rect, 3.14, 0, 5)
            case _:
                start = self.position[0], self.position[1] + self.size[1] // 2
                end = self.position[0] + self.size[0], self.position[1] + self.size[1] // 2
                pygame.draw.line(screen, self.MOUTH_COLOR, start_pos=start, end_pos=end, width=5)
