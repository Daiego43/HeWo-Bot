import pygame
from hewo.sandbox import SandBox


class HeWoEye:
    EYE_MAX_SIZE = (940 // 20, 640 // 3)
    EYE_COLOR = (231, 210, 146)
    BLINK_STEP = 30
    MOVE_STEP = 20
    BLINK_RATE = 60 * 4
    GROW = True
    SHRINK = False

    def __init__(self, name, size=EYE_MAX_SIZE, position=(0, 0), bbox=((0, 960), (0, 640))):
        self.name = name
        self.color = self.EYE_COLOR
        self.size = size
        self.position = position
        self.update_count = 0
        self.blink_rate = self.BLINK_RATE
        self.enable_blink = False
        self.blink_step = self.BLINK_STEP
        self.blink_state = self.SHRINK
        self.move_step = self.MOVE_STEP
        self.bbox = bbox

    def update(self):
        self.update_count += 1
        self.handle_input()
        if self.update_count % self.blink_rate == 0:
            self.enable_blink = True
        if self.enable_blink:
            self.blink()

    def blink(self):
        if self.blink_state == self.SHRINK:
            self.size = (self.size[0], self.size[1] - self.blink_step)
            self.blink_step *= 1.1
            if self.size[1] <= 0:
                self.blink_step = self.BLINK_STEP
                self.blink_state = self.GROW

        if self.blink_state == self.GROW:
            self.size = (self.size[0], self.size[1] + self.blink_step)
            if self.size[1] >= self.EYE_MAX_SIZE[1]:
                self.blink_state = self.SHRINK
                self.enable_blink = False

    def draw(self, screen):
        # Calcula la posición superior izquierda desde el centro
        top_left = (self.position[0] - self.size[0] // 2,
                    self.position[1] - self.size[1] // 2)
        self.validate_position()
        pygame.draw.ellipse(screen, self.color, (*top_left, *self.size))

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

    def validate_position(self):
        position = self.get_position()
        size = self.size
        if position[0] - size[0] // 2 < self.bbox[0][0]:
            position = (self.bbox[0][0] + size[0] // 2, position[1])
        if position[0] + size[0] // 2 > self.bbox[0][1]:
            position = (self.bbox[0][1] - size[0] // 2, position[1])
        if position[1] - size[1] // 2 < self.bbox[1][0]:
            position = (position[0], self.bbox[1][0] + size[1] // 2)
        if position[1] + size[1] // 2 > self.bbox[1][1]:
            position = (position[0], self.bbox[1][1] - size[1] // 2)
        self.set_position(position)

    def set_position(self, position):
        self.position = position

    def handle_event(self, event):
        pass

    def get_position(self):
        return self.position

    def set_size(self, size):
        self.size = size


if __name__ == '__main__':
    left_eye = HeWoEye("left",
                       bbox=((0, 800),
                             (0, 640)))
    right_eye = HeWoEye("right",
                        bbox=((160, 960),
                              (0, 640)))

    game = SandBox(elements=[left_eye, right_eye])
    game.run()
