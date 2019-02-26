from __future__ import print_function
import pickle
import os.path
import sys
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import traceback

# If modifying these scopes, delete the file token.pickle.

class Google():
      def __init__(self):
          self.__SCOPES_CONTACT = ['https://www.googleapis.com/auth/contacts']

      def createContact(self, data):
          try:

            # Credentials file from google api
            # https://console.developers.google.com/apis/credentials
            file_credentials = sys.path[0] + '/addons/management_api/config/credentials.json'
            credentials = None

            # The file token.pickle stores the user's access and refresh tokens, and is
            # created automatically when the authorization flow completes for the first
            # time.
            if os.path.exists('token.pickle'):
                with open('token.pickle', 'rb') as token:
                    credentials = pickle.load(token)

            # If there are no (valid) credentials available, let the user log in.
            if not credentials or not credentials.valid:
                if credentials and credentials.expired and credentials.refresh_token:
                    credentials.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        file_credentials, self.__SCOPES_CONTACT)
                    credentials = flow.run_local_server()

                # Save the credentials for the next run
                with open('token.pickle', 'wb') as token:
                    pickle.dump(credentials, token)

            service = build('people', 'v1', credentials=credentials)
            
            try:
              service.people().createContact(
                body=data
              ).execute()

              # Success response
              print('='*100)
              print('Contact has been created')
            except Exception as identifier:
              print(identifier)

            # Call the People API
            # print('List 10 connection names')

            # results = service.people().connections().list(
            #     resourceName='people/me',
            #     pageSize=10,
            #     personFields='names,emailAddresses,phoneNumbers').execute()
            # connections = results.get('connections', [])

            # for person in connections:
            #     print(person)
            #     names = person.get('names', [])
            #     if names:
            #         name = names[0].get('displayName')
            #         print(name)
          except Exception as identifier:
            print(traceback.format_exc())