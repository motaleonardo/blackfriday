import requests
from dotenv import load_dotenv, find_dotenv
import os
from pprint import pprint

# Load the environment variables
load_dotenv(find_dotenv())

# API Token & Form ID
form_id = os.getenv('FORM_ID')
api_token = os.getenv('API_TOKEN_TYPEFORM')

# Access the form responses
url = f'https://api.typeform.com/forms/{form_id}/responses'
headers = {'Authorization': f'Bearer {api_token}'}
params = {'page_size': 100}

# Get the responses
response = requests.get(url, headers=headers, params=params)

# Print the responses
pprint(response.json())