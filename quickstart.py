import datetime
import os.path
from os import path
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive"]
PATH_TO_LOCAL_FILES = 'C:/Users/balaz/OneDrive/Documents/Obsidian Vault'
PATH_TO_DRIVE_FILES = "name='Notes'"

creds = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first time.
if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      # If there are no (valid) credentials available, let the user log in.
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())



def changeDateFormat(timeDate):
  date = datetime.datetime.utcfromtimestamp(timeDate)
  return date.strftime('%d %b %Y %H %M %S')

def checkChanges():
    with os.scandir(PATH_TO_LOCAL_FILES) as dir_entries:
        for dir_entry in dir_entries:
            if os.path.splitext(dir_entry)[-1] == ".md":
                print(dir_entry.name)
                dir_date = changeDateFormat(dir_entry.stat().st_atime)
                print(dir_date)

    try:
        service = build("drive", "v3", credentials=creds)
        results = (
            service.files()
            .list(q=PATH_TO_DRIVE_FILES, fields="nextPageToken, files(id, name)")
            .execute()
        )
        items = results.get("files", [])

        if not items:
            print("File not found, upload files")
        else:
            for item in items:
                print(item['name'], item['id'])

    except HttpError as err:
        print(err.error_details)



'''
def main():
  """Shows basic usage of the Drive v3 API.
  Prints the names and ids of the first 10 files the user has access to.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("drive", "v3", credentials=creds)

    # Call the Drive v3 API
    results = (
        service.files()
        .list(pageSize=10, fields="nextPageToken, files(id, name)")
        .execute()
    )
    items = results.get("files", [])

    if not items:
      print("No files found.")
      return
    print("Files:")
    for item in items:
      print(f"{item['name']} ({item['id']})")
  except HttpError as error:
    # TODO(developer) - Handle errors from drive API.
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()
'''

checkChanges()
