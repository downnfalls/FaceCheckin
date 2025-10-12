import os

import time
import numpy as np
import face_recognition
import cv2

mark_attendance_delay = 5
save_encoded_delay = 10

face_vectors = []
face_names = []

def saveEncoded(name, timestamp, encoded):
    np.save(f"face_vectors/{name}_{timestamp}.npy", encoded)
    face_names.append(f"{name}_{timestamp}")
    face_vectors.append(encoded)

def markAttendance(name, timestamp):
    with open('attendances.csv', 'r+', encoding='utf-8') as f:
        my_data_list = f.readlines()
        name_list = []
        for line in my_data_list:
            entry = line.strip().split(',')  # strip() กัน \n
            name_list.append(entry[0])
        if name not in name_list:
            now = time.localtime(timestamp)
            time_string = time.strftime("%d/%m/%Y %H:%M:%S", now)  # strftime representing date and time using date
            f.writelines(f'\n{name}, {time_string}\n')
        print(my_data_list)

input_face = []
for file in os.listdir('face_input'):
    raw_image = cv2.imread(f'face_input/{file}')

    converted_image = cv2.cvtColor(raw_image, cv2.COLOR_BGR2RGB)
    input_face.append({"name": os.path.splitext(file)[0], "image": converted_image})


# convert input image to face vector and keep it to face_vector dir
for face in input_face:
    name = face["name"]
    image = face["image"]

    encoded = face_recognition.face_encodings(image)[0]

    # create encoded face file
    np.save(f"face_vectors/{name}_0000000000.npy", encoded)

# load face_vectors
for file in os.listdir('face_vectors'):
    face_vectors.append(np.load(f"face_vectors/{file}"))
    face_names.append(os.path.splitext(file)[0])

mark_attendance_map = {}
save_encoded_map = {}
webCam = cv2.VideoCapture(0)
while True:

    for key, value in mark_attendance_map.items():
        if int(time.time()) - value > mark_attendance_delay:
            mark_attendance_map.pop(key)

    for key, value in save_encoded_map.items():
        if int(time.time()) - value > save_encoded_delay:
            save_encoded_map.pop(key)

    success, img = webCam.read()
    resized_frame = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
    converted_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)

    locations = face_recognition.face_locations(converted_frame)
    encoded_faces = face_recognition.face_encodings(converted_frame, locations)

    for location, encoded_face in zip(locations, encoded_faces):
        matches = face_recognition.compare_faces(face_vectors, encoded_face)
        face_distances = face_recognition.face_distance(face_vectors, encoded_face)

        min_face_distance_index = np.argmin(face_distances)

        if matches[min_face_distance_index]:
            name = face_names[min_face_distance_index].split("_")[0].upper()

            # check if this person is out of frame over delay second
            if name not in mark_attendance_map:
                markAttendance(name, int(time.time()))

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