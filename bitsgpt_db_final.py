import os
import logging
import sys
from datetime import datetime
import constants
import mysql.connector
from langchain.document_loaders import TextLoader 
from langchain.indexes import VectorstoreIndexCreator
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI

# Set up logging
log_file_path = 'question_log.txt'
logging.basicConfig(filename=log_file_path, level=logging.INFO)

# MySQL connection configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Reset123',
    'database': 'dbforchatbot',
}

os.environ["OPENAI_API_KEY"] = constants.APIKEY

def get_user_details():
    # Ask for Username and Bits ID
    username = input("Enter your Username: ")
    bits_id = input("Enter your Bits ID: ")

    # Log user information
    user_info_message = f"User Information - Username: {username}, Bits ID: {bits_id}"
    logging.info(user_info_message)

    return username, bits_id

def insert_into_database(username, bits_id, query):
    # Connect to the database
    try:
        print('indatabase1')
        print(db_config)
        connection = mysql.connector.connect(**db_config)
        print('indatabase2')
        cursor = connection.cursor()
        print('indatabase3')
        # Insert data into the database
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print('indatabase4')
        insert_query = "INSERT INTO data (datetime, username, userid, questions) VALUES (%s, %s, %s, %s)"
        print('indatabase5')
        data = (current_time, username, bits_id, query)
        print('indatabase6')
        cursor.execute(insert_query, data)
        print('indatabase7')
        # Commit the changesasa
        connection.commit()

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the database connection
        if connection.is_connected():
            cursor.close()
            connection.close()

def run_chatbot(username, bits_id):
    while True:
        # Ask the user for a question
        query = input("Ask the chatbot (type 'exit' to end): ")
        if query.lower() == 'exit':
            break

        # Log the question along with user information
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print('------')
        log_message = f"{current_time} - {username} (Bits ID: {bits_id}) asked: {query}"
        logging.info(log_message)
        print('---------3a')
        print(username, bits_id, query)

        # Insert data into the database
        insert_into_database(username, bits_id, query)
        print('--------2')
        # Continue with the rest of the code
        loader = TextLoader('data.txt')
        print('---------1')
        index = VectorstoreIndexCreator().from_loaders([loader])
        print('---------0')

        response = index.query(query, llm=ChatOpenAI())
        print(response)
username, bits_id = get_user_details()
print('----------')

# Run the chatbot loop
run_chatbot(username, bits_id)
print('----------')
#hif __name__ == "__main__":
# Get user details
