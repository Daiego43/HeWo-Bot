from hewo_bot.game.scenes.sandbox import SandBox
from hewo_bot.game.characters.hewo.face_components.face import Face
from hewo_bot.settings.settings_loader import SettingsLoader

display = SettingsLoader().load_settings('settings.displays.main')

max_size = (display['width'], display['height'])
pos = [display['width'] // 5, display['height'] // 5]

if __name__ == '__main__':
    elements = [
        Face(position=pos, enable_controls=False, max_size=max_size),
    ]
    sandbox = SandBox(elements, fullscreen=False, display=display)
    sandbox.run()
