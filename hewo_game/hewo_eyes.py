import pygame
from hewo_game.hewo_game_sandbox import SandBox


class HewoEye:
    """
    HeWo eyes are just elipses.
    We have to define their color,shape and logic.
    Maybe animate the blinking of the eyes.
    """

    def __init__(self):
        self.color = (231, 210, 146)
        self.size = (100, 350)
        self.position = (0, 0)
        self.blinking = False
        self.blinking_counter = 0
        self.blinking_speed = 60
        self.blinking_duration = 10

    def update(self):
        pass

    def draw(self, screen):
        if not self.blinking:
            pygame.draw.ellipse(screen, self.color, (self.position, self.size))

    def set_position(self, position):
        self.position = position

    def set_size(self, size):
        self.size = size


class HewoEyes():
    DISTANCE_BETWEEN_EYES = 300

    def __init__(self):
        self.eye_left = HewoEye()
        self.eye_right = HewoEye()
        self.set_position((0, 0))

    def update(self):
        self.eye_left.update()
        self.eye_right.update()

    def draw(self, screen):
        self.eye_left.draw(screen)
        self.eye_right.draw(screen)

    def set_position(self, position):
        self.eye_left.set_position((position[0], position[1]))
        self.eye_right.set_position((position[0] + self.DISTANCE_BETWEEN_EYES, position[1]))


if __name__ == '__main__':
    eyes = HewoEyes()
    game = SandBox(elements=[eyes])
    game.run()
