import cv2
from vision.handtracker import HandTracker
import gesture.gesture as gesture
from vision.camera import TelloDroneCamFrameProvider
from djitellopy import tello

DRONE_MOVE_CM = 5

gestures = [
    gesture.RightPointingGesture(lambda drone: drone.move_right(DRONE_MOVE_CM)),
    gesture.LeftPointingGesture(lambda drone: drone.move_left(DRONE_MOVE_CM)),
    gesture.UpPointingGesture(lambda drone: drone.move_up(DRONE_MOVE_CM)),
    gesture.DownPointingGesture(lambda drone: drone.move_down(DRONE_MOVE_CM)),
    gesture.HandClosedFistGesture(lambda drone: drone.land())
]


def main():
    drone = tello.Tello()
    drone.connect()
    drone.streamon()

    frame_provider = TelloDroneCamFrameProvider(drone)
    tracker = HandTracker(hands=1)
    drone = frame_provider.drone
    drone.takeoff()

    while True:
        success, img = frame_provider.get_frame()

        img = cv2.flip(img, 1)
        hands = tracker.find_hands(img)

        if len(hands) == 1:
            hand = hands[0]
            gest = get_gesture(hand)
            if gest:
                gest.do_command(drone)
            tracker.draw_shape_box(img, hand)

        img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        cv2.imshow("img", img_bgr)
        cv2.waitKey(1)


def get_gesture(hand):
    for gest in gestures:
        if gest.is_gesture(hand):
            return gest


if __name__ == "__main__":
    main()
