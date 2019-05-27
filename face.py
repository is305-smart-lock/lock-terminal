import face_recognition
import picamera
import numpy as np
import requests, json
import os
import utils

def poll():
    camera = picamera.PiCamera()
    camera.resolution = (320, 240)
    output = np.empty((240, 320, 3), dtype=np.uint8)

    data = json.loads(requests.get('https://lock.dy.tongqu.me/lock-terminal/faces?hid=' + os.environ.get('HID')).content)
    known_face_encodings = [x["landmarks"] for x in data]
    known_face_names = [x["user"] for x in data]

    while True:
        # print("Capturing image.")
        # 以numpy array的数据结构从picamera摄像头中获取一帧图片
        camera.capture(output, format="rgb")

        face_locations = face_recognition.face_locations(output)
        # print("Found {} faces in image.".format(len(face_locations)))
        face_encodings = face_recognition.face_encodings(output, face_locations)

        # 将每一个人脸与已知样本图片比对
        for face_encoding in face_encodings:

            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = None

            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            if name != None:
                utils.welcome(name)
