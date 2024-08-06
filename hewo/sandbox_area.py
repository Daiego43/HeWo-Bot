from hewo.game.scenes.sandbox import SandBox
from hewo.game.characters.hewo.eye import Eye
from hewo.game.characters.hewo.mouth import Mouth
from hewo.settings.settings_loader import SettingsLoader

LOADER = SettingsLoader().load_settings('hewo.settings.game')
FULLSCREEN = LOADER['game']['display']['fullscreen']
FOLLOW_MOUSE = False
TRACKING = False

if __name__ == '__main__':
    size = (960, 640)
    pos = [0, 0]
    e_size = (size[0] / 5, size[1] / 5 * 4)
    m_size = (size[0] / 5 * 3, size[1] / 5)
    l_pos = pos
    r_pos = [e_size[0] * 4, 0]

    m_pos = [e_size[0], e_size[1]]
    elements = [
        Eye(e_size, l_pos),
        Eye(e_size, r_pos),
        Mouth(m_size, m_pos)
    ]
    sandbox = SandBox(elements, fullscreen=FULLSCREEN)
    sandbox.run()
