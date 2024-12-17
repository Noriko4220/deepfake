import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.oauth2 import service_account

# Google Drive API setup
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'credentials/deepfake-444719-e99653d65880.json'  

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=credentials)


def upload_to_drive(file_path, folder_id):
    try:
        file_metadata = {
            'name': os.path.basename(file_path),
            'parents': [folder_id]
        }
        media = MediaFileUpload(file_path, resumable=True)
        file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(f"Uploaded {file_path} to Google Drive with ID: {file['id']}")
        return file['id']
    except Exception as e:
        print(f"Error uploading file to Google Drive: {e}")
        raise


def download_from_drive(file_id, output_path):
    try:
        print(f"Starting download. File ID: {file_id}, Output Path: {output_path}")

        request = drive_service.files().get_media(fileId=file_id)
        with open(output_path, 'wb') as f:
            downloader = MediaIoBaseDownload(f, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                print(f"Download progress: {int(status.progress() * 100)}%")
            
        if os.path.exists(output_path):
            print(f"File downloaded successfully to: {output_path}")
        else:
            print(f"Download failed: {output_path} does not exist.")
            raise FileNotFoundError(f"Downloaded file not found: {output_path}")
    except Exception as e:
        print(f"Error downloading file from Google Drive: {e}")
        raise
