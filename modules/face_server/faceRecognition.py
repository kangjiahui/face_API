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
import csv
import os
import urllib.request
from config import data_path

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


class FaceRecognition(object):
    def __init__(self):
        self.predictor_path = os.path.join(os.getcwd(), 'modules/face_server/params', 'shape_predictor_68_face_landmarks.dat')
        self.face_rec_model_path = os.path.join(os.getcwd(), 'modules/face_server/params', 'dlib_face_recognition_resnet_model_v1.dat')
        if not os.path.exists('modules/face_server/params'):
            os.makedirs('modules/face_server/params')
        if not os.path.exists(self.predictor_path):
            download_from_url("http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2", os.path.join(os.getcwd(), 'modules/face_server/params'))
            os.system('bzip2 -d modules/face_server/params/shape_predictor_68_face_landmarks.dat.bz2')
        if not os.path.exists(self.face_rec_model_path):
            download_from_url("http://dlib.net/files/dlib_face_recognition_resnet_model_v1.dat.bz2", os.path.join(os.getcwd(), 'modules/face_server/params'))
            os.system('bzip2 -d modules/face_server/params/dlib_face_recognition_resnet_model_v1.dat.bz2')
        self.detector = dlib.get_frontal_face_detector()
        self.sp = dlib.shape_predictor(self.predictor_path)
        self.facerec = dlib.face_recognition_model_v1(self.face_rec_model_path)
        self.data_path = os.path.join(data_path, "data.csv")
        if not os.path.exists(data_path):
            os.makedirs(data_path)
        self.register = {}

    def register_load(self):
        """
        When database changed, this function should be called to reload newest register.
        :return: None
        """
        self.register = {}
        if not os.path.exists(self.data_path):
            file = open(self.data_path, 'w')
            file.close()
        with open(self.data_path, "r") as data:
            reader = csv.reader(data)
            for line in reader:
                if line:
                    print(line)
                    feature = np.fromstring(eval(line[1]))
                    self.register[line[0]] = np.array(feature)

    def face_register(self, _image_path, _name):
        """
        Registers only one picture.
        :param _image_path: refers to a picture path which contains one and only one face
        :param _name: the name for the registering face
        :return: None, results will be written into data_path.
        """
        image = cv2.imread(_image_path)
        if _name not in self.register.keys():
            faces = self.detector(image, 1)
            if len(faces) != 1:
                print("There must be one and only one face in the image!")
                return 0
            shape = self.sp(image, faces[0])
            face_chip = dlib.get_face_chip(image, shape)
            face_descriptor = np.array(self.facerec.compute_face_descriptor(face_chip)).tostring()
            with open(self.data_path, "a+") as _data:
                writer = csv.writer(_data)
                writer.writerow([_name, face_descriptor])
            self.register_load()

    def face_register_batch(self, _image_path):
        """
        All pictures in the path could be register at once. Name refers to filename.
        :param _image_path: str, contains one or more pictures, register name will be the picture's filename
        :return: None
        """
        _register = {}
        _image_list = []
        for root, dirs, files in os.walk(_image_path):
            for file in files:
                if os.path.splitext(file)[1] == '.jpg':
                    _image_list.append(os.path.join(root, file))
        print(_image_list)

        for path in _image_list:
            image = cv2.imread(path)
            name = os.path.basename(path).split('.')[0]
            if name not in self.register.keys():
                faces = self.detector(image, 1)
                if len(faces) != 1:
                    print("There must be one and only one face in the image{}!".format(path))
                    continue
                shape = self.sp(image, faces[0])
                face_chip = dlib.get_face_chip(image, shape)
                face_descriptor = np.array(self.facerec.compute_face_descriptor(face_chip)).tostring()
                _register[name] = face_descriptor
        if _register:
            with open(self.data_path, "a+") as _data:
                writer = csv.writer(_data)
                for key in _register:
                    writer.writerow([key, _register[key]])
            self.register_load()

    def search_identity(self, image=None, path=None, thresh=0.4):
        """
        Serch all faces in one image in the register of n faces' features.
        :param image: numpy.ndarray
        :param path: str, indicates an image
        :param thresh: distance between face and matched face should be smaller than thresh
        :return:list[dict], in format of [{"box": bbox, "name": name, "distance": distance}, ]
        """
        if path:
            image = cv2.imread(path)  # if path and image coexist, then path will cover image
        faces = self.detector(image, 1)
        result = []
        for face in faces:
            bbox = [int(face.left()), int(face.top()), int(face.right()), int(face.bottom())]
            shape = self.sp(image, face)
            face_chip = dlib.get_face_chip(image, shape)
            face_descriptor = np.array(self.facerec.compute_face_descriptor(face_chip))
            distance = 1
            name = ""
            for key in self.register:
                dist_tmp = calculate_distance(face_descriptor, self.register[key])
                if dist_tmp < distance:
                    distance = dist_tmp
                    name = key
            if distance < thresh:
                result.append({"box": bbox, "name": name, "distance": distance})
                cv2.rectangle(image, (int(face.left()), int(face.top())), (int(face.right()), int(face.bottom())),
                              (255, 255, 255), 2)
                cv2.putText(image, name, (int(face.left()), int(face.top())), 0, 1, (255, 255, 255), 2)
        return result
