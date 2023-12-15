import cv2
import face_recognition
import supabase
import numpy as np

# Initialize Supabase client
supabase_url = 'https://eqeyugzznvjbkywsccfl.supabase.co'
supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVxZXl1Z3p6bnZqYmt5d3NjY2ZsIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcwMTI4NjMzNywiZXhwIjoyMDE2ODYyMzM3fQ.dyF0FZp_LCfhrqzsNG8tIvMwEEzk8rA1Fg679btx28Q'
supabase_client = supabase.create_client(supabase_url, supabase_key)

# Function to fetch face vectors from Supabase
def fetch_face_vectors():
    # Fetch face vectors stored in the 'face' table of Supabase
    try:
        response = supabase_client.table('face').select('face_vector').execute()
    except Exception as e:
        print(f"An error occurred: {e}")


    # Extract face vectors from the response
    response = supabase_client.table('face').select('face_vector').execute()
    # Extract face vectors from the response
    data = response.content.get('data', [])
    face_vectors = [np.array(record['face_vector']) for record in data]
    print("Successfully fetched face vectors from Supabase.")
    
    return face_vectors

# Load known face vectors from Supabase
known_face_encodings = fetch_face_vectors()

# Get a reference to your webcam (0 is usually the default camera)
cam_pardefaut = cv2.VideoCapture(0)

while True:
    # Capture each frame from the webcam
    ret, frame = cam_pardefaut.read()

    # Find all face locations in the current frame
    face_locations = face_recognition.face_locations(frame)
    
    # Get face encodings for each face in the current frame
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    # Loop through each face found in the frame
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Compare the detected face encoding with known face encodings
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown Person"

        # If a match is found, consider it a known face
        if True in matches:
            match_index = matches.index(True)
            name = f"Known Person {match_index + 1}"

        # Draw a rectangle around the face and display the name
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

    # Display the resulting frame
    cv2.imshow('Video', frame)

    # Break the loop when the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all windows
cam_pardefaut.release()
cv2.destroyAllWindows()
