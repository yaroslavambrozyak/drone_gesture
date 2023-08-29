from abc import ABC, abstractmethod
import cv2

class CamFrameProvider(ABC):

    @abstractmethod
    def get_frame(self):
        pass


class CV2CamFrameProvider(CamFrameProvider):

    def __init__(self, cam_id=0):
        self.cap = cv2.VideoCapture(cam_id)

    def get_frame(self):
        return self.cap.read()
