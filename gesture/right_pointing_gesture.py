from vision.handtracker import HandResult
from gesture.gesture import AbstractGesture, X_COORDINATE_POSITION, Y_COORDINATE_POSITION, INDEX_FINGER_PIP_ID, \
    INDEX_FINGER_TIP_ID

X_TRASH_HOLD = 10
Y_TRASH_HOLD_ASPECT_RATIO = 0.20


class RightPointingGesture(AbstractGesture):

    def is_gesture(self, hand: HandResult) -> bool:
        if hand:
            index_finger_pip_x = hand.landmarks[INDEX_FINGER_PIP_ID][X_COORDINATE_POSITION]
            index_finger_tip_x = hand.landmarks[INDEX_FINGER_TIP_ID][X_COORDINATE_POSITION]

            index_finger_tip_y = hand.landmarks[INDEX_FINGER_TIP_ID][Y_COORDINATE_POSITION]
            index_finger_pip_y = hand.landmarks[INDEX_FINGER_PIP_ID][Y_COORDINATE_POSITION]

            tip_finger_diff = index_finger_tip_x - index_finger_pip_x

            # If tip of index finger has X coordinate > than pip of index = points to right side
            is_pointing_to_right_side = tip_finger_diff > X_TRASH_HOLD

            is_pointing_horizontally = abs(index_finger_tip_y - index_finger_pip_y) < tip_finger_diff * Y_TRASH_HOLD_ASPECT_RATIO

            # Assume pointing to right when index points to right side and pointing horizontally
            if is_pointing_to_right_side and is_pointing_horizontally:
                return True

        return False

    def do_command(self):
        print()
