from hewo.game.scenes.sandbox import SandBox
from hewo.game.characters.hewo.face import HewoFace
from hewo.settings.settings_loader import SettingsLoader

LOADER = SettingsLoader().load_settings('hewo.settings.game')
FULLSCREEN = LOADER['game']['display']['fullscreen']
FOLLOW_MOUSE = False
TRACKING = False

if __name__ == '__main__':
    elements = [
        HewoFace(),
    ]
    sandbox = SandBox(elements, fullscreen=FULLSCREEN)
    sandbox.run()
