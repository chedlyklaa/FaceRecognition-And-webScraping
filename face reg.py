import cv2
import face_recognition
import os
import time

# Directory path containing known faces for comparison
directory_path = '.\downloaded_images'


known_face_encodings = []
known_face_labels = []
temps_debut = time.time()
# multiple known faces 
for filename in os.listdir(directory_path):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        image_path = os.path.join(directory_path, filename)
        known_image = face_recognition.load_image_file(image_path)
        known_face_encoding = face_recognition.face_encodings(known_image)[0]  
        known_face_encodings.append(known_face_encoding)
        known_face_labels.append(filename.split('.')[0])  


cam_pardefaut = cv2.VideoCapture(0)

while True:
    # Capture each frame from the webcam
    ret, frame = cam_pardefaut.read()

    # Find all face locations in the current frame
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown Person"

        if True in matches:
            match_index = matches.index(True)
            name = known_face_labels[match_index]

       
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)
        temps_fin = time.time()
        duree_execution = temps_fin - temps_debut
        print("temps d excution :")
        print(duree_execution)
        temps_debut = time.time()

    # Display 
    cv2.imshow('Video', frame)

    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#close all windows

cam_pardefaut.release()
cv2.destroyAllWindows()