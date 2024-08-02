import screeninfo
import pygame
import os
import sys


class SandBox:
    WINDOW_SIZE = 960, 640
    BACKGROUND_COLOR = (100, 139, 127)
    HEWO_DISPLAY = 0
    HEWO_MONITOR_NAME = "DP-1"

    def __init__(self, elements=None):
        pygame.init()
        self.find_and_set_display()
        pygame.display.set_caption("Testing Sandbox")
        print("Press F to toggle fullscreen.")
        self.clock = pygame.time.Clock()
        self.running = True
        self.is_fullscreen = False
        self.elements = elements
        self.screen = pygame.display.set_mode(size=self.WINDOW_SIZE,
                                              flags=pygame.RESIZABLE,
                                              display=self.HEWO_DISPLAY)

    def find_and_set_display(self):
        print("Looking for HeWo's display...")
        found = False
        for i, monitor in enumerate(screeninfo.get_monitors()):
            print(f"Display {i}: {monitor.name} - {monitor.width}x{monitor.height}")
            if monitor.name == self.HEWO_MONITOR_NAME:
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
                if event.key == pygame.K_f:
                    if self.HEWO_DISPLAY != 0:
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
