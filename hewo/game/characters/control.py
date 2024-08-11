import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox


class VariableSlider:
    def __init__(self, surface, x=15, y=10, variable_name='sample', width=250, height=20, min_val=0, max_val=100,
                 step=1):
        self.surface = surface
        self.variable_name = variable_name
        self.slider = Slider(self.surface, x, y + 5, width, height, min=min_val, max=max_val, step=step)
        self.output = TextBox(self.surface, x + width + 20, y, 120, 30, fontSize=20)
        self.output.disable()

    def update(self):
        events = pygame.event.get()
        value = self.slider.getValue()
        self.output.setText(f'{self.variable_name}: {value}')
        pygame_widgets.update(events)
        return value


class FaceControls:
    """
    A surface that contains sliders to control variables in your game.
    """
    vars = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'L', 'M', 'N', 'O', 'P']
    win_width = 425
    win_height = 10 + 30 * len(vars) + 10

    def __init__(self, position=(0, 0)):
        pygame.init()
        self.position = position
        self.surface = pygame.Surface((self.win_width, self.win_height))
        self.values = [0 for _ in range(len(self.vars))]
        self.sliders = []
        y = 10
        for var in self.vars:
            self.sliders.append(VariableSlider(self.surface, variable_name=var, y=y))
            y += 30

    def update(self):
        for i, slider in enumerate(self.sliders):
            val = slider.update()
            self.values[i] = val

    def draw(self, surface):
        surface.blit(self.surface, self.position)

    def handle_event(self, event):
        pass


class ControlWindow:
    """
    A separate window that displays the ControlSurface.
    """

    def __init__(self):
        pygame.init()
        self.win_width = FaceControls.win_width
        self.win_height = FaceControls.win_height
        self.screen = pygame.display.set_mode((self.win_width, self.win_height))
        pygame.display.set_caption("Control Window")

        self.control_surface = FaceControls()
        self.running = True

    def run(self):
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            self.control_surface.update(events)
            self.screen.fill((255, 255, 255))  # Clear screen with white
            self.control_surface.draw(self.screen)
            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    # Create and run the control window
    control_window = ControlWindow()
    control_window.run()
