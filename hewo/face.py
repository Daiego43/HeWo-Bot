import pygame
from hewo.eyes import HeWoEyes
from hewo.mouth import HeWoMouth
from hewo.sandbox import SandBox


class HeWoFace:

    def __init__(self, enable_teleop=False):
        self.eyes = HeWoEyes(enable_teleop=enable_teleop)
        self.mouth = HeWoMouth(enable_teleop=enable_teleop)

    def update(self):
        self.eyes.update()
        self.mouth.update()

    def draw(self, screen):
        self.eyes.draw(screen)
        self.mouth.draw(screen)

    def handle_event(self, event):
        self.mouth.handle_event(event)
        self.eyes.handle_event(event)


if __name__ == '__main__':
    elements = [HeWoFace(enable_teleop=True)]
    sandbox = SandBox(elements)
    sandbox.run()
