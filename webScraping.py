import requests
from bs4 import BeautifulSoup
import os
import face_recognition
import supabase

# Function to download images and convert faces to vectors
def download_images_and_store_vectors(url, num_to_download):
    save_directory = 'downloaded_images'

    # Check if the directory exists, create if it doesn't
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    existing_images = len([name for name in os.listdir(save_directory) if os.path.isfile(os.path.join(save_directory, name))])

    faces_downloaded = existing_images

    # Supabase connection
    supabase_url = 'https://eqeyugzznvjbkywsccfl.supabase.co'
    supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVxZXl1Z3p6bnZqYmt5d3NjY2ZsIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcwMTI4NjMzNywiZXhwIjoyMDE2ODYyMzM3fQ.dyF0FZp_LCfhrqzsNG8tIvMwEEzk8rA1Fg679btx28Q'
    supabase_client = supabase.create_client(supabase_url, supabase_key)

    while faces_downloaded < num_to_download + existing_images:
        response = requests.get(url[faces_downloaded % len(url)])
        html_content = response.content

        if response.status_code == 200:
            # Parse the HTML 
            soup = BeautifulSoup(html_content, 'html.parser')

            # Extract face images 
            for card in soup.find_all('div', class_='card-image'):
                if faces_downloaded >= num_to_download + existing_images:
                    break

                # Extract information src
                image_url = card.find('img')['src']

                # Download image
                image_response = requests.get(image_url)
                if image_response.status_code == 200:
                    filename = f"image_{faces_downloaded + 1}.jpg"
                    file_path = os.path.join(save_directory, filename)

                    # Save the image to the specified directory
                    with open(file_path, 'wb') as file:
                        file.write(image_response.content)
                        print(f"Downloaded: {filename}")

                    
                    image = face_recognition.load_image_file(file_path)

                    
                    face_locations = face_recognition.face_locations(image)

                    # convert it to a face vector
                    if len(face_locations) == 1:
                        face_encoding = face_recognition.face_encodings(image, known_face_locations=face_locations)[0]
                        # Convert the face encoding to a list for storage in Supabase
                        face_encoding_list = face_encoding.tolist()

                        # Store the face vector in the Supabase database
                        data = [{'face_vector': face_encoding_list}]
                        response = supabase_client.table('face').insert(data).execute()

                        

                    faces_downloaded += 1

            print(f"Total images downloaded: {faces_downloaded - existing_images}")
        else:
            print(f"Failed to fetch the webpage. Status Code: {response.status_code}")

# Website URLs
url = ['https://generated.photos/faces','https://generated.photos/faces/child','https://generated.photos/faces/elderly','https://generated.photos/faces/female','https://generated.photos/faces/right-facing','https://generated.photos/faces/young-adult','https://generated.photos/faces/adult','https://generated.photos/faces/front-facing','https://generated.photos/faces/male','https://generated.photos/faces/left-facing','https://generated.photos/faces/infant','https://generated.photos/faces/short','https://generated.photos/faces/joy']

# Number of photos to download
num_photos_to_download = 50

# Start downloading images and storing face vectors in Supabase
download_images_and_store_vectors(url, num_photos_to_download)