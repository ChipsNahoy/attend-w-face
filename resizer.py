import cv2
import os

dataset_path = "dataset_new"

for student_id in os.listdir(dataset_path):
    student_folder = os.path.join(dataset_path, student_id)
    print(f"Student_id: {student_id}")
    if os.path.isdir(student_folder):
        for image_file in os.listdir(student_folder):
            image_path = os.path.join(student_folder, image_file)
            img = cv2.imread(image_path)
            if img.shape != (216, 216, 3):
                img = cv2.resize(img, (216,216), interpolation=cv2.INTER_AREA)
                cv2.imwrite(image_path, img)
                print(f"Resized img address: {image_path}")
    print()
