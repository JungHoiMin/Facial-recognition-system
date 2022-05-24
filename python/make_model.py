import cv2
import numpy as np
from os import listdir
from os.path import isdir, isfile, join

face_classifier = cv2.CascadeClassifier('../openCV/haarcascade_frontalface_default.xml')


def train(name):
    data_path = 'faces/' + name + '/'
    face_pics = [f for f in listdir(data_path) if isfile(join(data_path, f))]

    Training_Data, Labels = [], []

    for i, files in enumerate(face_pics):
        image_path = data_path + face_pics[i]
        images = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if images is None:
            continue

        Training_Data.append(np.asarray(images, dtype=np.uint8))
        Labels.append(i)
    if len(Labels) == 0:
        print("There is no data to train.")
        return None

    Labels = np.asarray(Labels, dtype=np.int32)
    model = cv2.face.LBPHFaceRecognizer_create()
    model.train(np.asarray(Training_Data), np.asarray(Labels))
    print(name + " : Model Training Complete!!!!!")

    return model


def trains():
    data_path = 'faces/'
    model_dirs = [f for f in listdir(data_path) if isdir(join(data_path, f))]

    for model in model_dirs:
        print('model :' + model)

        result = train(model)
        if result is None:
            continue
        result.write("models/model_"+model+".yml")

if __name__ == "__main__":
    models = trains()
    print('finish train!!!')


