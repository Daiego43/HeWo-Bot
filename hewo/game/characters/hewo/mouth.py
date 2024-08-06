import pygame
import numpy as np
from scipy.interpolate import make_interp_spline


class Lip:
    def __init__(self, size, position, color):
        self.size = size
        self.position = position
        self.color = color
        self.lip_points = np.array([
            [0, 0],
            [self.size[0] / 2, 0],
            [self.size[0], 0]
        ])
        self.increments = [0, 0, 0]

    def lip_shape(self):
        x_points = np.array([p[0] for p in self.lip_points])
        y_points = np.array([p[1] for p in self.lip_points])
        y_points = self.set_y_points(y_points)
        spline = make_interp_spline(x_points, y_points, k=2)
        x_range = np.linspace(min(x_points), max(x_points), 500)
        interpolated_points = [(int(x), int(spline(x))) for x in x_range]
        return interpolated_points

    def set_y_points(self, y_points):
        for i, val in enumerate(zip(y_points, self.increments)):
            point = val[0] + val[1]
            clamped_value = max(0, min(point, self.size[1]))
            y_points[i] = clamped_value
        return y_points

    def set_increments(self, increments):
        for i in range(len(increments)):
            increments[i] = max(0, min(increments[i], self.size[1]))
        self.increments = increments

    def update(self):
        pass

    def draw(self, surface):
        points = self.lip_shape()
        pygame.draw.lines(surface, self.color, False, points, 10)

    def handle_event(self, event):
        pass


class Mouth:
    point_elevation = 0

    def __init__(self, size, position):
        self.size = size
        self.position = position
        self.surface = pygame.Surface(self.size)
        self.up_lip_values = [0, 0, 0]
        self.down_lip_values = [0, 0, 0]
        self.lips = [
            Lip(self.size, self.position, (0, 255, 0)),
            Lip(self.size, self.position, (255, 0, 0))
        ]

    def draw(self, surface):
        self.surface.fill((0, 0, 255))
        for lip in self.lips:
            lip.draw(self.surface)
        surface.blit(self.surface, self.position)

    def update(self):
        self.handle_input()

    def handle_input(self):
        """
        Mouth controls
        Up and Down lip indices [0] and [2] always share position
        q/a -> increase and decrease left position
        r/f -> inc/dec right position
        w/s -> inc/dec up lip center
        e/d -> inc/dec down lip center
        :return:
        """

        def adjust_value(key_increase, key_decrease, value, step=10):
            if keys[key_increase]:
                value -= step
            if keys[key_decrease]:
                value += step
            return value

        keys = pygame.key.get_pressed()
        up = self.up_lip_values
        down = self.down_lip_values

        up[0] = down[0] = adjust_value(pygame.K_q, pygame.K_a, up[0])
        up[1] = adjust_value(pygame.K_w, pygame.K_s, up[1])
        down[1] = adjust_value(pygame.K_e, pygame.K_d, down[1])
        up[2] = down[2] = adjust_value(pygame.K_r, pygame.K_f, up[2])
        # Don't letting the down lip go up
        down[1] = max(up[1], min(down[1], self.size[1]))

        self.lips[0].set_increments(up)
        self.lips[1].set_increments(down)

    def handle_event(self, event):
        pass
