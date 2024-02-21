import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from firebase_admin import db
import numpy as np

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "XXX",
    'storageBucket': "XXX"
})
student_db = db.reference(f'XXX').get()

# student_db = {'001': {'name': 'Sugondese Dover', 'others': 'blabla'},
#               '002': {'name': 'Ben Bols', 'others': 'bleble'}}
## Or put in your data as a dictionary like the dictionary above

dataset_path = "dataset_new"
stud_ids = os.listdir(dataset_path)

num_pics = 0
num_face = 0
encodings = []
for student_id in os.listdir(dataset_path):
    print(f"Encoding {student_db[str(student_id)]['nama']}'s face...")
    student_folder = os.path.join(dataset_path, student_id)
    if os.path.isdir(student_folder):
        to_mean = []
        for image_file in os.listdir(student_folder):
            image_path = os.path.join(student_folder, image_file)
            bkt_path = image_path.replace('\\', '/')

            bucket = storage.bucket()
            blob = bucket.blob(bkt_path)
            blob.upload_from_filename(bkt_path)

            face_image = face_recognition.load_image_file(image_path)
            face_encoding = face_recognition.face_encodings(face_image)
            num_pics += 1
            if len(face_encoding):
                to_mean.append(face_encoding[0])
                num_face += 1
                print(image_path)
        encodings.append(np.median(to_mean, axis=0))
    print(f"Number of Pictures: {num_pics}\nNumber of Faces: {num_face}\n")
    num_pics = 0
    num_face = 0

# Create a list containing both encodings and student IDs
encodings_with_ids = [encodings, stud_ids]

# Save the encodings with corresponding IDs to a file
with open('EncodeFileFinal.p', 'wb') as file:
    pickle.dump(encodings_with_ids, file)
    file.close()

print("Encoding file saved!")
