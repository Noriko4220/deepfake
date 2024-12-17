import os
import time
from flask import Flask, request, jsonify, send_file, send_from_directory
from werkzeug.utils import secure_filename
from flask_cors import CORS
from google_drive_helper import upload_to_drive, download_from_drive
from googleapiclient.discovery import build
from google.oauth2 import service_account
from threading import Thread

SERVICE_ACCOUNT_FILE = 'credentials/deepfake-444719-e99653d65880.json'

SCOPES = ['https://www.googleapis.com/auth/drive']

credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads')
PROCESSED_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'processed')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

DRIVE_FOLDER_ID = '1CVQP4MZ9XAEALKgrds0VJFi4ezIel_za'

PROCESS_STATUS = {}

drive_service = build('drive', 'v3', credentials=credentials)


def get_file_id(file_name, folder_id):
    try:
        query = f"'{folder_id}' in parents and name = '{file_name}' and trashed = false"
        results = drive_service.files().list(q=query, spaces='drive', fields='files(id, name)', pageSize=1).execute()
        files = results.get('files', [])

        if not files:
            raise FileNotFoundError(f"File '{file_name}' not found in folder ID: {folder_id}")

        file_id = files[0]['id']
        print(f"File '{file_name}' found with ID: {file_id}")
        return file_id
    except Exception as e:
        print(f"Error retrieving file ID: {e}")
        raise

@app.route('/upload', methods=['POST'])
def upload_files():
    try:
        if 'video' not in request.files or 'image' not in request.files:
            return jsonify({'error': 'Both video and image files are required'}), 400

        video = request.files['video']
        image = request.files['image']
        video_path = os.path.join(UPLOAD_FOLDER, 'video.mp4')
        image_path = os.path.join(UPLOAD_FOLDER, 'image.jpg')
        video.save(video_path)
        image.save(image_path)

        video_id = upload_to_drive(video_path, DRIVE_FOLDER_ID)
        image_id = upload_to_drive(image_path, DRIVE_FOLDER_ID)

        PROCESS_STATUS[video_id] = {'ready': False, 'processed_id': None}
        simulate_processing(video_id)

        return jsonify({'message': 'Files uploaded successfully', 'video_id': video_id, 'image_id': image_id})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/status', methods=['GET'])
def check_status():
    video_id = request.args.get('video_id')
    if video_id not in PROCESS_STATUS:
        return jsonify({'error': 'Invalid video_id'}), 400

    if not PROCESS_STATUS[video_id]['ready']:
        return jsonify({'ready': False})

    try:
        processed_id = get_file_id('swapped.mp4', DRIVE_FOLDER_ID)
        PROCESS_STATUS[video_id]['processed_id'] = processed_id
        return jsonify({'ready': True, 'processed_id': processed_id})
    except FileNotFoundError:
        return jsonify({'ready': False})

@app.route('/download/<file_id>', methods=['GET'])
def download_file(file_id):
    try:
        output_path = os.path.join(PROCESSED_FOLDER, 'swapped.mp4')

        download_from_drive(file_id, output_path)

        return send_file(output_path, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/static/processed/<filename>')  
def serve_processed_file(filename):
    try:
        return send_from_directory(PROCESSED_FOLDER, filename)
    except Exception as e:
        print(f"Error serving file: {e}")
        return jsonify({'error': str(e)}), 500

def simulate_processing(video_id):
    def process():
        max_attempts = 360
        attempt = 0
        processed_id = None

        print("Starting periodic search for 'swapped.mp4'...")

        while attempt < max_attempts:
            try:
                processed_id = get_file_id('swapped.mp4', DRIVE_FOLDER_ID)

                print(f"File 'swapped.mp4' found! ID: {processed_id}")
                PROCESS_STATUS[video_id]['ready'] = True
                PROCESS_STATUS[video_id]['processed_id'] = processed_id

                output_path = os.path.join(PROCESSED_FOLDER, 'swapped.mp4')
                download_from_drive(processed_id, output_path)
                print(f"File downloaded to: {output_path}")

                return

            except FileNotFoundError:
                attempt += 1
                print(f"Attempt {attempt}/{max_attempts}: 'swapped.mp4' not found. Retrying in 5 seconds...")
                time.sleep(5)

        print("Processing timed out: 'swapped.mp4' not found after maximum attempts.")

    Thread(target=process).start()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
