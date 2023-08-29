from abc import ABC, abstractmethod

from vision.handtracker import HandResult

# Coordinates po
X_COORDINATE_POSITION = 0
Y_COORDINATE_POSITION = 1

# Index finger ids
INDEX_FINGER_PIP_ID = 6
INDEX_FINGER_TIP_ID = 8


class AbstractGesture(ABC):

    @abstractmethod
    def is_gesture(self, hand: HandResult) -> bool:
        pass
