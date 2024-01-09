#This python script will be used to analyze the agents conversations 
#importing modules 
import os 
import json 
import sys

#Declaring functions 
# Function to analyze conversations and search for specific keywords
def analyze_convo(json_data, keywords):
    # Iterate through each entry in the JSON data
    for entry in json_data:
        # Check each persona's conversation if available
        for persona, details in entry['persona'].items():
            if 'chat' in details and details['chat']:
                for conversation in details['chat']:
                    # Check if any of the keywords are in the conversation
                    for keyword in keywords:
                        if keyword in conversation[1]:
                            print(f"Keyword '{keyword}' found in conversation: {conversation}")

# Load the JSON data
json_string = sys.argv[1]
json_data = json.loads(json_string)

# Define the keywords to search for
keywords = ['hiding', 'searching', 'found', 'close-by']  # Add more keywords as needed

# Analyze the conversations
analyze_convo(json_data, keywords)


