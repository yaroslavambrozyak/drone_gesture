from gesture.gesture import AbstractGesture, X_COORDINATE_POSITION, Y_COORDINATE_POSITION, INDEX_FINGER_PIP_ID, \
    INDEX_FINGER_TIP_ID
from vision.handtracker import HandResult

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


class LeftPointingGesture(AbstractGesture):

    def is_gesture(self, hand: HandResult) -> bool:
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

    def do_command(self):
        print()


class RightPointingGesture(AbstractGesture):

    def is_gesture(self, hand: HandResult) -> bool:
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

    def do_command(self):
        print()


class UpPointingGesture(AbstractGesture):

    def is_gesture(self, hand: HandResult) -> bool:
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

    def do_command(self):
        print()


class DownPointingGesture(AbstractGesture):

    def is_gesture(self, hand: HandResult) -> bool:
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

    def do_command(self):
        print()
