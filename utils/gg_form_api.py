import os
import json
import requests
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from dotenv import load_dotenv
load_dotenv()
SCOPES = ['https://www.googleapis.com/auth/forms.body']
TOKEN_PATH = os.getenv('TOKEN_FILE', 'token.json')
CREDENTIALS_PATH = os.getenv('CREDENTIALS_FILE', 'credentials.json')

SERVICE_ENDPOINT = 'https://forms.googleapis.com'

def get_credentials():
    creds = None
    token_path = TOKEN_PATH
    creds_path = CREDENTIALS_PATH  # Downloaded from Google Cloud Console

    # Load saved credentials
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    # If no valid credentials, start OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=50699)

        # Save credentials for next time
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
    return creds

def create_form_with_question(creds):
    headers = {
        'Authorization': f'Bearer {creds.token}',
        'Content-Type': 'application/json'
    }
    # Step 1: Create form
    form_data = {
        "info": {
            "title": "Python Quiz"
        },
    }
    resp = requests.post(f'{SERVICE_ENDPOINT}/v1/forms', headers=headers, json=form_data)
    form = resp.json()
    form_id = form['formId']
    print(f"Form created: {form['responderUri']}")

    # Step 2: Add question
    question_data = {
        "requests": [{
            "createItem": {
                "item": {
                    "title": "What does 'def' do in Python?",
                    "questionItem": {
                        "question": {
                            "required": True,
                            "choiceQuestion": {
                                "type": "RADIO",
                                "options": [
                                    {"value": "Defines a variable"},
                                    {"value": "Defines a function"},
                                    {"value": "Defines a class"},
                                    {"value": "Defines a module"}
                                ]
                            }
                        }
                    }
                },
                "location": {"index": 0}
            }
        }]
    }
    resp = requests.post(
        f'{SERVICE_ENDPOINT}/v1/forms/{form_id}:batchUpdate',
        headers=headers,
        json=question_data
    )
    print("Question added!")

def main():
    creds = get_credentials()
    create_form_with_question(creds)

if __name__ == "__main__":
    main()
