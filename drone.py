from djitellopy import tello
import cv2
from PIL import Image

drone = tello.Tello()
drone.connect()

drone.streamon()

while True:
    img = drone.get_frame_read().frame
    #img = Image.fromarray(arr.T, 'RGB')
    #img.save('out.png')
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imshow("img", img)
    cv2.waitKey(1)
