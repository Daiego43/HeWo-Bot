import screeninfo
import pygame
import os
import sys


class SandBox:
    WINDOW_WIDTH = 960
    WINDOW_HEIGHT = 640
    BACKGROUND_COLOR = (100, 139, 127)

    def __init__(self, elements=None):
        pygame.init()
        self.find_and_set_display()
        pygame.display.set_caption("Testing Sandbox")
        print("Press F to toggle fullscreen.")
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.is_fullscreen = False
        self.elements = elements

    def find_and_set_display(self):
        for monitor in screeninfo.get_monitors():
            if monitor.width == self.WINDOW_WIDTH and monitor.height == self.WINDOW_HEIGHT:
                os.environ['SDL_VIDEO_WINDOW_POS'] = f"{monitor.x},{monitor.y}"
                break

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        self.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    self.toggle_fullscreen()
            if self.elements is not None:
                for elem in self.elements:
                    elem.handle_event(event)

    def update(self):
        if self.elements is not None:
            for elem in self.elements:
                elem.update()

    def draw(self):
        self.screen.fill(self.BACKGROUND_COLOR)
        if self.elements is not None:
            for elem in self.elements:
                elem.draw(self.screen)
        pygame.display.flip()

    def toggle_fullscreen(self):
        if self.is_fullscreen:
            self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT), pygame.RESIZABLE)
            self.is_fullscreen = False
        else:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.is_fullscreen = True

    def quit(self):
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = SandBox()
    game.run()
