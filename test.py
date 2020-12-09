import os

import cv2
import dlib
import pymysql

# 打开数据库连接
import numpy as np

conn = pymysql.connect('localhost', user="root", passwd="6")
# 获取游标
cursor = conn.cursor()
# 创建pythonBD数据库
cursor.execute('drop DATABASE if EXISTS face_rec;')
cursor.execute('CREATE DATABASE face_rec;')
cursor.execute('use face_rec;')
cursor.execute('drop table if EXISTS users;')
sql = """CREATE TABLE users(
user_id VARCHAR(20) not null PRIMARY KEY,
group_id VARCHAR(100),
user_info VARCHAR(100) not null,
face_feature blob not null
);"""
cursor.execute(sql)
print('创建pythonBD数据库成功')

predictor_path = os.path.join(os.getcwd(), 'modules/face_server/params',
                              'shape_predictor_68_face_landmarks.dat')
face_rec_model_path = os.path.join(os.getcwd(), 'modules/face_server/params',
                                   'dlib_face_recognition_resnet_model_v1.dat')
detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor(predictor_path)
facerec = dlib.face_recognition_model_v1(face_rec_model_path)

image = cv2.imread("register_img/kang.jpg")
info = {"user_id": "10098440", "group_id": "staff", "user_info": "康佳慧"}
user_id = info["user_id"]
group_id = info["group_id"]
user_info = info["user_info"]
# get the face's feature
faces = detector(image, 1)
if len(faces) != 1:
    print("There must be one and only one face in the image!")
else:
    shape = sp(image, faces[0])
    face_chip = dlib.get_face_chip(image, shape)
    face_descriptor_1 = np.array(facerec.compute_face_descriptor(face_chip))
    face_descriptor = face_descriptor_1.tostring()
    # print(face_descriptor)
    # restore = np.fromstring(face_descriptor)
    # print(restore.shape)
    statement = """INSERT INTO users (user_id, group_id, user_info, face_feature) VALUES (%s, %s, %s, %s);"""
    cursor.execute(statement, (user_id, group_id, user_info, face_descriptor))
    conn.commit()

cursor.execute("SELECT user_id, group_id, user_info, face_feature from users;")
result = cursor.fetchall()
for user_id, group_id, user_info, face_feature in result:
    # 将vector 从blob转换为numpy float16
    # print(face_feature)
    face_descriptor_2 = np.fromstring(face_feature)
    print(face_descriptor_2 - face_descriptor_1)


cursor.close()  # 先关闭游标
conn.close()  # 再关闭数据库连接
