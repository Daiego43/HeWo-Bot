from hewo.game.scenes.sandbox import SandBox
from hewo.game.characters.hewo.eye import Eye
from hewo.settings.settings_loader import SettingsLoader

LOADER = SettingsLoader().load_settings('hewo.settings.game')
FULLSCREEN = LOADER['game']['display']['fullscreen']
FOLLOW_MOUSE = False
TRACKING = False

if __name__ == '__main__':
    size = (960, 640)
    pos = [0, 0]
    eye_size = (size[0] / 5, size[1] / 5 * 4)

    l_pos = pos
    r_pos = [eye_size[0] * 4, 0]

    elements = []
    for i in range(5):
        eye = Eye(eye_size, (eye_size[0] * i, 0))
        elements.append(eye)
    elements = [
        Eye(eye_size, l_pos),
        Eye(eye_size, r_pos)
    ]
    sandbox = SandBox(elements, fullscreen=FULLSCREEN)
    sandbox.run()
