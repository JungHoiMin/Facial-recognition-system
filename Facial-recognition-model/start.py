import cv2
import numpy as np
from os import listdir
from os.path import isdir, isfile, join
import RPi.GPIO as gpio
import time
import paho.mqtt.client as mqtt

face_classifier = cv2.CascadeClassifier('../openCV/haarcascade_frontalface_default.xml')


def trains():
    model_path = 'models/'
    model_files = [f for f in listdir(model_path) if isfile(join(model_path, f))]
    models = {}
    for file in model_files:
        model_name = file[6:-4]
        model = None
        model = cv2.face.LBPHFaceRecognizer_create()
        model.read(model_path + file)
        models[model_name] = model

    return models


def face_detector(img, size=0.5):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)
    if faces is ():
        return img, []
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), 2)
        roi = img[y:y + h, x:x + w]
        roi = cv2.resize(roi, (200, 200))
    return img, roi


def run(models):
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        image, face = face_detector(frame)
        name = ""
        score = 0
        try:
            min_score = 999
            min_score_name = ""

            face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

            for key, model in models.items():
                result = model.predict(face)
                if min_score > result[1]:
                    min_score = result[1]
                    min_score_name = key

            if min_score < 500:
                confidence = int(100 * (1 - (min_score) / 300))
                display_string = str(confidence) + '% Confidence it is ' + min_score_name
            cv2.putText(image, display_string, (100, 120), cv2.FONT_HERSHEY_COMPLEX, 1, (250, 120, 255), 2)

            if confidence > 75:
                cv2.putText(image, "Unlocked : " + min_score_name, (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0),
                            2)
                cv2.imshow('Face Cropper', image)
                score = confidence
                name = min_score_name
            else:
                cv2.putText(image, "Locked", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
                cv2.imshow('Face Cropper', image)
                score = confidence
                name = "Outsider"
        except:
            cv2.putText(image, "Face Not Found", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
            cv2.imshow('Face Cropper', image)
            pass
        if score > 20:
            sendMQTT(name)
            break
        if (cv2.waitKey(1) & 0xff) == 27:
            break
    cap.release()
    cv2.destroyAllWindows()

def distanceCheck():
    gpio.setwarnings(False)
    gpio.setmode(gpio.BCM)
    trig = 20
    echo = 21
    print('start')
    gpio.setup(trig, gpio.OUT)
    gpio.setup(echo, gpio.IN)

    while True:
        gpio.output(trig, False)
        time.sleep(0.5)
        gpio.output(trig, True)
        time.sleep(0.00001)
        gpio.output(trig, False)

        while gpio.input(echo) == 0:
            pulse_start = time.time()

        while gpio.input(echo) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17000
        distance = round(distance, 2)
        print(distance)
        if distance < 30.00:
            print("detected something")
            break


def sendMQTT(name):
    msg = name+" is comming"
    mq = mqtt.Client("JUNG-pub")
    mq.connect("broker.mqtt-dashboard.com", 1883)
    mq.publish("jhm", msg)
    mq.loop(2)

if __name__ == "__main__":
    models = trains()
    while True:
        distanceCheck()
        run(models)
        time.sleep(5)


