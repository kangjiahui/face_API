import base64
import threading
from time import sleep

from flask import Flask, request, jsonify
from modules.utils.api import *
from flask_cors import CORS
from multiprocessing import Process, Queue
import json
import cv2

app = Flask(__name__)
CORS(app, resources=r'/*')
q = Queue(3)
print(f"q.id={id(q)}")


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


# t1 = threading.Thread(target=show_in_video, args=(q,))
# t1.start()


# 人脸识别运行
@app.route('/getImgFlow', methods=["GET"])
def face_recog():
    # global q
    if request.method == 'GET':
        # print("==api=run=== ", id(q), q.qsize())

        result = q.get()
        # print("==api=run11------- ", id(q), q.qsize())
        # print("==api=run===result ", result)
        if result:
            # print(result)
            return result
        else:
            return json.dumps({"result": 1, "message": "failed"})


# 人脸信息注册
@app.route('/uploadInfo', methods=["POST"])
def uploadInfo():
    abd = request
    file = request.files['user_image']
    image_base64 = base64.b64encode(file.read())
    print(type(image_base64))
    # image_base64 = base64.b64encode(file.read())
    # image_base64 = base64.encodebytes(file.read())
    print(image_base64)
    user_id = request.form['user_id']
    group_id = request.form['group_id']
    user_info = request.form['user_info']
    print("data received!")
    input_data = {"user_id": user_id, "group_id": group_id, "user_info": user_info, "user_image": image_base64}
    print(input_data)
    face_register(input_data)
    return '1'


# 人脸更新
@app.route('/updateInfo', methods=["POST"])
def updateInfo():
    file = request.files['user_image']
    image_base64 = base64.b64encode(file.read())
    print(type(image_base64))
    # image_base64 = base64.b64encode(file.read())
    # image_base64 = base64.encodebytes(file.read())
    print(image_base64)
    user_id = request.form['user_id']
    group_id = request.form['group_id']
    user_info = request.form['user_info']
    print("data received!")
    input_data = {"user_id": user_id, "group_id": group_id, "user_info": user_info, "user_image": image_base64}
    print(input_data)
    face_update(input_data)
    return '1'


# 人脸更新
@app.route('/updateInfo2', methods=["POST"])
def updateInfo2():
    # file = request.files['user_image']
    # image_base64 = base64.b64encode(file.read())
    # print(type(image_base64))
    # image_base64 = base64.b64encode(file.read())
    # image_base64 = base64.encodebytes(file.read())
    # print(image_base64)
    user_id = request.form['user_id']
    image_base64 = request.form['user_image']
    group_id = request.form['group_id']
    user_info = request.form['user_info']
    print("data received!")
    input_data = {"user_id": user_id, "group_id": group_id, "user_info": user_info, "user_image": image_base64}
    print(input_data)
    face_update(input_data)
    return '1'


# 人脸删除
@app.route('/deleteInfo', methods=["POST"])
def deleteInfo():
    user_id = request.form['user_id']
    print(f"data received! User_id={user_id}")
    face_delete(user_id)
    return '1'


# 人脸信息获取
@app.route('/getAllInfo', methods=["POST"])
def getAllInfo():
    print("Here get info!===============")
    try:
        position = request.form['position']
        print(f"data received! Position={position}")
        return face_get_info(page_num=position)
    except BaseException:
        return face_get_info()


if __name__ == '__main__':
    deal_video_no = Process(target=show_in_video, args=(q,))
    deal_video_no.start()
    # app.run(host='0.0.0.0', port=8100, debug=True)
    app.run(host='0.0.0.0', port=8100, debug=True, use_reloader=False)
