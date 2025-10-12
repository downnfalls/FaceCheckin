import os

import numpy as np
import face_recognition
import cv2

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
    np.save(f"face_vectors/{name}.npy", encoded)

# load face_vectors
face_vectors = []
face_names = []
for file in os.listdir('face_vectors'):
    face_vectors.append(np.load(f"face_vectors/{file}"))
    face_names.append(os.path.splitext(file)[0])

webCam = cv2.VideoCapture(0)
while True:
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
            name = face_names[min_face_distance_index].upper()
            print(name)
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