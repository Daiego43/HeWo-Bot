import pygame
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

    def __init__(self, size, position, flip=False):
        self.size = size
        self.position = position
        self.color = self.COLOR
        self.flip = flip
        self.max_emotion = self.size[1]
        self.emotion = [0, 0, 0]
        self.emotion_pcts = [0.0, 0.0, 0.0]
        self.update_vertices()

    def update(self):
        self.handle_input()
        self.update_vertices()

    def handle_input(self):
        keys = pygame.key.get_pressed()
        pcts = self.emotion_pcts.copy()
        if keys[pygame.K_u]:
            pcts[0] += 0.1
        if keys[pygame.K_j]:
            pcts[0] -= 0.1
        if keys[pygame.K_i]:
            pcts[1] += 0.1
        if keys[pygame.K_k]:
            pcts[1] -= 0.1
        if keys[pygame.K_o]:
            pcts[2] += 0.1
        if keys[pygame.K_l]:
            pcts[2] -= 0.1
        self.set_emotion_by_pct(pcts)

    def update_vertices(self):
        if self.flip:
            self.vertices = [
                (self.position[0], self.position[1] + self.size[1]),
                (self.position[0] + self.size[0], self.position[1] + self.size[1]),
                (self.position[0] + self.size[0], self.position[1] + self.size[1] - self.emotion[2]),
                (self.position[0] + self.size[0] // 2, self.position[1] + self.size[1] - self.emotion[1]),
                (self.position[0], self.position[1] + self.size[1] - self.emotion[0])
            ]
        else:
            self.vertices = [
                (self.position[0], self.position[1]),
                (self.position[0] + self.size[0], self.position[1]),
                (self.position[0] + self.size[0], self.position[1] + self.emotion[2]),
                (self.position[0] + self.size[0] // 2, self.position[1] + self.emotion[1]),
                (self.position[0], self.position[1] + self.emotion[0])
            ]

    def set_emotion_by_pct(self, emotion_pcts):
        for i, p in enumerate(emotion_pcts):
            self.emotion_pcts[i] = min(max(p, 0.0), 1.0)
            self.emotion[i] = self.max_emotion * self.emotion_pcts[i]
        self.update_vertices()

    def set_size(self, size):
        self.size = size
        self.update_vertices()

    def set_position(self, position):
        self.position = position
        self.update_vertices()

    def draw(self, surface):
        pygame.draw.polygon(surface, self.color, self.vertices)

    def handle_event(self, event):
        pass


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
        self.top_pos = (0, 0)
        self.bottom_pos = (0, self.size[1] // 2)
        self.elements = [
            Pupil(size=self.size, position=self.position),
            EyeLash(size=self.lash_size, position=self.top_pos),
            EyeLash(size=self.lash_size, position=self.bottom_pos, flip=True)
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
        for elem in self.elements:
            elem.update()


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
