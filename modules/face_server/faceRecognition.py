# -*- coding: utf-8 -*-
"""
   File Name：     faceRecognition.py
   Description :  wrapping code of face recognition into a class, instantiation occurs in modules/face_server/utils/api.py
   Author :       KangJiaHui
   date：         2020/11/26
"""

import dlib
import cv2
import numpy as np
import pymysql
import os
import urllib.request
from config import data_path
from modules.utils.utils import image_to_base64, base64_to_image
from PIL import Image, ImageDraw, ImageFont


# conn = pymysql.connect('localhost', user="root", passwd="6", db="users")


def calculate_distance(vector1, vector2):
    """
    Calculates Euclidean distance between two vectors.
    :param vector1:vector presents a face feature
    :param vector2:vector presents a face feature
    :return:disance:the Euclidean distance between vector1 and vector2.
    """
    temp = vector1 - vector2
    distance = np.linalg.norm(temp)
    return distance


def download_from_url(filepath, save_dir):
    """
    download file from URL
    :param filepath: str, URL
    :param save_dir: str, save path without filename
    :return: None
    """
    print('\nDownloading file from {}'.format(filepath))
    filename = filepath.split('/')[-1]
    save_path = os.path.join(save_dir, filename)
    urllib.request.urlretrieve(filepath, save_path)
    print('\nSuccessfully downloaded to {}'.format(save_path))


def cv2_img_add_text(img, text, left, top, text_color=(255, 255, 0), text_size=30):
    if isinstance(img, np.ndarray):  # 判断是否OpenCV图片类型
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img)
    font_text = ImageFont.truetype(
        "fonts/simsun.ttc", text_size, encoding="utf-8")
    draw.text((left, top - 30), text, text_color, font=font_text)
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)


class FaceRecognition(object):
    def __init__(self):
        if not os.path.exists('register_img'):
            os.makedirs('register_img')
        self.predictor_path = os.path.join(os.getcwd(), 'modules/face_server/params',
                                           'shape_predictor_68_face_landmarks.dat')
        self.face_rec_model_path = os.path.join(os.getcwd(), 'modules/face_server/params',
                                                'dlib_face_recognition_resnet_model_v1.dat')
        if not os.path.exists('modules/face_server/params'):
            os.makedirs('modules/face_server/params')
        if not os.path.exists(self.predictor_path):
            download_from_url("http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2",
                              os.path.join(os.getcwd(), 'modules/face_server/params'))
            os.system('bzip2 -d modules/face_server/params/shape_predictor_68_face_landmarks.dat.bz2')
        if not os.path.exists(self.face_rec_model_path):
            download_from_url("http://dlib.net/files/dlib_face_recognition_resnet_model_v1.dat.bz2",
                              os.path.join(os.getcwd(), 'modules/face_server/params'))
            os.system('bzip2 -d modules/face_server/params/dlib_face_recognition_resnet_model_v1.dat.bz2')
        self.detector = dlib.get_frontal_face_detector()
        self.sp = dlib.shape_predictor(self.predictor_path)
        self.facerec = dlib.face_recognition_model_v1(self.face_rec_model_path)
        self.conn = pymysql.connect('localhost', user="root", passwd="6")
        self.cursor = self.conn.cursor()

    def new_database(self):
        # 创建pythonBD数据库
        self.cursor.execute('drop DATABASE if EXISTS face_rec;')
        self.cursor.execute('CREATE DATABASE face_rec;')
        self.cursor.execute('use face_rec;')
        self.cursor.execute('drop table if EXISTS users;')
        print('========Database "face_rec" created!========')
        sql = """CREATE TABLE users(
        user_id VARCHAR(20) not null PRIMARY KEY,
        group_id VARCHAR(100),
        user_info VARCHAR(100) not null,
        face_feature blob not null,
        image_path VARCHAR(100) not null,
        latest_modify_time datetime
        );"""
        self.cursor.execute(sql)
        print('========Table "users" created!========')

    def face_register(self, _image_base64, _info):
        """
        Registers only one picture.
        :param _image_base64: image encoded in base64
        :param _info: a diction E.X.:{"user_id": "10098440", "group_id": "staff", "user_info": "康佳慧"}
        :return: None, results will be written into mysql database
        """
        self.cursor.execute('use face_rec;')
        image = base64_to_image(_image_base64)
        user_id = _info["user_id"]
        group_id = _info["group_id"]
        user_info = _info["user_info"]
        image_path = os.path.join(os.getcwd(), 'register_img', user_id + ".jpg")
        cv2.imwrite(image_path, image)
        # get the face's feature
        faces = self.detector(image, 1)
        if len(faces) != 1:
            print("There must be one and only one face in the image!")
            return 0
        shape = self.sp(image, faces[0])
        face_chip = dlib.get_face_chip(image, shape)
        face_descriptor = np.array(self.facerec.compute_face_descriptor(face_chip)).tostring()

        statement = """INSERT INTO users (user_id, group_id, user_info, face_feature, image_path, latest_modify_time) 
                    VALUES (%s, %s, %s, %s, %s, NOW());"""
        self.cursor.execute(statement, (user_id, group_id, user_info, face_descriptor, image_path))
        self.conn.commit()

    def face_delete(self, user_id):
        """
        Delete an exact face info by user_id.
        :param user_id: user_id of the face to be deleted
        :return: none, face info will be deleted in mysql database
        """
        self.cursor.execute('use face_rec;')
        statement = """delete from users where user_id=%s;"""
        self.cursor.execute(statement, user_id)
        self.conn.commit()

    def face_update(self, _image_base64, _info):
        """
        Reregisters only one picture.
        :param _image_base64: image encoded in base64
        :param _info: a diction E.X.:{"user_id": "10098440", "group_id": "staff", "user_info": "康佳慧"}
        :return: None, results will be written into mysql database
        """
        self.cursor.execute('use face_rec;')
        image = base64_to_image(_image_base64)
        user_id = _info["user_id"]
        group_id = _info["group_id"]
        user_info = _info["user_info"]
        image_path = os.path.join(os.getcwd(), 'register_img', user_id + ".jpg")
        cv2.imwrite(image_path, image)
        # get the face's feature
        faces = self.detector(image, 1)
        if len(faces) != 1:
            print("There must be one and only one face in the image!")
            return 0
        shape = self.sp(image, faces[0])
        face_chip = dlib.get_face_chip(image, shape)
        face_descriptor = np.array(self.facerec.compute_face_descriptor(face_chip)).tostring()
        statement = """update users set group_id=%s, user_info=%s, face_feature=%s, image_path=%s, 
        latest_modify_time=NOW() where user_id=%s;"""
        self.cursor.execute(statement, (group_id, user_info, face_descriptor, image_path, user_id))
        self.conn.commit()

    def face_get_info(self, page_num, max_rows):
        self.cursor.execute('use face_rec;')
        page_start = (page_num - 1) * max_rows
        statement = """SELECT user_id, group_id, user_info, image_path, latest_modify_time from users limit %s, %s;"""
        self.cursor.execute(statement, (page_start, max_rows))
        user_data = self.cursor.fetchall()
        result = []
        for user_id, group_id, user_info, image_path, latest_modify_time in user_data:
            result.append({"userID": user_id, "userGroup": group_id, "userName": user_info,
                           "latest_modify_time": str(latest_modify_time),
                           "userIMG": image_to_base64(cv2.imread(image_path))})
        return result

    def search_identity(self, image=None, path=None, thresh=0.4):
        """
        Serch all faces in one image in the register of n faces' features.
        :param image: numpy.ndarray
        :param path: str, indicates an image
        :param thresh: distance between face and matched face should be smaller than thresh
        :return:list[dict], in format of [{"box": bbox, "name": name, "distance": distance}, ]
        """
        self.cursor.execute('use face_rec;')
        if path:
            image = cv2.imread(path)  # if path and image coexist, then path will cover image
        faces = self.detector(image, 1)
        result = []
        for face in faces:
            bbox = [int(face.left()), int(face.top()), int(face.right()), int(face.bottom())]
            shape = self.sp(image, face)
            face_chip = dlib.get_face_chip(image, shape)
            face_descriptor = np.array(self.facerec.compute_face_descriptor(face_chip))
            # print(face_descriptor)
            distance = 1
            matched_id = ""
            self.cursor.execute("SELECT user_id, face_feature from users;")
            users_in_sql = self.cursor.fetchall()
            for user_id, face_feature in users_in_sql:
                face_feature = np.fromstring(face_feature)
                dist_tmp = calculate_distance(face_descriptor, face_feature)
                if dist_tmp < distance:
                    distance = dist_tmp
                    matched_id = user_id
            if distance < thresh:
                statement = """SELECT user_id, group_id, user_info from users where user_id=%s;"""
                self.cursor.execute(statement, matched_id)
                user_data = self.cursor.fetchall()
                for user_id, group_id, user_info in user_data:
                    result.append({"user_id": user_id, "group_id": group_id, "user_info": user_info,
                                   "box": bbox, "distance": distance})
                    cv2.rectangle(image, (int(face.left()), int(face.top())), (int(face.right()), int(face.bottom())),
                                  (0, 255, 255), 2)
                    image = cv2_img_add_text(image, user_info, int(face.left()), int(face.top()))
        encoded_img = image_to_base64(image)
        return result, encoded_img

    def release(self):
        self.cursor.close()  # 先关闭游标
        self.conn.close()  # 再关闭数据库连接
