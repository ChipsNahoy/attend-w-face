# attend-w-face
An Attendance System using Face Recognition Model. Inspired by Face Recognition with Real-Time Database from Murtaza's Workshop Channel on Youtube.

This program attempts to mitigate the drawbacks of the regular pen-paper method in my uni. Using Python with face_recognition library.

Currently uses Firebase Realtime Database or regular Python dictionary, but can be changed to support all kinds of database systems.
The JSON is only used for Firebase integration.

This program used the face_recognition library to recognize people. It encodes faces from the training data directory and saves it as a .p file, which then will be used as a comparison with the newly detected and encoded face in the camera frame. If you watched the video that inspired this program, they only used 1 photo as the training data, but this program can use multiple photos of a single person to improve its recognition ability. When usually it encodes a single face and saves the encoding to represent the person, this program encodes a whole folder of a person's face and takes the average of the entire encoded face.

The uploaded program is used for testing. It will detect 100 faces before it closes. After that, it will give you how long the program was running, the average frame time, and the frequency of each detected face. With my system (i7-7700HQ), it takes around half a second for each recognition with an average accuracy of 99.45%.
