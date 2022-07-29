
from __future__ import print_function
import httplib2
import os
import json

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import pandas as pd

def get_columns():
    return ('dt', 'from', 'title', 'url', 'summary', 'image', 'brief', 'body', 'raw_page') 
def get_empty_columns():
    return ('', '', '', '', '', '', '', '', '') 

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def main():
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    
    lableIDs = ['Label_47']
    messages = []
        
    #results = service.users().labels().list(userId='me').execute()
    response = service.users().messages().list(userId='me', labelIds=lableIDs).execute()
    #results.get(, id=msg_id).execute()

    if 'messages' in response:
      messages.extend(response['messages'])
    
    #print (results)
    #labels = results.get('messages', [])
    #messages = results.get('messages', [])

    while 'nextPageToken' in response:
      page_token = response['nextPageToken']
      response = service.users().messages().list(userId='me', labelIds=lableIDs,
                                         pageToken=page_token).execute()
      messages.extend(response['messages'])    
        
    #if not labels:
    if not messages:
        #print('No labels found.')
        print('No messages found.')
    else:
      print('Messages:')
      print (len(messages))
#      for label in labels:
      idx = 0
      df = pd.DataFrame(columns = get_columns())
      for message in messages:        
        response = service.users().messages().get(userId='me',
                                                 id=message['id']).execute()
        
        #print (type(response['payload']['headers']))
        tt = response['payload']['headers']
        #print (tt[6]['value'])
        #print (tt[5])

        #print (response['Subject'])
        #print (response['body'])
        #print (response['snippet'])

        #print ('Message snippet: %s' % response['snippet'])
        df.loc[idx] = get_empty_columns()
        df.loc[idx]['title'] = tt[7]['value']
        
        df.loc[idx]['dt'] = tt[6]['value']
        #df.loc[idx]['body'] = response['body']
        df.loc[idx]['brief'] = response['snippet']        
        df.loc[idx]['raw_page'] = response
        idx += 1
        
        #print ('Message: %s' % response)
        #print(label['name'])
        #print (message['id'])
          
        print ('write out file')
        
        fname = './data/json/google_message' + str(idx) + '.json'
        with open(fname, 'w+') as json_file:
            json.dump(response, json_file, ensure_ascii=False)
          
      df.to_csv('google_huizhou_messages.csv', encoding='utf-8', index=False)

if __name__ == '__main__':
    main()