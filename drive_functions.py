
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials

# Load service account credentials
SERVICE_ACCOUNT_FILE = "decision-maker-scraper-service_account.json" 
scopes = ['https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, scopes)

# Authenticate and initialize PyDrive
gauth = GoogleAuth()
gauth.credentials = creds
drive = GoogleDrive(gauth)

def get_max_file_number(folder_id):
    # Auto-iterate through all files that matches this query
    query = f"'{folder_id}' in parents and trashed=false"
    file_list = drive.ListFile({'q': query}).GetList()
    results_numbers = []
    for file_info in file_list:
        file_name = file_info['title']
        if "results_" in file_name and ".csv" in file_name:
            end = file_name.index(".csv")
            results_numbers.append(int(file_name[8:end]))
    return max(results_numbers)

# Upload a file to the shared Google Drive folder
def drive_upload(upload_file_name, folder_id):
    file_to_upload = drive.CreateFile({
        'title': upload_file_name,
        'mimeType': 'text/csv',
        'parents': [{'id': folder_id}]  # Replace with the shared folder ID
    })
    file_to_upload.SetContentFile(upload_file_name)  # The file you want to upload
    file_to_upload.Upload()

    print("✅ File uploaded successfully!")
