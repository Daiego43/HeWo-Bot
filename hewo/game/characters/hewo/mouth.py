import pygame
import numpy as np
from scipy.interpolate import make_interp_spline
from settings.settings_loader import SettingsLoader

settings = SettingsLoader().load_settings("settings.hewo")
mouth = settings['elements']['mouth']


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
    COLOR = (
        mouth['surface']['color']['r'],
        mouth['surface']['color']['g'],
        mouth['surface']['color']['b']
    )
    TOP_LIP = (
        mouth['elements']['top_lip']['color']['r'],
        mouth['elements']['top_lip']['color']['g'],
        mouth['elements']['top_lip']['color']['b']
    )
    BOT_LIP = (
        mouth['elements']['bot_lip']['color']['r'],
        mouth['elements']['bot_lip']['color']['g'],
        mouth['elements']['bot_lip']['color']['b']
    )

    def __init__(self, size, position, color=COLOR):
        self.size = size
        self.position = position
        self.surface = pygame.Surface(self.size)
        self.color = color

        self.top_lip_emotion = [0, 0, 0]
        self.bot_lip_emotion = [0, 0, 0]
        self.top_lip = Lip(self.size, self.position, self.TOP_LIP)
        self.bot_lip = Lip(self.size, self.position, self.BOT_LIP)

    def draw(self, surface):
        self.surface.fill(self.color)
        self.top_lip.draw(self.surface)
        self.bot_lip.draw(self.surface)
        surface.blit(self.surface, self.position)

    def update(self):
        self.handle_input()

    def handle_input(self):
        def adjust_value(key_increase, key_decrease, value, step=10):
            if keys[key_increase]:
                value -= step
            if keys[key_decrease]:
                value += step
            return value

        keys = pygame.key.get_pressed()
        top = self.top_lip_emotion
        bot = self.bot_lip_emotion

        top[0] = bot[0] = adjust_value(pygame.K_q, pygame.K_a, top[0])
        top[1] = adjust_value(pygame.K_w, pygame.K_s, top[1])
        bot[1] = adjust_value(pygame.K_e, pygame.K_d, bot[1])
        top[2] = bot[2] = adjust_value(pygame.K_r, pygame.K_f, top[2])
        bot[1] = max(top[1], min(bot[1], self.size[1]))

        self.top_lip.set_increments(top)
        self.bot_lip.set_increments(bot)

    def handle_event(self, event):
        pass
