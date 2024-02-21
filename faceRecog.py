# Made with references from Face Recognition with Real Time Database from Murtaza's Workshop Channel on Youtube
# (https://www.youtube.com/watch?v=iBomaK2ARyI)

import pickle
import numpy as np
import cv2
import face_recognition
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from collections import Counter
import time


def recognize_face():
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': "XXX",                   ## Put in the database URL provided by firebase
        'storageBucket': "XXX"                  ## Put in the storage bucket URL provided by firebase
    })
    student_db = db.reference(f'XXX').get()     ## Put in your database name

    # student_db = {'001': {'name': 'Sugondese Dover', 'others': 'blabla'},
    #               '002': {'name': 'Ben Bols', 'others': 'bleble'}}
    ## Or put in your data as a dictionary like the dictionary above

    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    file = open('EncodeFileFinal.p', 'rb')
    encodeListKnown, studentIds = pickle.load(file)
    file.close()

    detected = list()
    target_length = 50
    frame_times = list()

    success, img = cap.read()
    start = time.time()
    while success and cv2.waitKey(1) == -1 and len(detected) < target_length:
        ft_start = time.time()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        faceCurFrame = face_recognition.face_locations(imgS)
        if faceCurFrame:
            encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame, model='large')
            for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                matchIndex = np.argmin(faceDis)
                if matches[matchIndex]:
                    studId = studentIds[matchIndex]
                    name = student_db[str(studId)]['name']
                    detected.append(name)
                    m = 4
                    img = cv2.rectangle(img, (faceLoc[0] * m, faceLoc[1]),
                                        (faceLoc[0] * m + faceLoc[2] * m, faceLoc[1] + faceLoc[3] * m), (255, 0, 0), 2)
                    text = '%s, distance=%.2f' % (name, faceDis[matchIndex])
                    cv2.putText(img, text, (faceLoc[0] * m, faceLoc[1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                (255, 0, 0), 2)
                    cv2.putText(img, f"{round((len(detected) / target_length * 100), 2)}%", (0, 45),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2)
                    ft_stop = time.time()
                    frame_times.append(ft_stop - ft_start)

        cv2.imshow("Webcam", img)
        success, img = cap.read()
    cap.release()
    cv2.destroyAllWindows()
    stop = time.time()

    hist_name = Counter(detected)
    print(f"Loop finished in {stop - start} seconds")
    print(f"Average Detection frame time: {round(np.average(frame_times), 3)} seconds\n")
    print("Name Frequency and Detection Percentage:")
    for i in hist_name.keys():
        print(f"\t{i}: {hist_name[i]}, {round((hist_name[i] / len(detected) * 100), 2)}%")


recognize_face()
