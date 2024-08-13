from hewo.game.scenes.sandbox import SandBox
from hewo.game.characters.hewo.face import Face
from hewo.settings.settings_loader import SettingsLoader

display = SettingsLoader().load_settings('settings.displays.test')
max_size = (display['width'], display['height'])
pos = [display['width'] // 5 + 425, display['height'] // 5]

if __name__ == '__main__':
    elements = [
        Face(position=pos, enable_controls=True, max_size=max_size),
    ]
    sandbox = SandBox(elements, fullscreen=False, display=display)
    sandbox.run()
