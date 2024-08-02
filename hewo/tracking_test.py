import joblib
import time

from hewo.modules.perception.realsense_camera import RealSenseCamera
from hewo.modules.perception.vision.mppeople import MediaPeopleFaces


def timeit(func):
    def wrapper(*args, **kwargs):
        init = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"Time: {time.perf_counter() - init} sec")
        return result

    return wrapper


def save_person(person):
    with open('person.pkl', 'wb') as f:
        stuff_to_save = {
            'face_list': person.face_list,
            'pose_list': person.pose_list,
            'bbox_list': person.bbox_list,
            'hand_list': person.hand_list,
        }
        joblib.dump(stuff_to_save, f)


def main():
    objects = [MediaPeopleFaces()]
    camera = RealSenseCamera(objects=objects)
    camera.viewer(end=10, cv_rpr=True)
    camera.start_camera()
    while True:
        objects = camera.get_objects()
        print(objects[0].get_bbox_list())


if __name__ == '__main__':
    main()
