import os

import time
import numpy as np
import face_recognition
import cv2
import shutil

import tkinter as tk
from tkinter import messagebox

face_judgement_threshold = 0.30
mark_attendance_delay = 10 # seconds
save_encoded_delay = 10
data_keep_per_person = 5

face_vectors = []
face_names = []

def saveEncoded(name, timestamp, encoded):

    files = os.listdir(f'face_vectors/{name}')
    if len(files) > data_keep_per_person:
        image_times = []
        for file in files:
            times = os.path.splitext(file)[0].split('_')[1]
            image_times.append(times)

        min_time = min(image_times)
        os.remove(f"face_vectors/{name}/{name}_{min_time}.npy")

        index = face_names.index(f"{name}_{min_time}")
        face_names.pop(index)
        face_vectors.pop(index)

    folder = f"face_vectors/{name}"
    os.makedirs(folder, exist_ok=True)
    np.save(f"{folder}/{name}_{timestamp}.npy", encoded)
    face_names.append(f"{name}_{timestamp}")
    face_vectors.append(encoded)

def markAttendance(name, timestamp):

    filepath = 'attendances.csv' # ถ้ายังไม่มีชื่อใน attendance = write new one ( name, time )
    if not os.path.exists(filepath):
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines("Name, Time\n")

    with open('attendances.csv', 'r+', encoding='utf-8') as f:
        my_data_list = f.readlines()
        name_list = []
        for line in my_data_list:
            entry = line.strip().split(',')  # strip() กัน \n
            name_list.append(entry[0])
        # if name not in name_list:
        now = time.localtime(timestamp)
        time_string = time.strftime("%d/%m/%Y %H:%M:%S", now)  # strftime representing date and time using date
        f.writelines(f'{name}, {time_string}\n')
        print(my_data_list)

    

input_face = []
for file in os.listdir('face_input'):
    raw_image = cv2.imread(f'face_input/{file}')

    resized_frame = cv2.resize(raw_image, (0, 0), fx=0.25, fy=0.25)
    converted_image = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)

    input_face.append({"name": os.path.splitext(file)[0], "image": converted_image})

# convert input image to face vector and keep it to face_vector dir
for face in input_face:
    name = face["name"]
    image = face["image"]

    encoded = face_recognition.face_encodings(image)[0]

    # create encoded face file
    folder = f"face_vectors/{name.upper()}"
    os.makedirs(folder, exist_ok=True)
    np.save(f"{folder}/{name.upper()}_9999999999.npy", encoded)

for file in os.listdir('face_input_vectors'):
    if os.path.isfile(f'face_input_vectors/{file}'):

        name = os.path.splitext(file)[0]

        folder = f"face_vectors/{name.upper()}"
        os.makedirs(f"{folder}", exist_ok=True)
        shutil.copy(f"face_input_vectors/{name}.npy", f"{folder}/{name.upper()}_9999999999.npy")


# load face_vectors
for directory in os.listdir('face_vectors'):
    if os.path.isdir(f"face_vectors/{directory}"):
        for file in os.listdir(f"face_vectors/{directory}"):
            face_vectors.append(np.load(f"face_vectors/{directory}/{file}"))
            face_names.append(os.path.splitext(file)[0])

mark_attendance_map = {}
save_encoded_map = {}
webCam = cv2.VideoCapture(0)
while True:

    mark_attendance_map = {
        key: value
        for key, value in mark_attendance_map.items()
        if int(time.time()) - value <= mark_attendance_delay
    }

    save_encoded_map = {
        key: value
        for key, value in save_encoded_map.items()
        if int(time.time()) - value <= save_encoded_delay
    }

    success, img = webCam.read()
    resized_frame = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
    converted_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)

    locations = face_recognition.face_locations(converted_frame)
    encoded_faces = face_recognition.face_encodings(converted_frame, locations)

    for location, encoded_face in zip(locations, encoded_faces):
        matches = face_recognition.compare_faces(face_vectors, encoded_face)
        face_distances = face_recognition.face_distance(face_vectors, encoded_face)

        min_face_distance_index = np.argmin(face_distances)

        # check threshold value
        if face_distances[min_face_distance_index] <= face_judgement_threshold:

            if matches[min_face_distance_index]:
                name = face_names[min_face_distance_index].split("_")[0].upper()

                # check if this person is out of frame over delay second
                if name not in mark_attendance_map:
                    markAttendance(name, int(time.time()))
                    time.sleep(5)
                    root = tk.Tk()
                    root.withdraw()
                    messagebox.showinfo("Check-In Complete", f"{name} checked in successfully.")
                    root.destroy()

                if name not in save_encoded_map:
                    saveEncoded(name, int(time.time()), encoded_face)

                mark_attendance_map[name] = int(time.time())
                save_encoded_map[name] = int(time.time())

                # print(faceLoc)(top, right, bottom, left)
                y1, x2, y2, x1 = location
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4  # rescale พิกัดกลับมาไซส์เดิม
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0),
                              3)  # cv2.rectangle(image, pt1บนซ้าย, pt2ล่างขวา, color, thickness)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 2)

    cv2.imshow('Webcam', img)
    cv2.waitKey(1)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # press q to cancel
        break


# create GUI window to choose sign up or sign in
