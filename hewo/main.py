from hewo.game_elements.scenes.sandbox import SandBox
from hewo.game_elements.characters.hewo.face import HeWoFace

if __name__ == '__main__':
    elements = [
        HeWoFace(enable_follow_mouse=False,
                 enable_tracking=True),
    ]
    sandbox = SandBox(elements, fullscreen=True)
    sandbox.run()
