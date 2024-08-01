import pygame
from hewo.sandbox import SandBox


class HeWoEye:
    EYE_MAX_SIZE = (100, 350)
    GROW = True
    SHRINK = False
    BASE_STEP = 30
    EYE_COLOR = (231, 210, 146)

    def __init__(self):
        self.color = self.EYE_COLOR
        self.size = self.EYE_MAX_SIZE
        self.position = (0, 0)
        self.blink_state = self.SHRINK
        self.update_count = 0
        self.blink_rate = 60 * 3
        self.base_step = 30
        self.do_blink = False

    def update(self):
        self.update_count += 1
        if self.update_count % self.blink_rate == 0:
            self.do_blink = True
        if self.do_blink:
            self.eye_update()

    def eye_update(self):
        if self.blink_state == self.SHRINK:
            self.size = (self.size[0], self.size[1] - self.base_step)
            self.base_step *= 1.1
            if self.size[1] <= 0:
                self.base_step = self.BASE_STEP
                self.blink_state = self.GROW

        if self.blink_state == self.GROW:
            self.size = (self.size[0], self.size[1] + self.base_step)
            if self.size[1] >= self.EYE_MAX_SIZE[1]:
                self.blink_state = self.SHRINK
                self.do_blink = False

    def draw(self, screen):
        # Calcula la posición superior izquierda desde el centro
        top_left = (self.position[0] - self.size[0] // 2, self.position[1] - self.size[1] // 2)
        pygame.draw.ellipse(screen, self.color, (*top_left, *self.size))

    def set_position(self, position):
        self.position = position

    def set_size(self, size):
        self.size = size


class HeWoEyes():
    DISTANCE_BETWEEN_EYES = 300
    INIT_POSITION = (350, 250)
    BOUNDARIES = (960, 640)

    def __init__(self, position=INIT_POSITION, enable_teleop=False):
        self.eye_left = HeWoEye()
        self.eye_right = HeWoEye()
        self.eye_right.position = (self.eye_left.position[0] + self.DISTANCE_BETWEEN_EYES, self.eye_left.position[0])
        self.enable_teleop = enable_teleop
        self.position = position
        self.set_position(position)

    def update(self):
        self.eye_left.update()
        self.eye_right.update()
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
        self.eye_left.draw(screen)
        self.eye_right.draw(screen)

    def set_position(self, position):
        screen_width, screen_height = self.BOUNDARIES

        # TODO: I Want Eyes to squish horizontally when they get close to the edge
        x_left = max(
            self.eye_left.EYE_MAX_SIZE[0] / 2,
            min(
                position[0],
                screen_width - self.eye_left.EYE_MAX_SIZE[0] / 2 - self.DISTANCE_BETWEEN_EYES
            )
        )

        x_right = min(
            position[0] + self.DISTANCE_BETWEEN_EYES,
            screen_width - self.eye_right.EYE_MAX_SIZE[0] / 2
        )

        y_left = max(
            self.eye_left.EYE_MAX_SIZE[1] / 2,
            min(
                position[1],
                screen_height - self.eye_left.EYE_MAX_SIZE[1] / 2
            )
        )

        y_right = max(
            self.eye_right.EYE_MAX_SIZE[1] / 2,
            min(position[1],
                screen_height - self.eye_right.EYE_MAX_SIZE[1] / 2)
        )

        self.position = (x_left, y_left)
        self.eye_left.set_position((x_left, y_left))
        self.eye_right.set_position((x_right, y_right))

    def get_position(self):
        return self.position


if __name__ == '__main__':
    eyes = HeWoEyes(enable_teleop=True)
    game = SandBox(elements=[eyes])
    game.run()
