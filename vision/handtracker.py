from typing import NamedTuple, List

import cv2
import mediapipe as mp
import numpy as np


class HandResult(NamedTuple):
    landmarks: List[List[int]]
    normalized_landmarks: List[float]
    hand_type: str


def draw_shape_box(img: np.array, hand: HandResult):
    x_hand_coordinates = [landmark[0] for landmark in hand.landmarks]
    y_hand_coordinates = [landmark[1] for landmark in hand.landmarks]

    # Get min max coordinates to draw a box
    x_min, x_max = min(x_hand_coordinates), max(x_hand_coordinates)
    y_min, y_max = min(y_hand_coordinates), max(y_hand_coordinates)

    box_width = x_max - x_min
    box_height = y_max - y_min

    mp.solutions.drawing_utils.draw_landmarks(img, hand.normalized_landmarks, mp.solutions.hands.HAND_CONNECTIONS)

    start_point = (x_min - 20, y_min - 20)
    end_point = (x_min + box_width + 20, y_min + box_height + 20)
    color = (255, 0, 255)
    cv2.rectangle(img, start_point, end_point, color, 2)


class HandTracker:

    def __init__(self, static_img=False, hands=1):
        self.tracker = mp.solutions.hands.Hands(static_img, hands)

    def find_hands(self, img: np.array) -> List[HandResult]:
        """

        :param img: img in RGB format
        :return: List of HandResult that contains detected hands information
        """
        hands = self.tracker.process(img)
        hands_results = []

        if hands.multi_hand_landmarks:

            h, w, c = img.shape

            for hand_type, hand_landmark in zip(hands.multi_handedness, hands.multi_hand_landmarks):
                landmark_coordinates = []
                for landmark in hand_landmark.landmark:
                    # Get coordinates since landmarks are normalized
                    x, y, z = int(landmark.x * w), int(landmark.y * h), int(landmark.z * w)
                    landmark_coordinates.append([x, y, z])
                hand_result = HandResult(landmark_coordinates, hand_landmark, hand_type.classification[0].label)
                hands_results.append(hand_result)

        return hands_results
