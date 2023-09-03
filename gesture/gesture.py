import time
from abc import ABC, abstractmethod
from vision.handtracker import HandResult

# Coordinates po
X_COORDINATE_POSITION = 0
Y_COORDINATE_POSITION = 1

# Index finger ids
INDEX_FINGER_PIP_ID = 6
INDEX_FINGER_TIP_ID = 8

# Middle finger ids
MIDDLE_FINGER_TIP_ID = 12
MIDDLE_FINGER_PIP_ID = 10

# Ring finger ids
RING_FINGER_TIP_ID = 16
RING_FINGER_PIP_ID = 14

# Pinky finger ids
PINKY_FINGER_TIP_ID = 20
PINKY_FINGER_PIP_ID = 18

COMMAND_RATE_TIME_LIMIT_SECONDS = 2

X_TRASH_HOLD = 10
Y_TRASH_HOLD = 10
X_TRASH_HOLD_ASPECT_RATION = 0.2
# Aspect ratio allows to check is finger pointing horizontally on any distance from camera
Y_TRASH_HOLD_ASPECT_RATIO = 0.2


def is_pointing_horizontally(hand):
    index_finger_pip_x = hand.landmarks[INDEX_FINGER_PIP_ID][X_COORDINATE_POSITION]
    index_finger_tip_x = hand.landmarks[INDEX_FINGER_TIP_ID][X_COORDINATE_POSITION]

    index_finger_tip_y = hand.landmarks[INDEX_FINGER_TIP_ID][Y_COORDINATE_POSITION]
    index_finger_pip_y = hand.landmarks[INDEX_FINGER_PIP_ID][Y_COORDINATE_POSITION]

    tip_finger_diff = abs(index_finger_pip_x - index_finger_tip_x)

    return abs(index_finger_tip_y - index_finger_pip_y) < tip_finger_diff * Y_TRASH_HOLD_ASPECT_RATIO


def is_pointing_vertically(hand):
    index_finger_pip_x = hand.landmarks[INDEX_FINGER_PIP_ID][X_COORDINATE_POSITION]
    index_finger_tip_x = hand.landmarks[INDEX_FINGER_TIP_ID][X_COORDINATE_POSITION]

    index_finger_tip_y = hand.landmarks[INDEX_FINGER_TIP_ID][Y_COORDINATE_POSITION]
    index_finger_pip_y = hand.landmarks[INDEX_FINGER_PIP_ID][Y_COORDINATE_POSITION]

    tip_finger_diff = abs(index_finger_pip_y - index_finger_tip_y)

    return abs(index_finger_tip_x - index_finger_pip_x) < tip_finger_diff * X_TRASH_HOLD_ASPECT_RATION


class AbstractGesture(ABC):

    def __init__(self, on_gesture_handler):
        self.on_gesture_handler = on_gesture_handler

    @abstractmethod
    def is_gesture(self, hand: HandResult) -> bool:
        pass

    def do_command(self, *args):
        self.on_gesture_handler(*args)


class RateLimitedAbstractGesture(AbstractGesture):

    def __init__(self, on_gesture_handler, command_rate_time=COMMAND_RATE_TIME_LIMIT_SECONDS):
        super().__init__(on_gesture_handler)
        self.last_execution_time = time.time()
        self.command_rate_time = command_rate_time

    def is_gesture(self, hand: HandResult) -> bool:
        current_time = time.time()
        if current_time - self.last_execution_time > self.command_rate_time:
            is_gesture = self._is_gesture(hand)
            if is_gesture:
                self.last_execution_time = current_time

            return is_gesture

    @abstractmethod
    def _is_gesture(self, hand: HandResult) -> bool:
        pass


class LeftPointingGesture(RateLimitedAbstractGesture):

    def __init__(self, on_gesture_handler):

        super().__init__(on_gesture_handler)

    def _is_gesture(self, hand: HandResult) -> bool:
        if hand:
            index_finger_pip_x = hand.landmarks[INDEX_FINGER_PIP_ID][X_COORDINATE_POSITION]
            index_finger_tip_x = hand.landmarks[INDEX_FINGER_TIP_ID][X_COORDINATE_POSITION]

            tip_finger_diff = index_finger_pip_x - index_finger_tip_x

            # If pip of index finger has X coordinate > than tip of index = points to left side
            is_pointing_to_left_side = tip_finger_diff > X_TRASH_HOLD

            # Assume pointing to left when index points to left side and pointing horizontally
            if is_pointing_to_left_side and is_pointing_horizontally(hand):
                return True

        return False

    def _is_rest_fingers_are_closed(self, hand: HandResult):
        pass


class RightPointingGesture(RateLimitedAbstractGesture):

    def _is_gesture(self, hand: HandResult) -> bool:
        if hand:
            index_finger_pip_x = hand.landmarks[INDEX_FINGER_PIP_ID][X_COORDINATE_POSITION]
            index_finger_tip_x = hand.landmarks[INDEX_FINGER_TIP_ID][X_COORDINATE_POSITION]

            tip_finger_diff = index_finger_tip_x - index_finger_pip_x

            # If tip of index finger has X coordinate > than pip of index = points to right side
            is_pointing_to_right_side = tip_finger_diff > X_TRASH_HOLD

            # Assume pointing to right when index points to right side and pointing horizontally
            if is_pointing_to_right_side and is_pointing_horizontally(hand):
                return True

        return False


class UpPointingGesture(RateLimitedAbstractGesture):

    def _is_gesture(self, hand: HandResult) -> bool:
        if hand:
            index_finger_pip_y = hand.landmarks[INDEX_FINGER_PIP_ID][Y_COORDINATE_POSITION]
            index_finger_tip_y = hand.landmarks[INDEX_FINGER_TIP_ID][Y_COORDINATE_POSITION]

            tip_finger_diff = index_finger_pip_y - index_finger_tip_y

            # If tip of index finger has Y coordinate > than pip of index = points to up
            is_pointing_up = tip_finger_diff > Y_TRASH_HOLD

            # Assume pointing to right when index points to right side and pointing horizontally
            if is_pointing_up and is_pointing_vertically(hand):
                return True

        return False


class DownPointingGesture(RateLimitedAbstractGesture):

    def _is_gesture(self, hand: HandResult) -> bool:
        if hand:
            index_finger_pip_y = hand.landmarks[INDEX_FINGER_PIP_ID][Y_COORDINATE_POSITION]
            index_finger_tip_y = hand.landmarks[INDEX_FINGER_TIP_ID][Y_COORDINATE_POSITION]

            tip_finger_diff = index_finger_tip_y - index_finger_pip_y

            # If tip of index finger has Y coordinate > than pip of index = points to up
            is_pointing_up = tip_finger_diff > Y_TRASH_HOLD

            # Assume pointing to right when index points to right side and pointing horizontally
            if is_pointing_up and is_pointing_vertically(hand):
                return True

        return False


class HandClosedFistGesture(RateLimitedAbstractGesture):

    def __init__(self, on_gesture_handler):
        super().__init__(on_gesture_handler)

    def _is_gesture(self, hand: HandResult) -> bool:
        index_finger_tip_y = hand.landmarks[INDEX_FINGER_TIP_ID][Y_COORDINATE_POSITION]
        index_finger_pip_y = hand.landmarks[INDEX_FINGER_PIP_ID][Y_COORDINATE_POSITION]

        middle_finger_tip_y = hand.landmarks[MIDDLE_FINGER_TIP_ID][Y_COORDINATE_POSITION]
        middle_finger_pip_y = hand.landmarks[MIDDLE_FINGER_PIP_ID][Y_COORDINATE_POSITION]

        ring_finger_tip_y = hand.landmarks[RING_FINGER_TIP_ID][Y_COORDINATE_POSITION]
        ring_finger_pip_y = hand.landmarks[RING_FINGER_PIP_ID][Y_COORDINATE_POSITION]

        pinky_finger_tip_y = hand.landmarks[PINKY_FINGER_TIP_ID][Y_COORDINATE_POSITION]
        pinky_finger_pip_y = hand.landmarks[PINKY_FINGER_PIP_ID][Y_COORDINATE_POSITION]

        return index_finger_tip_y > index_finger_pip_y \
            and middle_finger_tip_y > middle_finger_pip_y \
            and ring_finger_tip_y > ring_finger_pip_y \
            and pinky_finger_tip_y > pinky_finger_pip_y
