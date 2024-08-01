import pygame
from hewo.sandbox import SandBox


class HeWoMouth:
    INIT_POSITION = (400, 415)
    BOUNDARIES = (960, 640)
    MOUTH_MAX_SIZE = (200, 100)
    MOUTH_COLOR = (231, 210, 146)

    def __init__(self, position=INIT_POSITION, enable_teleop=False):
        self.position = position
        self.mouth_size = self.MOUTH_MAX_SIZE
        self.enable_teleop = enable_teleop
        self.set_position(position)

    def update(self):
        if self.enable_teleop:
            self.handle_input()

    def handle_input(self):
        keys = pygame.key.get_pressed()
        step = 10
        act_position = self.get_position()
        if keys[pygame.K_UP]:
            act_position = (act_position[0], act_position[1] - step)
        if keys[pygame.K_DOWN]:
            act_position = (act_position[0], act_position[1] + step)
        if keys[pygame.K_LEFT]:
            act_position = (act_position[0] - step, act_position[1])
        if keys[pygame.K_RIGHT]:
            act_position = (act_position[0] + step, act_position[1])
        self.set_position(act_position)

    def handle_event(self, event):
        pass

    def draw(self, screen):
        # pygame.draw.ellipse(screen, (255, 0, 0), (self.position, self.MOUTH_MAX_SIZE))
        rect = [self.position[0], self.position[1], self.MOUTH_MAX_SIZE[0], self.MOUTH_MAX_SIZE[1]]
        pygame.draw.arc(screen, self.MOUTH_COLOR, rect, 3.14, 0, 10)

    def set_position(self, position):
        x = max(100, min(position[0], self.BOUNDARIES[0] - self.MOUTH_MAX_SIZE[0] -100))
        y = max(350, min(position[1], self.BOUNDARIES[1] - self.MOUTH_MAX_SIZE[1]))
        self.position = (x, y)

    def get_position(self):
        return self.position


if __name__ == '__main__':
    elements = [HeWoMouth(enable_teleop=True)]
    sandbox = SandBox(elements)
    sandbox.run()
