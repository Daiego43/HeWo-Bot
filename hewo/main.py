from hewo.sandbox import SandBox
from hewo.face import HeWoFace

if __name__ == '__main__':
    elements = [
        HeWoFace(enable_follow_mouse=False)
    ]
    sandbox = SandBox(elements)
    sandbox.run()
