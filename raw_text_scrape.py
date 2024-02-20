# This script is intended to scape agent conversations only

# importing modules
import json
import sys


# Function to analyze conversations and search for specific keywords
def raw_text_scrape(json_data):
    # Iterate through each entry in the JSON data
    for entry in json_data:
        # Check each persona's conversation if available
        for persona, details in entry["persona"].items():
            if "chat" in details and details["chat"]:
                for conversation in details["chat"]:
                    print(f"{conversation}\n")

    # with open(f"convo-analysis/key-words/{json_file}.txt", "w") as newfile:
    #     newfile.write("Keywords in Agent Conversations:\n")
    #     for element in non_rep_convos:
    #         newfile.write(f"{element}\n")
    #     newfile.write("\n")


def main():
    try:
        # Load the JSON data
        json_file = sys.argv[1]
        step_file = f"convo-analysis/JSON/{json_file}"

        with open(step_file, "r") as file:
            json_data = json.load(file)

        # Analyze the conversations
        raw_text_scrape(json_data)

    except IndexError:
        print("Error: No file name provided.")
    except FileNotFoundError:
        print(f"Error: File '{json_file}' not found.")
    except json.JSONDecodeError:
        print("Error: Invalid JSON file.")
        print(json_file)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
