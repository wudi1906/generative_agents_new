#This script is intended to analyze agent conversations 

#importing modules
import json
import sys

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
                            print(f"Keyword '{keyword}' found in conversation with {persona}: {conversation}")
                            keywords[keyword] += 1

def main():
    try:
        # Load the JSON data
        json_file = sys.argv[1]
        with open(json_file, 'r') as file:
            json_data = json.load(file)

        # Define the keywords to search for and keeping a number count
        keywords = {'hiding': 0 , 'searching': 0, 'found you' : 0 , 'close-by': 0} 

        # Analyze the conversations
        print("Keywords in Agent Conversations:")
        analyze_convo(json_data, keywords)

        print()
        print(F"Keyword Count:")
        print(keywords)

    except IndexError:
        print("Error: No file name provided.")
    except FileNotFoundError:
        print(f"Error: File '{json_file}' not found.")
    except json.JSONDecodeError:
        print("Error: Invalid JSON file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
