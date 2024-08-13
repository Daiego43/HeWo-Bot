import pygame
import numpy as np
from scipy.interpolate import make_interp_spline
from settings.settings_loader import SettingsLoader

settings = SettingsLoader().load_settings("settings.hewo")
mouth = settings['elements']['mouth']


class Lip:
    LIP_WIDTH = 5

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
            clamped_value = max(self.LIP_WIDTH, min(point, self.size[1] - self.LIP_WIDTH))
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
        pygame.draw.lines(surface, self.color, False, points, self.LIP_WIDTH)

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

    def __init__(self, size, position, color=COLOR, init_emotion=[[0, 0, 0], [0, 0, 0]]):
        self.size = size
        self.position = position
        self.surface = pygame.Surface(self.size)
        self.color = color

        self.top_lip_emotion = init_emotion[0]
        self.bot_lip_emotion = init_emotion[1]
        self.top_lip = Lip(self.size, self.position, self.TOP_LIP)
        self.bot_lip = Lip(self.size, self.position, self.BOT_LIP)

    def draw(self, surface):
        self.surface.fill(self.color)
        self.top_lip.draw(self.surface)
        self.bot_lip.draw(self.surface)
        surface.blit(self.surface, self.position)

    def update(self):
        self.top_lip.update()
        self.bot_lip.update()

    def handle_event(self, event):
        pass

    def set_emotion(self, top_lip_percentages, bot_lip_percentages):
        """
        Set the emotions of the lips using percentage values (0% to 100%).
        """

        def percentage_to_pixel(value, size):
            return int(value / 100 * size)

        self.top_lip_emotion = [percentage_to_pixel(val, self.size[1]) for val in top_lip_percentages]
        self.bot_lip_emotion = [percentage_to_pixel(val, self.size[1]) for val in bot_lip_percentages]
        self.top_lip.set_increments(self.top_lip_emotion)
        self.bot_lip.set_increments(self.bot_lip_emotion)

    def get_emotion(self):
        """
        Get the emotions of the lips as percentage values (0% to 100%).
        """

        def pixel_to_percentage(value, size):
            return (value / size) * 100

        top_lip_percentages = [pixel_to_percentage(val, self.size[1]) for val in self.top_lip_emotion]
        bot_lip_percentages = [pixel_to_percentage(val, self.size[1]) for val in self.bot_lip_emotion]
        return top_lip_percentages, bot_lip_percentages
