import screeninfo
import pygame
import os
import sys
from hewo.settings.settings_loader import SettingsLoader

SETTINGS = SettingsLoader().load_settings('hewo.settings.game')


class SandBox:
    display = SETTINGS['game']['display']
    WINDOW_SIZE = (
        display['width'],
        display['height']
    )
    BACKGROUND_COLOR = (display['bg_color']['r'],
                        display['bg_color']['g'],
                        display['bg_color']['b'])
    HEWO_DISPLAY = display['id']
    HEWO_MONITOR_NAME = display['name']

    def __init__(self, elements=None, fullscreen=False):
        pygame.init()
        self.find_and_set_display()
        pygame.display.set_caption("Testing Sandbox")
        print("Press F to toggle fullscreen.")
        self.clock = pygame.time.Clock()
        self.running = True
        self.is_fullscreen = fullscreen
        self.elements = elements

        if self.is_fullscreen:
            flags = pygame.FULLSCREEN
        else:
            flags = pygame.RESIZABLE

        self.screen = pygame.display.set_mode(size=self.WINDOW_SIZE,
                                              flags=flags,
                                              display=self.HEWO_DISPLAY,
                                              vsync=True)

    def find_and_set_display(self):
        print("Looking for HeWo's display...")
        found = False
        for i, monitor in enumerate(screeninfo.get_monitors()):
            if monitor.width == self.WINDOW_SIZE[0] and monitor.height == self.WINDOW_SIZE[1]:
                self.HEWO_DISPLAY = i
                self.WINDOW_SIZE = monitor.width, monitor.height
                os.environ['SDL_VIDEO_WINDOW_POS'] = f"{monitor.x},{monitor.y}"
                print("HeWo's display found!")
                found = True
                break

        if not found:
            print("HeWo's display not found. Using default")
            print("Full screen will be disabled.")
            self.HEWO_DISPLAY = 0
            self.WINDOW_SIZE = 960, 640

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
                if event.key == pygame.K_1:
                    if self.HEWO_DISPLAY != 0:
                        self.toggle_fullscreen()
                if event.key == pygame.K_ESCAPE:
                    self.running = False
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
            self.screen = pygame.display.set_mode(size=self.WINDOW_SIZE,
                                                  flags=pygame.RESIZABLE,
                                                  display=self.HEWO_DISPLAY,
                                                  vsync=True)
            self.is_fullscreen = False
        else:
            self.screen = pygame.display.set_mode(size=self.WINDOW_SIZE,
                                                  flags=pygame.FULLSCREEN,
                                                  display=self.HEWO_DISPLAY,
                                                  vsync=True)
            self.is_fullscreen = True
        pygame.display.flip()  # Asegurarse de que la pantalla se actualice inmediatamente

    def quit(self):
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = SandBox()
    game.run()
