from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pathlib import Path
import io
from googleapiclient.http import MediaIoBaseDownload

#authenticate with google
gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

#get all the text files with the .txt exention in top level Google Drive directory
def get_txt_files(dir_id='root'):
    file_list = drive.ListFile({'q': f"'{dir_id}' in parents and trashed=false"}).GetList()
    for file1 in file_list:
        print('title: %s, id: %s' % (file1['title'], file1['id']))
    return [[file1['title'], file1['id'], file1.GetContentString()]
            for file1 in file_list if file1['title'].endswith(".txt")]

def get_google_doc_files(dir_id='root'):
    file_list = drive.ListFile({'q': f"'{dir_id}' in parents and trashed=false and mimeType='application/vnd.google-apps.document'"}).GetList()
    for file1 in file_list:
        print('title: %s, id: %s' % (file1['title'], file1['id']))
    return [[file1['title'], file1['id'], download_as_text(file1['id'])] for file1 in file_list]

def download_as_text(file_id):
    request = drive.auth.service.files().export_media(fileId=file_id, mimeType='text/plain')
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
    fh.seek(0)
    return fh.read().decode('utf-8')

def create_test_file():
    "not currently used, but useful for testin. "

    #create GoogelDriveFile instance with title "hello.txt"
    file1 = drive.CreateFile("hello.txt")
    file1.SetContentFile('Hello World!')
    file1.Upload()

def test():
    files = get_google_doc_files()
    for file in files:
        title, file_id, content = file
        print('title: %s, id: %s' % (title, file_id))
        with open("data/" + title, "w") as f:
            f.write(content)

if __name__ == '__main__':
    test()