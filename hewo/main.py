from hewo.game.scenes.sandbox import SandBox
from hewo.game.characters.hewo.face import HeWoFace

TRACKING = True
FOLLOW_MOUSE = False
FULLSCREEN = False


if __name__ == '__main__':
    elements = [
        HeWoFace(enable_follow_mouse=FOLLOW_MOUSE,
                 enable_tracking=TRACKING)
    ]
    sandbox = SandBox(elements, fullscreen=FULLSCREEN)
    sandbox.run()











