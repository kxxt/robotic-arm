import cv2
import numpy as npy


def get(img):
    return npy.mean(img)


if __name__ == '__main__':
    video = cv2.VideoCapture(0)
    while True:
        success, image = video.read()
        if not success:
            print("Failed!")
            continue
        print("Fuck")
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        frame = cv2.putText(image, str(get(gray)), (10, 30), cv2.FONT_HERSHEY_DUPLEX, 1.0, (0, 255, 0), 2)
        cv2.imshow("Darkness", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
