import cv2
from vision.handtracker import HandTracker
import gesture.pointing_gesture as p_ges
from vision.camera import CV2CamFrameProvider

gestures = [
    p_ges.RightPointingGesture(),
    p_ges.LeftPointingGesture(),
    p_ges.UpPointingGesture(),
    p_ges.DownPointingGesture()
]


def main():
    frame_provider = CV2CamFrameProvider(0)
    tracker = HandTracker(hands=1)

    while True:
        success, img = frame_provider.get_frame()

        img = cv2.flip(img, 1)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        hands = tracker.find_hands(img_rgb)

        if len(hands) == 1:
            hand = hands[0]
            gesture = get_gesture(hand)
            if gesture:
                print(gesture.__class__.__name__)
                # gesture.do_command()
            tracker.draw_shape_box(img, hand)
        cv2.imshow("img", img)
        cv2.waitKey(1)


def get_gesture(hand):
    for gesture in gestures:
        if gesture.is_gesture(hand):
            return gesture


if __name__ == "__main__":
    main()
