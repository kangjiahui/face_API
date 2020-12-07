import threading
from time import sleep

from flask import Flask, request, jsonify
from modules.utils.api import search_identity
from flask_cors import CORS
from multiprocessing import Process, Queue
import json
import cv2

app = Flask(__name__)
CORS(app, resources=r'/*')
q = Queue(10)
print(f"  q.id={id(q)}")


def show_in_video(q_):
    # print(f"show_in_video  q.id={}")
    print("===show_in_video=== ", id(q_))

    print('into show_in_video')
    # fourcc = cv2.VideoWriter_fourcc(*'XVID')

    # out = cv2.VideoWriter('output.avi', fourcc, 3.0, (640, 480))
    video_capture = cv2.VideoCapture(0)
    while True:
        print('while...put new img into quque')
        print("===run=== ", id(q_), q_.qsize())
        # sleep(1)
        ret, img = video_capture.read()  # frame shape 640*480*3
        if not ret:
            break
        result = search_identity(image=img)
        if q_.full():
            q_.get()
        else:
            # print(f"before put  q.size={q.size()}")
            q_.put(result)
            # print(f"after put  q.size={q.size()}")
        # print(q.get())
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    video_capture.release()


t1 = threading.Thread(target=show_in_video, args=(q,))
t1.start()


# run_thread()

# def run_thread():
#     while True:
#
#         deal_video_no = Process(target=show_in_video, args=(q,))
#         deal_video_no.start()


# 获取记录用户uid的json文件，获取用户uid，输出结果
@app.route('/getImgFlow', methods=["GET"])
def face_recog():
    # global q
    if request.method == 'GET':
        print("==api=run=== ", id(q), q.qsize())

        result = q.get()
        print("==api=run11------- ", id(q), q.qsize())
        print("==api=run===result ", result)
        if result:
            print(result)
            return result
        else:
            return json.dumps({"result": 1, "message": "failed"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8100, debug=True, use_reloader=False)
