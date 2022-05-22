# import the required libraries
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path
import base64
import email
from bs4 import BeautifulSoup
from database_queires import firebase_actions
firebase_obj = firebase_actions("self-f70d2-firebase-adminsdk-5noxc-2b24c749dd.json")
  
# Define the SCOPES. If modifying it, delete the token.pickle file.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
  
def credit_card_emails():
    existing_data = []
    for doc in firebase_obj.existing_data('credit_card'):
        existing_data.append(doc.to_dict())
        
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    #Get Messages
    results = service.users().messages().list(userId='me', labelIds=['Label_338684985447358641']).execute()
    messages = results.get('messages', [])
    row_number = len(existing_data)
    for msg in messages:
        # Get the message from its id
        txt = service.users().messages().get(userId='me', id=msg['id']).execute()
  
        # Use try-except to avoid any Errors
        try:
            # Get value of 'payload' from dictionary 'txt'
            payload = txt['payload']
            headers = payload['headers']
  
            # Look for Subject and Sender Email in the headers
            for d in headers:
                if d['name'] == 'Subject':
                    subject = d['value']
                if d['name'] == 'From':
                    sender = d['value']
            
            # The Body of the message is in Encrypted format. So, we have to decode it.
            # Get the data and decode it with base 64 decoder.
            parts = payload.get('parts')[0]
            data = parts['body']['data']
            data = data.replace("-","+").replace("_","/")
            decoded_data = base64.b64decode(data)
  
            # Now, the data obtained is in lxml. So, we will parse 
            # it with BeautifulSoup library
            soup = BeautifulSoup(decoded_data , "lxml")
            data = soup.find( "body" ).find("table").findAll("tr")[1].find("td").find("table").find("tr").find("td").find("table").find("tr").find("td").findAll("tr")[1].find("td")
            data = data.text.split('<br/>')[0].split('. ')[0].split(' for ')[2].split(' at ')
            amount = data[0].replace("Rs ",'')
            target = data[1].split(" on ")
            received_by = target[0]
            received_date = target[1]
            data = {"amount":float(amount),"receiver":received_by,"date":received_date}
            # Printing the subject, sender's email and message
            #if "HDFC" in subject.split(" "):
            #print("Subject: ", subject)
            #print("From: ", sender)
            #print("Message: Paid Rs. {price} to {receiver} ".format(price=amount,receiver=target))
            
            if data not in existing_data:
                row_number = int(row_number) + 1
                if row_number<=9:
                    row_number = "0"+str(row_number)
                firebase_obj.insert_credit_card_records(str(row_number),data)
            else:
                print("Not Inserted")
            
        except:
            pass
  
if __name__ == '__main__':
    credit_card_emails()
    
