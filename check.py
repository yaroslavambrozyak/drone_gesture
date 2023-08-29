import cv2
from vision.handtracker import HandTracker
from gesture.right_pointing_gesture import RightPointingGesture


def main():
    cap = cv2.VideoCapture(0)

    tracker = HandTracker()
    r_ges = RightPointingGesture()

    while True:
        success, img = cap.read()

        img = cv2.flip(img, 1)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        hands = tracker.find_hands(img_rgb)
        for hand in hands:
            tracker.draw_shape_box(img, hand)
            isq = r_ges.is_gesture(hand)
            print(isq)


        cv2.imshow("img", img)

        cv2.waitKey(1)


if __name__ == "__main__":
    main()