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
face.register_load()


def face_register(_image_path, _name):
    """
    Registers only one picture.
    :param _image_path: refers to a picture path which contains one and only one face
    :param _name: the name for the registering face
    :return: None, results will be written into data_path.
    """
    try:
        face.face_register(_image_path, _name)
        result_json = json.dumps({"result": 0, "message": "SUCCESS"})
    except Exception as e:
        print(e)
        msg = str(e)
        result_json = json.dumps({"result": -1, "message": msg})
    return result_json


def face_register_batch(_image_path):
    """
     All pictures in the path could be register at once. Name refers to filename.
    :param _image_path: str, contains one or more pictures, register name will be the picture's filename
    :return: None
    """
    try:
        face.face_register_batch(_image_path)
        result_json = json.dumps({"result": 0, "message": "SUCCESS"})
    except Exception as e:
        print(e)
        msg = str(e)
        result_json = json.dumps({"result": -1, "message": msg})
    return result_json


def search_identity(image=None, path=None, thresh=0.4):
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
            faces_info = face.search_identity(path=path, thresh=thresh)
        else:
            faces_info = face.search_identity(image=image, thresh=thresh)
        result_json = json.dumps({"result": 0, "message": "SUCCESS", "faces": faces_info})
    except Exception as e:
        print(e)
        msg = str(e)
        result_json = json.dumps({"result": -1, "message": msg})
    return result_json
