Project Documentation

Project Structure
The project is organized as follows:
face-swap
- backend/
-- uploads/                # Folder where uploaded files (video, image) are stored
-- processed/              # Folder where downloaded processed video (swapped.mp4) is stored
-- server.py               # Flask server for handling API endpoints
-- google_drive_helper.py  # Google Drive API helper functions
- frontend/
-- index.html              # HTML structure for the frontend
-- app.js                  # JavaScript file for frontend logic
-- style.css               # Styling for the frontend UI
- credentials/
-- creds.json    # Google Drive API service account credentials
- readme.md    # Project documentation file

1. server.py - Flask Backend
The server.py is the main backend file. It provides API endpoints to upload files, check processing status, and download processed files.

Functions and Routes
get_file_id(file_name, folder_id)
Purpose: Retrieves the file ID for a specific file (file_name) from a Google Drive folder.
Parameters:
file_name (str): The name of the file to search.
folder_id (str): The Google Drive folder ID where the file is stored.
Output: Returns the file ID if found or raises FileNotFoundError.

/upload (POST)
Purpose: Receives a video and an image from the user, renames and uploads them to Google Drive.
Steps:
Accepts two files: video and image.
Renames the files to video.mp4 and image.jpg.
Saves the files in the uploads/ folder.
Uploads the files to Google Drive.
Initiates the simulate_processing function to simulate processing.
Returns: A JSON response containing the uploaded file IDs.

/status (GET)
Purpose: Checks the processing status of the uploaded files.
Steps:
Checks if swapped.mp4 exists in the Google Drive folder.
Updates the PROCESS_STATUS dictionary when the file is found.
Returns: A JSON response indicating whether the file is ready.

/download/<file_id> (GET)
Purpose: Downloads the processed file (swapped.mp4) from Google Drive.
Steps:
Downloads the file using its ID to the processed/ folder.
Returns the file to the user as an attachment.

/static/processed/<filename> (GET)
Purpose: Serves the processed file (swapped.mp4) from the processed/ folder.
simulate_processing(video_id)
Purpose: Simulates the processing of the uploaded files by periodically searching for swapped.mp4.
Steps:
Searches for the file every 5 seconds using get_file_id.
Downloads the file once it is found.
Runs in: A separate thread to avoid blocking the main server.

2. google_drive_helper.py - Google Drive API Helper
This file contains helper functions to interact with the Google Drive API, including file uploads and downloads.

Functions
upload_to_drive(file_path, folder_id)
Purpose: Uploads a file to a specific Google Drive folder.
Parameters:
file_path (str): Path to the file on the server.
folder_id (str): Google Drive folder ID.
Output: Returns the file ID of the uploaded file.

download_from_drive(file_id, output_path)
Purpose: Downloads a file from Google Drive using its file ID.
Parameters:
file_id (str): ID of the file to download.
output_path (str): Local path to save the downloaded file.
Steps:
Downloads the file in chunks using MediaIoBaseDownload.
Saves the file locally to the specified output_path.

3. index.html - Frontend HTML
The HTML file provides the structure for the frontend user interface.
Structure

File Upload Section:
Two input fields to upload a video and an image.
A button to trigger the "Run Model" function.

Loading Section:
A hidden div to show a loading message during processing.

Results Section:
Two <video> elements to display the original video and the processed video.
Three buttons to control the view:
Show Original: Displays only the original video.
Show Processed: Displays only the processed video.
Show Both: Displays both videos side by side.

4. app.js - Frontend JavaScript Logic
The app.js file provides the logic to interact with the backend API and handle video display functionality.

Functions
runModel()
Purpose: Handles the file upload process, starts the model, and polls for processing status.
Steps:
Collects the uploaded video and image files.
Sends the files to the backend via the /upload endpoint.
Polls the /status endpoint every 5 seconds to check if the processed file is ready.
Once ready, downloads the processed file from /download/<file_id> and displays it.

showOriginal()
Purpose: Displays only the original video.
Steps:
Hides the processed video.
Centers the original video.

showProcessed()
Purpose: Displays only the processed video.
Steps:
Hides the original video.
Centers the processed video.

showBoth()
Purpose: Displays both videos side by side.
Steps:
Adjusts the layout to display both videos in a horizontal row.

5. style.css - Styling for the Frontend UI
The style.css file provides styles for the HTML elements to improve the appearance of the user interface.

Key Styles
Page Layout:
Centered content with a clean and modern design.

Buttons:
Styled buttons with hover and focus effects for better interactivity.

Video Display:
Videos are styled to have a clean border, shadow, and slight scaling effect on hover.

Dynamic Layout:
Single video is centered when either Show Original or Show Processed is pressed.
Videos are displayed in a horizontal row when Show Both is pressed.
Loading Indicator:
A visible message that appears while the backend is processing the uploaded files.

6. credentials
This is the service account JSON file for the Google Drive API.
It contains the credentials used by the backend to authenticate with Google Drive.

How the Project Works
File Upload:
The user uploads a video and an image on the frontend.
The files are sent to the backend using the /upload endpoint.

Processing:
The backend uploads the files to Google Drive.
The backend periodically checks for the swapped.mp4 file in Google Drive.

File Download:
Once the processed file is found, it is downloaded to the backend/processed folder.

Video Display:
The frontend fetches the processed video and displays it alongside the original video.

User Controls:
The user can choose to view only the original video, only the processed video, or both videos side by side.
