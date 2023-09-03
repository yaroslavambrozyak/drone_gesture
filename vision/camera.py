from abc import ABC, abstractmethod
import cv2


class CamFrameProvider(ABC):

    @abstractmethod
    def get_frame(self):
        """
        Provides success bool and numpy ndarray which represents a frame in RGB format
        :return: (bool, ndarray)
        """
        pass


class CV2CamFrameProvider(CamFrameProvider):

    def __init__(self, cam_id=0):
        self.cap = cv2.VideoCapture(cam_id)

    def get_frame(self):
        success, img = self.cap.read()
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        return success, img_rgb


class TelloDroneCamFrameProvider(CamFrameProvider):

    def __init__(self, drone):
        self.drone = None

        self.cap = cv2.VideoCapture(0)

    def get_frame(self):
        # img = self.drone.get_frame_read().frame
        # return True, img
        success, img = self.cap.read()
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        return success, img_rgb
