import requests
from dotenv import load_dotenv, find_dotenv
import os
from pprint import pprint
import pandas as pd
from sqlalchemy import create_engine

# Load the environment variables
load_dotenv(find_dotenv())

# API Token & Form ID
form_id = os.getenv('FORM_ID')
api_token = os.getenv('API_TOKEN_TYPEFORM')

# Replace these variables with your actual database credentials
db_username = os.getenv('USERNAME')
db_password = os.getenv('PASSWORD')
db_host = os.getenv('HOST')
db_port = os.getenv('PORT')
db_name = os.getenv('DATABASE')

# Access the form responses
url = f'https://api.typeform.com/forms/{form_id}/responses'
headers = {'Authorization': f'Bearer {api_token}'}
params = {'page_size': 100}

# Get the responses
response = requests.get(url, headers=headers, params=params)

# Check if the request was successful
if response.status_code == 200:
    # Get the data
    data = response.json()

    # Get the responses
    responses = data['items']

    # Create a list to store the formatted responses
    formatted_responses = []

    for resp in responses:
        formatted_resp = {
            'submitted_at': resp['submitted_at'],
            'response_id': resp['response_id']
        }

        # Get the answers for each question
        for answer in resp['answers']:
            question_id = answer['field']['ref']
            question_type = answer['type']

            # Check the type of question
            if question_type in ['text', 'number', 'date']:
                formatted_resp[question_id] = answer[question_type]
            elif question_type == 'choice':
                formatted_resp[question_id] = answer['choice']['label']
            elif question_type == 'choices':
                formatted_resp[question_id] = ', '.join([choice['label'] for choice in answer['choices']['labels']])
        
        formatted_responses.append(formatted_resp)

    # Create a DataFrame
    df = pd.DataFrame(formatted_responses)


    # Create the connection string
    connection_string = f'postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}'
    # Create the SQLAlchemy engine
    engine = create_engine(connection_string)

    # Write the DataFrame to a SQL table
    df.to_sql('typeform_responses', con=engine, if_exists='replace', index=False)

    print("Connection to SQL database established and Typeform data transferred successfully.")