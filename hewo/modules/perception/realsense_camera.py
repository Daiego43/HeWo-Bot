import cv2
import time
import joblib
import numpy as np
import pyrealsense2 as rs
import matplotlib.pyplot as plt
from hewo.modules.perception.vision.mpface import MediaPeopleFaces


class RealSenseCamera:
    def __init__(self, objects):
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
        pipeline_profile = self.config.resolve(pipeline_wrapper)
        device = pipeline_profile.get_device()
        self.device_product_line = str(device.get_info(rs.camera_info.product_line))
        print("Using camera Intel RealSense", self.device_product_line)
        print("Config:", self.config)
        self.width = 640
        self.height = 480
        self.fps = 30
        self.config.enable_stream(rs.stream.depth, self.width, self.height, rs.format.z16, self.fps)
        self.config.enable_stream(rs.stream.color, self.width, self.height, rs.format.bgr8, self.fps)
        self.objects = objects

    def get_rgb_frame(self):
        frames = self.pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        if not color_frame:
            return None, None
        color_image = np.asanyarray(color_frame.get_data())
        rgb_frame = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
        return color_image, rgb_frame

    def init_capture(self, person_parts_objects, end=None, plt_rpr=True, cv_rpr=True):
        self.pipeline.start(self.config)
        if plt_rpr:
            fig = plt.figure()
        i = 100 + len(person_parts_objects) * 10 + 1
        start = time.time()
        cond = lambda t: True
        if end is not None:
            cond = lambda t: t - start < end
        try:
            while cond(time.time()):
                img, rgb = self.get_rgb_frame()
                if img is not None:
                    if plt_rpr:
                        plt.clf()
                    for obj in person_parts_objects:
                        img = obj.draw_landmarks(img, rgb)
                        if plt_rpr:
                            ax = fig.add_subplot(i, projection='3d')
                            obj.plt_3D_repr(ax)
                            i += 1
                    i = 100 + len(person_parts_objects) * 10 + 1
                    if cv_rpr:
                        cv2.imshow('RGB', img)
                        cv2.waitKey(1)
                    if plt_rpr:
                        plt.pause(0.00000001)
        finally:
            self.pipeline.stop()
            cv2.destroyAllWindows()
