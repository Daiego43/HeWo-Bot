import pygame
from hewo.eyes import HeWoEye
from hewo.mouth import HeWoMouth
from hewo.sandbox import SandBox


class HeWoFace:
    FACE_SURFACE = (960, 640)
    MOUTH_SIZE = (FACE_SURFACE[0] // 6, FACE_SURFACE[1] // 6)
    MOUTH_BBOX = ((MOUTH_SIZE[0] // 2, FACE_SURFACE[0] - MOUTH_SIZE[0] // 2),
                  (MOUTH_SIZE[1], FACE_SURFACE[1]))

    DISTANCE_BETWEEN_EYES = MOUTH_SIZE[0]

    LEFT_EYE_SIZE = (FACE_SURFACE[0] // 20, FACE_SURFACE[1] // 4)
    LEFT_EYE_BBOX = ((0, FACE_SURFACE[0] - DISTANCE_BETWEEN_EYES - LEFT_EYE_SIZE[0] * 2.5),
                     (0, FACE_SURFACE[1] - MOUTH_SIZE[1]))

    RIGHT_EYE_SIZE = (FACE_SURFACE[0] // 20, FACE_SURFACE[1] // 4)
    RIGHT_EYE_BBOX = ((DISTANCE_BETWEEN_EYES + RIGHT_EYE_SIZE[0] * 2.5, FACE_SURFACE[0]),
                      (0, FACE_SURFACE[1] - MOUTH_SIZE[1]))

    MOVE_STEP = 15

    def __init__(self, enable_follow_mouse=False):
        self.elements = []
        self.move_step = self.MOVE_STEP
        self.elements.append(HeWoEye(name="left",
                                     bbox=self.LEFT_EYE_BBOX,
                                     size=self.LEFT_EYE_SIZE))
        self.elements.append(HeWoEye(name="right",
                                     bbox=self.RIGHT_EYE_BBOX,
                                     size=self.RIGHT_EYE_SIZE))
        self.elements.append(HeWoMouth(name="mouth",
                                       size=self.MOUTH_SIZE,
                                       bbox=self.MOUTH_BBOX))
        self.enable_follow_mouse = enable_follow_mouse

    def update(self):
        self.handle_input()
        if self.enable_follow_mouse:
            self.follow_mouse()
        for elem in self.elements:
            elem.update()

    def draw(self, screen):
        for elem in self.elements:
            elem.draw(screen)

    def handle_event(self, event):
        for elem in self.elements:
            elem.handle_event(event)

    def handle_input(self):
        for elem in self.elements:
            elem.handle_input(step=self.MOVE_STEP)

    def follow_mouse(self):
        pos = pygame.mouse.get_pos()
        for elem in self.elements:
            if elem.name == 'mouth':
                elem.set_position((pos[0], pos[1]))
            elif elem.name == 'left':
                elem.set_position((pos[0] - 35, pos[1]))
            elif elem.name == 'right':
                elem.set_position((pos[0] + self.DISTANCE_BETWEEN_EYES + 35, pos[1]))


if __name__ == '__main__':
    elements = [HeWoFace(enable_follow_mouse=False)]
    sandbox = SandBox(elements)
    sandbox.run()
