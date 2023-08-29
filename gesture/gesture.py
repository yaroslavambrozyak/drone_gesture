from vision.handtracker import HandResult

# Coordinates po
X_COORDINATE_POSITION = 0
Y_COORDINATE_POSITION = 1

# Index finger ids
INDEX_FINGER_PIP_ID = 6
INDEX_FINGER_TIP_ID = 8


class AbstractGesture:

    def get_coordinate(self, hand: HandResult, coordinate_id: int, scale_id: int):
        if hand:
            return hand.landmarks[coordinate_id][scale_id]
