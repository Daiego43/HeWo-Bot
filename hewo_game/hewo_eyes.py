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
        self.blinking_counter = 0
        self.blinking_speed = 60
        self.blinking_duration = 10

    def update(self):
        pass

    def draw(self, screen):
        size = screen.get_size()
        pygame.draw.ellipse(screen, self.color, (self.position, self.size))

    def set_position(self, position):
        self.position = position

    def set_size(self, size):
        self.size = size


class HewoEyes():
    DISTANCE_BETWEEN_EYES = 300

    def __init__(self, position=(300, 50), teleop=False):
        self.eye_left = HewoEye()
        self.eye_right = HewoEye()
        self.boundaries = (960, 640)
        self.teleop = teleop
        self.position = position
        self.set_position(position)

    def update(self):
        self.eye_left.update()
        self.eye_right.update()
        if self.teleop:
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
        self.boundaries = screen.get_size()
        self.eye_left.draw(screen)
        self.eye_right.draw(screen)

    def set_position(self, position):
        screen_width, screen_height = self.boundaries

        # Adjust position to keep left eye within screen boundaries
        x_left = max(0, min(position[0], screen_width - self.eye_left.size[0]))
        y_left = max(0, min(position[1], screen_height - self.eye_left.size[1]))

        # Adjust position to keep right eye within screen boundaries
        x_right = max(self.DISTANCE_BETWEEN_EYES,
                      min(position[0] + self.DISTANCE_BETWEEN_EYES, screen_width - self.eye_right.size[0]))
        y_right = max(0, min(position[1], screen_height - self.eye_right.size[1]))

        self.position = (x_left, y_left)
        self.eye_left.set_position((x_left, y_left))
        self.eye_right.set_position((x_right, y_right))

    def get_position(self):
        return self.position


if __name__ == '__main__':
    eyes = HewoEyes(teleop=True)
    game = SandBox(elements=[eyes])
    game.run()
