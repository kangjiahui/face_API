# -*- coding: utf-8 -*-
"""
   File Name：     faceRecognition.py
   Description :  Instantiate FaceRecognition from faceRecognition.py. Give a clear API for user.
   Author :       KangJiaHui
   date：         2020/11/26
"""

import json
from modules.face_server.faceRecognition import FaceRecognition

face = FaceRecognition()
print("FaceRcognition created!")


def face_register(input_dict):
    """
    Registers only one picture.
    :param input_dict: e.x. {"user_id": "10098440", "group_id": "staff", "user_info": "康佳慧", "user_image": "……"}
    :return: None, results will be written into data_path.
    """
    try:
        # _json = json.loads(_json)
        _image_base64 = input_dict.pop("user_image")
        print(type(_image_base64))
        face.face_register(_image_base64, input_dict)
        result_json = json.dumps({"result": 0, "message": "SUCCESS"})
    except Exception as e:
        print(e)
        msg = str(e)
        result_json = json.dumps({"result": -1, "message": msg})
    return result_json


def face_delete(user_id):
    try:
        face.face_delete(user_id)
        result_json = json.dumps({"result": 0, "message": "SUCCESS"})
    except Exception as e:
        print(e)
        msg = str(e)
        result_json = json.dumps({"result": -1, "message": msg})
    return result_json


def search_identity(image=None, path=None, thresh=0.6):
    """
    Serch all faces in one image in the register of n faces' features.
    If path and image coexist, then path will cover image.
    :param image: numpy.ndarray
    :param path: str, indicates an image
    :param thresh: distance between face and matched face should be smaller than thresh
    :return:list[dict], in format of [{"box": bbox, "name": name, "distance": distance}, ]
    """
    try:
        if path:
            faces_info, encoded_img = face.search_identity(path=path, thresh=thresh)
        else:
            faces_info, encoded_img = face.search_identity(image=image, thresh=thresh)
        result_json = json.dumps({"result": 0, "message": "SUCCESS", "image": encoded_img, "faces": faces_info},
                                 ensure_ascii=False)
    except Exception as e:
        print(e)
        msg = str(e)
        result_json = json.dumps({"result": -1, "message": msg})
    return result_json


def new_database():
    try:
        face.new_database()
        result_json = json.dumps({"result": 0, "message": "SUCCESS"})
    except Exception as e:
        print(e)
        msg = str(e)
        result_json = json.dumps({"result": -1, "message": msg})
    return result_json

