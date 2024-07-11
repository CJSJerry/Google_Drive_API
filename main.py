from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Path to the service account key file
SERVICE_ACCOUNT_FILE = 'service_account.json'

# Define the required scopes
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# Create credentials using the service account key file
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Build the Drive API client
service = build('drive', 'v3', credentials=credentials)

def upload_file(file_path, file_name, folder_id):
    
    # Set the metadata for the file
    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }

    # Upload the file
    media = MediaFileUpload(file_path, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id, webViewLink').execute()
    
    # Set permissions
    service.permissions().create(fileId=file['id'], body={'type': 'anyone', 'role': 'reader'}).execute()

    return file['webViewLink']

if __name__ == '__main__':
    link = upload_file('C:\\Users\\CJJer\\coding\\GDrive\\test.txt', 'test.txt', '1kyX7Ald3GBLkxyFX2g_mdC1_6APPvvH_')
    print(f'File Link: {link}')