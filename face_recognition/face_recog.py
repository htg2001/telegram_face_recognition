import face_recognition
import cv2
import os
import datetime
import pickle

def capture_image(url):
    cam = cv2.VideoCapture(url)
    frame = cam.read()
    currennt_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M%S %p")
    cv2.putText(frame, currennt_time,(10,30), cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,255,0),2)
    cam.release()
    return frame

def compare_face(file_encoded_face, image_input):
    with open(file_encoded_face, "rb") as f:
        encoding = pickle.load(f)
    image_input = face_recognition.load_image_file(image_input)
    