import cv2
from modules.utils.api import face_register_batch, search_identity, face_register
from modules.utils.utils import base64_to_image
import json


def show_in_video():
    video_capture = cv2.VideoCapture(0)
    while True:
        ret, img = video_capture.read()  # frame shape 640*480*3
        if not ret:
            break
        result = search_identity(image=img)
        result = json.loads(result)
        image = base64_to_image(result["image"])

        cv2.namedWindow("face_recognition", 0)
        cv2.resizeWindow('face_recognition', 1024, 768)
        cv2.imshow('face_recognition', image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()


if __name__ == '__main__':
    # face_register_batch('register_img')
    show_in_video()
    # face_register("register_img/kang.jpg", ["10098440", "staff", "康佳慧_女_算法工程师"])
    # result = search_identity(path='test.jpg')
    # print(result)

