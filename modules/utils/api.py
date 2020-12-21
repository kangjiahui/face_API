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
    :return: None, results will be written into database.
    """
    try:
        # _json = json.loads(_json)
        _image_base64 = input_dict.pop("user_image")
        face.face_register(_image_base64, input_dict)
        result_json = json.dumps({"result": 0, "message": "SUCCESS"})
    except Exception as e:
        print(e)
        msg = str(e)
        result_json = json.dumps({"result": -1, "message": msg})
    return result_json


def face_delete(user_id):
    """
    Delete an exact face_info by user_id
    :param user_id: string e.x. "10098440"
    :return: None, the face_info will be deleted from database.
    """
    try:
        face.face_delete(user_id)
        result_json = json.dumps({"result": 0, "message": "SUCCESS"})
    except Exception as e:
        print(e)
        msg = str(e)
        result_json = json.dumps({"result": -1, "message": msg})
    return result_json


def face_update(input_dict):
    """
    Update exist face_info.
    :param input_dict: e.x. {"user_id": "10098440", "group_id": "staff", "user_info": "康佳慧", "user_image": "……"}
    :return: None, results will be written into data_path.
    """
    try:
        _image_base64 = input_dict.pop("user_image")
        face.face_update(_image_base64, input_dict)
        result_json = json.dumps({"result": 0, "message": "SUCCESS"})
    except Exception as e:
        print(e)
        msg = str(e)
        result_json = json.dumps({"result": -1, "message": msg})
    return result_json


def face_get_info(page_num=1, max_rows=100):
    """
    Fetch face_info page by page. You can only fetch one page at once.
    :param page_num: int, page index
    :param max_rows: int, how many registered faces in one page
    :return: dict, e.x. {"result": 0, "message": "SUCCESS",
                        "user_data": [{"userID": "10098440", "userGroup": "staff", "userName": "康佳慧",
                                        "latest_modify_time": "2020-12-15 15:15:41", "userIMG": base64_image}, ]}
    """
    try:
        result = face.face_get_info(page_num, max_rows)
        result_json = json.dumps({"result": 0, "message": "SUCCESS", "user_data": result}, ensure_ascii=False)
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
    :return:dict, in format of
            {"result": 0, "message": "SUCCESS", "image": encoded_base64_img,
            "faces":[{"box": bbox, "name": name, "distance": distance}, ]}
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
    """
    Initial a new database. Only execute once before use.
    :return: None. Database and table will be established.
    """
    try:
        face.new_database()
        result_json = json.dumps({"result": 0, "message": "SUCCESS"})
    except Exception as e:
        print(e)
        msg = str(e)
        result_json = json.dumps({"result": -1, "message": msg})
    return result_json

