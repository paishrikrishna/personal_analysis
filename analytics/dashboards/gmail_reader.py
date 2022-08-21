from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path
import base64
import email
from bs4 import BeautifulSoup
from dashboards.database_queires import firebase_actions

#firebase_obj = firebase_actions("/home/shripais003/personal_analysis/analytics/dashboards/self-f70d2-firebase-adminsdk-5noxc-2b24c749dd.json")
  
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
  
def credit_card_emails(firebase_obj):
    existing_data = []
    for doc in firebase_obj.existing_data('credit_card'):
        existing_data.append(doc.to_dict())
        
    creds = None
    if os.path.exists('/home/shripais003/personal_analysis/analytics/dashboards/token.pickle'):
        with open('/home/shripais003/personal_analysis/analytics/dashboards/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '/home/shripais003/personal_analysis/analytics/dashboards/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('/home/shripais003/personal_analysis/analytics/dashboards/token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    results = service.users().messages().list(userId='me', labelIds=['Label_338684985447358641']).execute()
    messages = results.get('messages', [])
    row_number = len(existing_data)
    for msg in messages:
        txt = service.users().messages().get(userId='me', id=msg['id']).execute()
  
        try:
            payload = txt['payload']
            headers = payload['headers']
  
            for d in headers:
                if d['name'] == 'Subject':
                    subject = d['value']
                if d['name'] == 'From':
                    sender = d['value']
            
            parts = payload.get('parts')[0]
            data = parts['body']['data']
            data = data.replace("-","+").replace("_","/")
            decoded_data = base64.b64decode(data)
  
            soup = BeautifulSoup(decoded_data , "lxml")
            data = soup.find( "body" ).find("table").findAll("tr")[1].find("td").find("table").find("tr").find("td").find("table").find("tr").find("td").findAll("tr")[1].find("td")
            data = data.text.split('<br/>')[0].split('. ')[0].split(' for ')[2].split(' at ')
            amount = data[0].replace("Rs ",'')
            target = data[1].split(" on ")
            received_by = target[0]
            received_date = target[1]
            data = {"amount":float(amount),"receiver":received_by,"date":received_date}
            
            if data not in existing_data:
                row_number = int(row_number) + 1
                if row_number<=9:
                    row_number = "0"+str(row_number)
                firebase_obj.insert_credit_card_records(str(row_number),data)
            else:
                print("Not Inserted")
            
        except:
            pass

    
