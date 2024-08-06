import pygame
import numpy as np
from scipy.interpolate import make_interp_spline
from hewo.settings.settings_loader import SettingsLoader
from hewo.game.scenes.sandbox import SandBox

eye_settings = SettingsLoader().load_settings("settings.hewo.eye")


class Pupil:
    pupil = eye_settings["pupil"]
    COLOR = (pupil["color"]["r"],
             pupil["color"]["g"],
             pupil["color"]["b"])

    def __init__(self, size, position):
        self.size = size
        self.position = position
        self.color = self.COLOR

    def update(self):
        pass

    def set_size(self, size):
        self.size = size

    def set_position(self, position):
        self.position = position

    def handle_event(self, event):
        pass

    def draw(self, surface):
        pygame.draw.ellipse(surface, self.color, (0, 0, self.size[0], self.size[1]))


class EyeLash:
    lash_settings = eye_settings['lash']
    COLOR = (
        lash_settings['color']['r'],
        lash_settings['color']['g'],
        lash_settings['color']['b'])

    def __init__(self, size, position, color=COLOR, init_pcts=[0, 0, 0], flip=False):
        self.size = size
        self.position = position
        self.color = color
        self.max_emotion = self.size[1]
        self.emotion_pcts = init_pcts
        x, y = position
        w, h = size
        self.polygon_points = [
            [0 + x, 0 + y],
            [0 + x, h + y],
            [w / 2 + x, h + y],
            [w + x, h + y],
            [w + x, 0 + y],
            [w / 2 + x, 0 + y]
        ]
        self.flip = flip
        self.set_points_by_pct(init_pcts)

    def handle_event(self, event):
        pass

    def update(self):
        pass

    def set_points_by_pct(self, emotion):
        self.set_emotion_pcts(emotion)
        indices = [1, 2, 3]
        if self.flip:
            self.emotion_pcts = [100 - e for e in self.emotion_pcts]
            indices = [0, 5, 4]

        for i, tup in enumerate(zip(indices, self.emotion_pcts)):
            self.polygon_points[tup[0]][1] = self.position[1] + self.size[1] * (tup[1] / 100)

    def draw(self, surface):
        points = self.polygon_points[1:4]
        if self.flip:
            points = [self.polygon_points[0], self.polygon_points[5], self.polygon_points[4]]
        ############################
        x_points = np.array([p[0] for p in points])
        y_points = np.array([p[1] for p in points])
        spline = make_interp_spline(x_points, y_points, k=2)
        x_range = np.linspace(min(x_points), max(x_points), 500)
        interpolated_points = [(int(x), int(spline(x))) for x in x_range]
        ############################
        polygon = [self.polygon_points[0]] + interpolated_points + self.polygon_points[4:]
        if self.flip:
            interpolated_points.reverse()
            polygon = self.polygon_points[1:4] + interpolated_points
        pygame.draw.polygon(surface, self.color, polygon)

    def set_emotion_pcts(self, emotion):
        for i, e in enumerate(emotion):
            self.emotion_pcts[i] = max(0, min(e, 100))


class Eye:
    COLOR = (
        eye_settings['canvas']['color']['r'],
        eye_settings['canvas']['color']['g'],
        eye_settings['canvas']['color']['b']
    )

    def __init__(self, size, position):
        self.size = size
        self.position = position
        self.lash_size = (self.size[0], self.size[1] / 2)
        self.t_pos = (0, 0)
        self.b_pos = (0, self.size[1] / 2)
        self.t_emotion = [0, 0, 0]
        self.b_emotion = [0, 0, 0]
        self.elements = [
            Pupil(size=self.size, position=self.position),
            EyeLash(size=self.lash_size, position=self.t_pos, color=[255, 0, 0]),
            EyeLash(size=self.lash_size, position=self.b_pos, color=[0, 255, 0], flip=True)
        ]
        self.eye_surface = pygame.Surface(self.size)

    def handle_event(self, event):
        for elem in self.elements:
            elem.handle_event(event)

    def draw(self, surface):
        self.eye_surface = pygame.surface.Surface(self.size)
        self.eye_surface.fill(self.COLOR)
        for elem in self.elements:
            elem.draw(self.eye_surface)
        surface.blit(self.eye_surface, self.position)

    def update(self):
        self.handle_input()
        for elem in self.elements:
            elem.update()

    def handle_input(self):
        keys = pygame.key.get_pressed()
        emotion = self.t_emotion

        def adjust_value(key_increase, key_decrease, value, step=10):
            if keys[key_increase]:
                value -= step
            if keys[key_decrease]:
                value += step
            return value

        emotion[2] = adjust_value(pygame.K_p, pygame.K_SEMICOLON, emotion[2])
        emotion[1] = adjust_value(pygame.K_o, pygame.K_l, emotion[1])
        emotion[0] = adjust_value(pygame.K_i, pygame.K_k, emotion[0])
        self.set_emotion_pct(emotion)
        self.elements[1].set_points_by_pct(self.t_emotion)
        self.elements[2].set_points_by_pct(self.b_emotion)

    def set_emotion_pct(self, emotion):
        for i, e in enumerate(emotion):
            self.t_emotion[i] = max(0, min(e, 100))
            self.b_emotion[i] = max(0, min(e, 100))


if __name__ == '__main__':
    size = (960, 640)
    position = (0, 0)

    eye_size = (size[0] / 5, size[1] / 5 * 4)
    l_pos = position
    r_pos = (position[0] + size[0] / 5 * 4, 0)
    elements = [
        Eye(eye_size, l_pos),
    ]
    sandbox = SandBox(elements=elements)
    sandbox.run()
