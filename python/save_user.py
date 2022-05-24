import cv2
import numpy as np
from os import makedirs
from os.path import isdir

face_dirs = 'faces/'
if not isdir(face_dirs):
    makedirs(face_dirs)

face_classifier = cv2.CascadeClassifier('../openCV/haarcascade_frontalface_default.xml')

def face_extractor(img):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray,1.3,5)
    if faces is():
        return None

    for(x,y,w,h) in faces:
        cropped_face = img[y:y+h, x:x+w]

    return cropped_face


def take_pictures():
    if not isdir(face_dirs+name):
        makedirs(face_dirs+name)

    cap = cv2.VideoCapture(0)
    count = 0

    while True:
        ret, frame = cap.read()
        if face_extractor(frame) is not None:
            count+=1

            face = cv2.resize(face_extractor(frame),(200,200))
            face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

            file_name_path = face_dirs+'picture' + str(count) + '.jpg'
            cv2.imwrite(file_name_path,face)

            cv2.putText(face,str(count),(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
            cv2.imshow('Face Cropper',face)
        else:
            print("Face not Found. Current count is {0}".format(count))
            pass

        if (cv2.waitKey(1) & 0xff) == 27 or count == 100:
            break

    cap.release()
    cv2.destroyAllWindows()
    print('Colleting Samples Complete!!!')


if __name__=="__main__":
    take_pictures()
