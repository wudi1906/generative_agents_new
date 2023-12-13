import os
import sys
import json


def get_unique_conversations(simulation_name):
    step_folder = f"environment/frontend_server/storage/{simulation_name}/movement"

    observed_conversations = set()
    file_contents = []

    # Iterate over all files in the simulation folder
    for filename in os.listdir(step_folder):
        filepath = os.path.join(step_folder, filename)

        with open(filepath, "r") as file:
            data = json.load(file)
            personas = data["persona"]

            # Loop over all personas except one, since conversations are always
            # between two people
            for name in list(personas.keys())[:-1]:
                persona = personas[name]
                chat = persona["chat"]

                if chat:
                    chat_string = str(chat)

                    if chat_string not in observed_conversations:
                        observed_conversations.add(chat_string)
                        file_contents.append(data)
                        break

    return file_contents


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the simulation name as a command line argument.")
        sys.exit(1)

    simulation_name = sys.argv[1]
    unique_conversations = get_unique_conversations(simulation_name)
    print(json.dumps(unique_conversations, indent=2))
