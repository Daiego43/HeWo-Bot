import pygame
from hewo.settings.settings_loader import SettingsLoader

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
        pygame.draw.ellipse(surface, self.color, (self.position[0], self.position[1], self.size[0], self.size[1]))


class EyeBrow:
    COLOR = (0, 100, 0)

    def __init__(self, size, position, flip=False):
        self.size = size
        self.position = position
        self.color = self.COLOR
        self.flip = flip
        self.vertices = [
            (self.position[0], self.position[1]),
            (self.position[0] + self.size[0], self.position[1]),
            (self.size[0], self.position[1] + self.size[1]),
            (self.position[0] + self.size[0] // 2, self.position[1] + self.size[1]),
            (self.position[0], self.position[1] + self.size[1])
        ]
        self.emotion_vertices = [
            [self.size[0], self.position[1] + self.size[1]],
            [self.position[0] + self.size[0] // 2, self.position[1] + self.size[1]],
            [self.position[0], self.position[1] + self.size[1]]
        ]
        self.max_emotion = self.size[1]
        self.emotion = [0, 0, 0]
        self.emotion_pcts = [0.0, 0.0, 0.0]

    def update(self):
        self.handle_input()
        self.max_emotion = self.size[1]

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

    def set_vertices(self, emotion_pcts):
        self.set_emotion_by_pct(emotion_pcts)
        if self.flip:
            self.vertices = [
                (self.position[0], self.position[1] + self.size[1]),
                (self.position[0] + self.size[0], self.position[1] + self.size[1]),
                (self.size[0], self.position[1] + self.size[1] - self.emotion[2]),
                (self.position[0] + self.size[0] // 2, self.position[1] + self.size[1] - self.emotion[1]),
                (self.position[0], self.position[1] + self.size[1] - self.emotion[0])
            ]
        else:
            self.vertices = [
                (self.position[0], self.position[1]),
                (self.position[0] + self.size[0], self.position[1]),
                (self.size[0], self.emotion[2]),
                (self.position[0] + self.size[0] // 2, self.emotion[1]),
                (self.position[0], self.emotion[0])
            ]

    def set_emotion_by_pct(self, emotion_pcts):
        for i, p in enumerate(emotion_pcts):
            self.emotion_pcts[i] = min(max(p, 0.0), 1.0)
            self.emotion[i] = self.max_emotion * self.emotion_pcts[i]

    def set_size(self, size):
        self.size = size

    def set_position(self, position):
        self.position = position

    def draw(self, surface):
        self.set_vertices(self.emotion_pcts)
        seq = self.vertices
        pygame.draw.polygon(surface, self.color, seq)

    def handle_event(self, event):
        pass


class Eye:
    def __init__(self, size=(0, 0), position=(0, 0)):
        self.size = size
        self.position = position
        self.pupil = Pupil(self.size, self.position)
        self.up_brow = EyeBrow(self.size, self.position)
        self.down_brow = EyeBrow(self.size, self.position, flip=True)
        self.set_size(size)
        self.set_position(position)

    def update(self):
        self.up_brow.update()
        self.down_brow.update()

    def set_size(self, size):
        self.size = size
        self.pupil.set_size(size)
        brow_size = (size[0], size[1] // 2)
        self.up_brow.set_size(brow_size)
        self.up_brow.color = (200, 0, 0)  # Color del párpado superior
        self.down_brow.set_size(brow_size)
        self.down_brow.color = (0, 200, 0)  # Color del párpado inferior

    def set_position(self, position):
        self.position = position
        self.up_brow.set_position(self.position)
        self.pupil.set_position(self.position)
        down_pos = (position[0], position[1] + self.size[1] // 2)
        self.down_brow.set_position(down_pos)

    def get_size(self):
        return self.size

    def handle_event(self, event):
        self.pupil.handle_event(event)
        self.up_brow.handle_event(event)
        self.down_brow.handle_event(event)

    def draw(self, surface):
        self.pupil.draw(surface)
        self.up_brow.draw(surface)
        self.down_brow.draw(surface)
