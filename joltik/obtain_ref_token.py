from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

f = InstalledAppFlow.from_client_secrets_file("client_secret.json", scopes=['https://www.googleapis.com/auth/adwords'])
creds = f.run_local_server(port=8080)
with open('ref-token.json', 'w') as token:
    token.write(creds.to_json())