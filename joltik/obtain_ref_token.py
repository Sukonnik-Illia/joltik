import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from dotenv import dotenv_values
dotenv = dotenv_values(".env")

f = InstalledAppFlow.from_client_secrets_file("client_secret.json", scopes=['https://www.googleapis.com/auth/adwords'])
creds = f.run_local_server(port=8080)
with open('ref-token.json', 'w') as token:
    config = json.loads(creds.to_json())
    config["use_proto_plus"] = True
    config["developer_token"] = dotenv["DEVELOPER_TOKEN"]
    config["login_customer_id"] = dotenv["LOGIN_CUSTOMER_ID"]
    token.write(json.dumps(config, indent=4))
    