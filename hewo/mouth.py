import pygame
from hewo.sandbox import SandBox


class HeWoMouth:
    INIT_POSITION = (0, 0)
    BBOX = ((0, 960),
            (400, 640))
    MOUTH_SIZE = (100, 100)
    MOUTH_COLOR = (231, 210, 146)
    MOVE_STEP = 20

    def __init__(self, name="mouth", position=INIT_POSITION, bbox=BBOX):
        self.name = name
        self.position = position
        self.size = self.MOUTH_SIZE
        self.move_step = self.MOVE_STEP
        self.bbox = bbox
        self.set_position(position)

    def update(self):
        self.handle_input()

    def handle_input(self):
        keys = pygame.key.get_pressed()
        position = list(self.get_position())
        if keys[pygame.K_UP]:
            position[1] -= self.move_step
        if keys[pygame.K_DOWN]:
            position[1] += self.move_step
        if keys[pygame.K_LEFT]:
            position[0] -= self.move_step
        if keys[pygame.K_RIGHT]:
            position[0] += self.move_step
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
        rect = [self.position[0], self.position[1], self.MOUTH_SIZE[0], self.MOUTH_SIZE[1]]
        pygame.draw.arc(screen, self.MOUTH_COLOR, rect, 3.14, 0, 10)


if __name__ == '__main__':
    from hewo.eyes import HeWoEye

    elements = [
        HeWoEye("left",
                bbox=((0, 800),
                      (0, 540))),
        HeWoEye("right",
                bbox=((160, 960),
                      (0, 540))),
        HeWoMouth(name="mouth",
                  position=(0, 0),
                  bbox=((960//20, 960 - 960//20),
                        (640//3, 640)))
    ]
    sandbox = SandBox(elements)
    sandbox.run()
