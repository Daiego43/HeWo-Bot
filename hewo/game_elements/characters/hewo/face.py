import random

import pygame
from hewo.game_elements.characters.hewo.eyes import HeWoEye
from hewo.game_elements.characters.hewo.mouth import HeWoMouth
from hewo.game_elements.scenes.sandbox import SandBox
from hewo.modules.perception.realsense_camera import RealSenseCamera
from hewo.modules.perception.vision.mppeople import MediaPeopleFaces


class HeWoFace:
    FACE_SURFACE = (960, 640)
    MOUTH_SIZE = (FACE_SURFACE[0] // 6, FACE_SURFACE[1] // 6)
    MOUTH_BBOX = ((MOUTH_SIZE[0] // 2, FACE_SURFACE[0] - MOUTH_SIZE[0] // 2),
                  (MOUTH_SIZE[1], FACE_SURFACE[1]))

    DISTANCE_BETWEEN_EYES = MOUTH_SIZE[0]

    LEFT_EYE_SIZE = (FACE_SURFACE[0] // 20, FACE_SURFACE[1] // 4)
    LEFT_EYE_BBOX = ((0, FACE_SURFACE[0] - DISTANCE_BETWEEN_EYES - LEFT_EYE_SIZE[0] * 2.5),
                     (0, FACE_SURFACE[1] - MOUTH_SIZE[1]))

    RIGHT_EYE_SIZE = (FACE_SURFACE[0] // 20, FACE_SURFACE[1] // 4)
    RIGHT_EYE_BBOX = ((DISTANCE_BETWEEN_EYES + RIGHT_EYE_SIZE[0] * 2.5, FACE_SURFACE[0]),
                      (0, FACE_SURFACE[1] - MOUTH_SIZE[1]))

    MOVE_STEP = 15

    def __init__(self, enable_follow_mouse=False, enable_tracking=True):
        self.elements = []
        self.move_step = self.MOVE_STEP
        self.elements.append(HeWoEye(name="left",
                                     bbox=self.LEFT_EYE_BBOX,
                                     size=self.LEFT_EYE_SIZE))
        self.elements.append(HeWoEye(name="right",
                                     bbox=self.RIGHT_EYE_BBOX,
                                     size=self.RIGHT_EYE_SIZE))
        self.elements.append(HeWoMouth(name="mouth",
                                       size=self.MOUTH_SIZE,
                                       bbox=self.MOUTH_BBOX))
        self.enable_follow_mouse = enable_follow_mouse
        self.enable_tracking = enable_tracking
        self.face_tracker = RealSenseCamera([MediaPeopleFaces()])
        if enable_tracking:
            self.face_tracker.start_camera()

    def update(self):
        self.handle_input()
        if self.enable_follow_mouse:
            self.follow_mouse()
        if self.enable_tracking:
            self.track()
        for elem in self.elements:
            elem.update()

    def random_blink(self):
        blinking_rate = 60 * random.randint(1, 5)
        self.elements[0].blink_rate = blinking_rate
        self.elements[1].blink_rate = blinking_rate

    def track(self):
        # Always tracking the face at 0
        face_result = self.face_tracker.get_objects()[0]
        if face_result.get_bbox_list():
            bbox = face_result.get_bbox_list()[0]
            center = (bbox[0] + bbox[2] // 2, (bbox[1] + bbox[3] // 2))
            center = self.transform_to_screen_coordinates(center)
            self.set_elems_pos(center)

    def transform_to_screen_coordinates(self, center):
        # Transform coordinates from camera to screen and invert x-axis
        camera_x, camera_y = center
        inverted_camera_x = 640 - camera_x
        screen_x = int(inverted_camera_x * self.FACE_SURFACE[0] / 640)
        screen_y = int(camera_y * self.FACE_SURFACE[1] / 480)
        return screen_x, screen_y

    def draw(self, screen):
        for elem in self.elements:
            elem.draw(screen)

    def handle_event(self, event):
        for elem in self.elements:
            elem.handle_event(event)

    def handle_input(self):
        for elem in self.elements:
            elem.handle_input(step=self.MOVE_STEP)

    def set_elems_pos(self, pos):
        distance_to_mouth = 50
        for elem in self.elements:
            if elem.name == 'mouth':
                elem.set_position((pos[0], pos[1]))
            elif elem.name == 'left':
                elem.set_position((pos[0] - distance_to_mouth, pos[1]))
            elif elem.name == 'right':
                elem.set_position((pos[0] + self.DISTANCE_BETWEEN_EYES + distance_to_mouth, pos[1]))

    def follow_mouse(self):
        pos = pygame.mouse.get_pos()
        self.set_elems_pos(pos)


if __name__ == '__main__':
    elements = [HeWoFace(enable_follow_mouse=False)]
    sandbox = SandBox(elements)
    sandbox.run()
