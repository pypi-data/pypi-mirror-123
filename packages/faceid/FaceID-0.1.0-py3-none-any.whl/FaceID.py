import os
import cv2
from face_recognition import load_image_file, face_encodings, face_distance
from os import listdir as ld, getcwd as ls, system as cmd


def camera(name):
    cap = cv2.VideoCapture(0)

    for i in range(30):
        cap.read()

    ret, frame = cap.read()

    cv2.imwrite(name, frame)
    cap.release()

    with open(name, "rb") as img:
        pass


class FaceID:
    def __init__(self):
        if os.path.exists("Face") == False:
            cmd("mkdir Face")

            camera("/Face/FaceID.jpg")
        self.names = {}
        for name in [x for x in ld() if not ("." in x)]:
            self.names.update({f"{name}": []})

    def load(self):
        for name in self.names:
            for photo in ld(f"{ls()}/{name}"):
                self.names[name].append(
                    face_encodings(load_image_file(f"{ls()}\\{name}\\{photo}"))[0]
                )

    def search(self):
        camera("/person.jpg")

        try:
            searched_photo = face_encodings(load_image_file(f"/person.jpg"))[0]
        except:
            print("Error!")

        answer = "unknow"
        max_coef = 0

        for name in self.names:
            for photo in self.names[name]:
                coef = 1 - face_distance([searched_photo], photo)[0]
                print(f"coef: {coef}")

                if coef > max_coef:
                    answer = name
                    max_coef = coef
        if answer == "Face":
            print("Это Вы!")
        else:
            print("Это не Вы!")


if __name__ == "__main__":
    k = FaceID()
    k.load()
    k.search()
