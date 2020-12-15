import cv2
from modules.utils.api import *
from modules.utils.utils import base64_to_image, image_to_base64
import json
from modules.face_server.faceRecognition import FaceRecognition


def video_file_process():
    cap = cv2.VideoCapture("test.mp4")
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter('output.avi', fourcc, 20.0, (width, height))
    while True:
        # get a frame
        ret, img = cap.read()
        if ret:
            # deal with a frame
            result = search_identity(image=img)
            result = json.loads(result)
            image = base64_to_image(result["image"])
            out.write(image)
            cv2.imshow('face_recognition', image)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
        else:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()


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
    # res = face_delete("10098441")
    # print(res)

    # video_file_process()
    # show_in_video()

    # new_database()
    # image = cv2.imread("register_img/t2.jpg")
    # image_64 = image_to_base64(image)
    # face_register({"user_id": "10097508", "group_id": "master", "user_info": "童随兵", "user_image": image_64})
    # face_update({"user_id": "10098441", "group_id": "staff", "user_info": "康佳慧", "user_image": image_64})
    print(face_get_info())
    # result = search_identity(path='test.jpg')
    # print(result)


