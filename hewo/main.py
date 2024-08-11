from hewo.game.scenes.sandbox import SandBox
from hewo.game.characters.hewo.face import Face
from hewo.game.characters.control import FaceControls
from hewo.settings.settings_loader import SettingsLoader

display = SettingsLoader().load_settings('settings.display')
FULLSCREEN = display['fullscreen']

pos = [display['width'] / 5, display['height'] / 5]

if __name__ == '__main__':
    elements = [
        Face(position=pos),
        FaceControls(position=(0, 0))
    ]
    sandbox = SandBox(elements, fullscreen=FULLSCREEN)
    sandbox.run()
